#!/bin/bash

# ------------------ Theme selection ------------------
# Parameter: ./run_autoledger.sh [light|dark|auto]
param=${1:-auto}
theme="light"

if [[ "$param" == "auto" ]]; then
    # Auto-detect macOS theme
    if [[ "$(uname)" == "Darwin" ]]; then
        result=$(defaults read -g AppleInterfaceStyle 2>/dev/null)
        if [[ "$result" == "Dark" ]]; then
            theme="dark"
        fi
    fi
    # Windows fallback (optional)
    if [[ "$(uname -s)" == *"MINGW"* || "$(uname -s)" == *"CYGWIN"* ]]; then
        theme="light"
    fi
else
    # Manual override
    if [[ "$param" == "dark" ]]; then
        theme="dark"
    elif [[ "$param" == "light" ]]; then
        theme="light"
    else
        echo "Invalid parameter. Using auto-detect."
    fi
fi

# ------------------ Choose config ------------------
if [[ "$theme" == "dark" ]]; then
    config=".streamlit/config_dark.toml"
else
    config=".streamlit/config_light.toml"
fi

echo "Launching AutoLedger in $theme mode..."
export STREAMLIT_CONFIG=$config

# ------------------ Run Streamlit ------------------
streamlit run app/main.py
