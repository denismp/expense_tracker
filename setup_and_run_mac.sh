#!/bin/bash

echo "🚀 Setting up expense_tracker on macOS..."

# Step 1: Ensure Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "⚠️ Homebrew not found! Installing..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Step 2: Install Python if not installed
if ! command -v python3 &> /dev/null; then
    echo "⚠️ Python3 not found! Installing..."
    brew install python
fi

# Step 3: Ensure pip is up-to-date
python3 -m ensurepip --default-pip
python3 -m pip install --upgrade pip

# Step 4: Install virtualenv if not installed
if ! command -v virtualenv &> /dev/null; then
    echo "⚠️ virtualenv not found! Installing..."
    python3 -m pip install virtualenv
fi

# Step 5: Create and activate virtual environment
echo "🔹 Setting up virtual environment..."
python3 -m venv expense_tracker_env
source expense_tracker_env/bin/activate

# Step 6: Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Step 7: Apply migrations
echo "⚙️ Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Step 8: Create a superuser (optional)
read -p "Do you want to create a superuser? (y/n): " create_superuser
if [[ $create_superuser == "y" ]]; then
    python manage.py createsuperuser
fi

# Step 9: Start the Django server
echo "🚀 Starting the Django server..."
python manage.py runserver

# Keep the virtual environment active
exec $SHELL