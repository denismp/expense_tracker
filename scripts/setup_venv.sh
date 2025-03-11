#!/bin/bash

echo "🛠️ Setting up virtual environment inside the packaged app..."

# Get the absolute directory of this script
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Check if running in development (repo) or a packaged app
if [[ -d "$SCRIPT_DIR/../electron-app" ]]; then
    # Development Mode: Virtual environment is inside electron-app/
    VENV_DIR="$SCRIPT_DIR/../electron-app/venv"
    REQUIREMENTS_FILE="$SCRIPT_DIR/../requirements.txt"
else
    # Packaged Mode: Virtual environment is inside /Contents/Resources/venv
    VENV_DIR="$SCRIPT_DIR/../venv"
    REQUIREMENTS_FILE="$SCRIPT_DIR/../requirements.txt"
fi

echo "📂 Virtual Environment Directory: $VENV_DIR"

# Ensure Python is installed
if ! command -v python3 &>/dev/null; then
    echo "❌ Python3 is not installed. Please install it and rerun this script."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [[ ! -d "$VENV_DIR" ]]; then
    echo "📂 Creating virtual environment at $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
    if [[ $? -ne 0 ]]; then
        echo "❌ Failed to create virtual environment. Exiting."
        exit 1
    fi
    echo "✅ Virtual environment created."
else
    echo "🔄 Virtual environment already exists."
fi

# Ensure activation script exists
if [[ ! -f "$VENV_DIR/bin/activate" ]]; then
    echo "❌ Virtual environment setup failed: Activation script not found at $VENV_DIR/bin/activate."
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Ensure pip is installed
if ! command -v pip &>/dev/null; then
    echo "❌ pip is not installed in the virtual environment. Installing pip..."
    python3 -m ensurepip --default-pip
fi

# Install dependencies
if [[ -f "$REQUIREMENTS_FILE" ]]; then
    echo "📦 Installing dependencies from $REQUIREMENTS_FILE..."
    pip install --upgrade pip setuptools wheel
    pip install -r "$REQUIREMENTS_FILE"
    if [[ $? -ne 0 ]]; then
        echo "❌ Failed to install dependencies. Exiting."
        exit 1
    fi
    echo "🚀 Dependencies installed successfully."
else
    echo "⚠️ Warning: requirements.txt not found at $REQUIREMENTS_FILE. Skipping dependency installation."
fi

echo "✅ Virtual environment setup complete."