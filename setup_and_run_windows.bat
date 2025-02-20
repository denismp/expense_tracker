@echo off
echo 🚀 Setting up expense_tracker on Windows...

:: Step 1: Ensure Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ⚠️ Python not found! Please install Python first.
    exit /b
)

:: Step 2: Install pip if not found
python -m ensurepip --default-pip
python -m pip install --upgrade pip

:: Step 3: Install virtualenv if not installed
where virtualenv >nul 2>nul
if %errorlevel% neq 0 (
    echo ⚠️ virtualenv not found! Installing...
    python -m pip install virtualenv
)

:: Step 4: Create virtual environment
echo 🔹 Setting up virtual environment...
python -m venv expense_tracker_env

:: Step 5: Activate virtual environment
call expense_tracker_env\Scripts\activate

:: Step 6: Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt

:: Step 7: Apply migrations
echo ⚙️ Running database migrations...
python manage.py makemigrations
python manage.py migrate

:: Step 8: Create a superuser (optional)
set /p create_superuser="Do you want to create a superuser? (y/n): "
if /I "%create_superuser%"=="y" (
    python manage.py createsuperuser
)

:: Step 9: Start the Django server
echo 🚀 Starting the Django server...
python manage.py runserver

:: Keep the virtual environment active
cmd /k