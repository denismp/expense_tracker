#!/bin/bash

# Define variables
APP_NAME="ExpenseTracker"
PROJECT_DIR="$HOME/git/expense_tracker"
DIST_DIR="${PROJECT_DIR}/dist"
EXE_PATH="${DIST_DIR}/${APP_NAME}.exe"
CONDA_ENV="expense_tracker_env"
ICON_PATH="${PROJECT_DIR}/icons/icon.ico"
REQUIREMENTS_FILE="${PROJECT_DIR}/requirements-win.txt"
STATIC_DIR="${PROJECT_DIR}/static"
BUILD_DIR="${PROJECT_DIR}/build"
ENTITLEMENTS_FILE="entitlements.mac.plist"
TEMP_DIR="${PROJECT_DIR}/.temp_build_backup"

PYINSTALLER_CMD="pyinstaller --noconsole --onefile --windowed --name=${APP_NAME} \
  --icon=${ICON_PATH} \
  --add-data \"db.sqlite3;.\" \
  --add-data \"static;static\" \
  --add-data \"expense_tracker/templates;expense_tracker/templates\" \
  --add-data \"expense_tracker/apps/expenses/templates;expense_tracker/apps/expenses/templates\" \
  --add-data \"expense_tracker/apps/accounts/templates;expense_tracker/apps/accounts/templates\" \
  winmain.py"

echo "🔄 Activating Conda environment: ${CONDA_ENV}"
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate "${CONDA_ENV}" || { echo "❌ Failed to activate Conda env."; exit 1; }

echo "📦 Installing dependencies from requirements-win.txt..."
if [ -f "${REQUIREMENTS_FILE}" ]; then
    pip install -r "${REQUIREMENTS_FILE}" || { echo "❌ Failed to install dependencies."; exit 1; }
else
    echo "⚠️ requirements-win.txt not found at ${REQUIREMENTS_FILE}. Skipping dependency installation."
fi

echo "🛠️ Setting USE_POSTGRES=false"
export USE_POSTGRES=false

echo "📂 Collecting static files..."
cd "${PROJECT_DIR}" || { echo "❌ Failed to change to project directory: ${PROJECT_DIR}"; exit 1; }
python manage.py collectstatic --noinput || { echo "❌ collectstatic failed."; exit 1; }

echo "🧹 Cleaning old build artifacts..."

# Backup entitlements.mac.plist if it exists
mkdir -p "${TEMP_DIR}"
if [ -f "${BUILD_DIR}/${ENTITLEMENTS_FILE}" ]; then
    cp "${BUILD_DIR}/${ENTITLEMENTS_FILE}" "${TEMP_DIR}/"
fi

# Remove entire build directory
rm -rf "${BUILD_DIR}"

# Restore entitlements.mac.plist
mkdir -p "${BUILD_DIR}"
if [ -f "${TEMP_DIR}/${ENTITLEMENTS_FILE}" ]; then
    mv "${TEMP_DIR}/${ENTITLEMENTS_FILE}" "${BUILD_DIR}/"
fi
rm -rf "${TEMP_DIR}"

rm -f "${PROJECT_DIR}/${APP_NAME}.spec"
rm -rf "${DIST_DIR}/ExpenseTracker"

if [ ! -f "${ICON_PATH}" ]; then
    echo "❌ Error: Icon file not found at ${ICON_PATH}"
    exit 1
fi

echo "🚀 Building the app with PyInstaller..."
eval "${PYINSTALLER_CMD}"
if [ $? -ne 0 ]; then
    echo "❌ PyInstaller build failed."
    exit 1
fi

if [ ! -f "${EXE_PATH}" ]; then
    echo "❌ Error: ${EXE_PATH} not found."
    exit 1
fi

echo "✅ Windows executable created at: ${EXE_PATH}"
