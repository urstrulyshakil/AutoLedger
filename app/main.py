# ===== AutoLedger main.py =====

import streamlit as st
st.set_page_config(
    page_title="AutoLedger",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime
import io  # <-- for Excel export

# =========================
# File paths
# =========================
DATA_FILE = "transactions.csv"
BACKUP_FILE = "transactions_backup.csv"

# =========================
# Load or initialize transactions
# =========================
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE, parse_dates=["Date"])
else:
    df = pd.DataFrame(columns=["Date", "Description", "Amount", "Category"])

# Backup if not exists
if not os.path.exists(BACKUP_FILE):
    df.to_csv(BACKUP_FILE, index=False)

# =========================
# Session state for UI
# =========================
if "transactions" not in st.session_state:
    st.session_state["transactions"] = df.copy()

# =========================
# Sidebar - Add Transaction
# =========================
st.sidebar.header("Add Transaction")
with st.sidebar.form(key="add_transaction"):
    date = st.date_input("Date", datetime.today())
    description = st.text_input("Description")
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    category = st.selectbox("Category", ["Food", "Transport", "Entertainment", "Bills", "Shopping", "Other"])
    submit = st.form_submit_button("Add Transaction")
    
    if submit:
        new_entry = {
            "Date": pd.to_datetime(date),
            "Description": description,
            "Amount": amount,
            "Category": category
        }
        st.session_state["transactions"] = pd.concat(
            [st.session_state["transactions"], pd.DataFrame([new_entry])],
            ignore_index=True
        )
        st.success("Transaction added!")
        # Save to CSV and backup
        st.session_state["transactions"].to_csv(DATA_FILE, index=False)
        st.session_state["transactions"].to_csv(BACKUP_FILE, index=False)

# =========================
# Sidebar - Filters
# =========================
st.sidebar.header("Filters")
filter_start = st.sidebar.date_input("Start Date", df["Date"].min() if not df.empty else datetime.today())
filter_end = st.sidebar.date_input("End Date", df["Date"].max() if not df.empty else datetime.today())
filter_category = st.sidebar.multiselect(
    "Category",
    options=df["Category"].unique() if not df.empty else [],
    default=None
)

# =========================
# Filter transactions
# =========================
filtered_df = st.session_state["transactions"].copy()

if not filtered_df.empty:
    filtered_df = filtered_df[(filtered_df["Date"] >= pd.to_datetime(filter_start)) &
                              (filtered_df["Date"] <= pd.to_datetime(filter_end))]
    if filter_category:
        filtered_df = filtered_df[filtered_df["Category"].isin(filter_category)]

# =========================
# Main Dashboard
# =========================
st.title("💰 AutoLedger")

st.header("Summary")
col1, col2 = st.columns(2)
col1.metric("Total Transactions", len(filtered_df))
col2.metric("Total Amount", f"${filtered_df['Amount'].sum():.2f}")

st.header("Transactions")
st.dataframe(filtered_df.sort_values(by="Date", ascending=False), use_container_width=True)

# Delete transaction
st.header("Delete Transaction")
if not filtered_df.empty:
    index_to_delete = st.selectbox("Select row to delete (by index)", filtered_df.index)
    if st.button("Delete"):
        st.session_state["transactions"].drop(index=index_to_delete, inplace=True)
        st.session_state["transactions"].to_csv(DATA_FILE, index=False)
        st.success("Transaction deleted!")
        st.experimental_rerun()

# =========================
# Charts
# =========================
st.header("Category Charts")
if not filtered_df.empty:
    category_sum = filtered_df.groupby("Category")["Amount"].sum()
    # Bar chart
    st.subheader("Spending by Category (Bar)")
    fig, ax = plt.subplots()
    category_sum.plot(kind="bar", ax=ax, color="skyblue")
    ax.set_ylabel("Amount ($)")
    ax.set_xlabel("Category")
    ax.set_title("Total Spending per Category")
    st.pyplot(fig)

    # Pie chart
    st.subheader("Spending by Category (Pie)")
    fig2, ax2 = plt.subplots()
    category_sum.plot(kind="pie", autopct="%1.1f%%", ax=ax2)
    ax2.set_ylabel("")
    st.pyplot(fig2)

# =========================
# Export Data
# =========================
st.header("Export Transactions")
col1, col2 = st.columns(2)

# CSV Export
with col1:
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", csv, "transactions.csv", "text/csv")

# Excel Export
with col2:
    excel_buffer = io.BytesIO()
    filtered_df.to_excel(excel_buffer, index=False, engine="openpyxl")
    excel_buffer.seek(0)
    st.download_button(
        label="Download Excel",
        data=excel_buffer,
        file_name="transactions.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )