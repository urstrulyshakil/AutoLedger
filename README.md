# 💰 AutoLedger
_Track every transaction, master your finances 🧾_

[![Python](https://img.shields.io/badge/python-3.10-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.22.0-orange)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/docker-ready-blue)](https://www.docker.com/)

AutoLedger is a lightweight, dark-mode financial tracker built with **Streamlit** and fully Dockerized. Easily add, delete, filter, and visualize your transactions, while exporting your data for backup or analysis.

---

## Features

- **Sleek Dark Mode:** Modern interface optimized for readability  
- **Add Transactions:** Record date, description, amount, and category  
- **Delete Transactions:** Remove incorrect entries easily  
- **Filter Transactions:** Filter by date range and category  
- **Summary Metrics:** Quick overview of total transactions and total amounts  
- **Monthly Summary & Charts:** Bar and pie charts for spending trends and category analysis  
- **Export Data:** Download filtered transactions to CSV or Excel  
- **Auto-Backup:** Transactions are backed up automatically

---

## Screenshots

### Dashboard Overview
![Dashboard](images/dashboard.png)

### Add Transaction
![Add Transaction](images/add_transaction.png)

### Filter & Summary
![Filter & Summary](images/filter_summary.png)

### Category Chart
![Category Chart](images/category_chart.png)


---

## Installation & Running

### Using Docker (Recommended)

**1️⃣ Build the Docker Image**

```bash
docker build -t autoledger-dark:latest .