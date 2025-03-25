#!/bin/bash

# Define variables
APP_NAME="ExpenseTracker"
#PROJECT_DIR="/Users/denisputnam/git/expense_tracker"
PROJECT_DIR="${HOME}/git/expense_tracker"
APP_PATH="${PROJECT_DIR}/dist/${APP_NAME}.app"
DMG_NAME="${APP_NAME}.dmg"
DMG_PATH="${PROJECT_DIR}/dist/${DMG_NAME}"
TEMP_DIR="${PROJECT_DIR}/dist/dmg_contents"
CONDA_ENV="expense_tracker_env"
ICON_PATH="${PROJECT_DIR}/icons/icon.icns"

PYINSTALLER_CMD="pyinstaller --onefile --windowed --name=ExpenseTracker \
  --osx-bundle-identifier=com.denisputnam.expense-tracker \
  --icon=${ICON_PATH} \
  --add-data \"static:static\" \
  --add-data \"expense_tracker/templates:expense_tracker/templates\" \
  --add-data \"expense_tracker/apps/expenses/templates:expense_tracker/apps/expenses/templates\" \
  --add-data \"expense_tracker/apps/accounts/templates:expense_tracker/apps/accounts/templates\" \
  --add-data \"db.sqlite3:.\" \
  main.py"

# Step 1: Activate the Conda environment
echo "🔄 Activating Conda environment: ${CONDA_ENV}"
source /Users/denisputnam/opt/anaconda3/bin/activate "${CONDA_ENV}"
if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to activate Conda environment."
    exit 1
fi

# Step 2: Set environment variables
echo "🛠️ Setting USE_POSTGRES=false"
export USE_POSTGRES=false

# Step 3: Run collectstatic to gather static files
echo "📂 Collecting static files..."
cd "${PROJECT_DIR}" || exit
python manage.py collectstatic --noinput
if [ $? -ne 0 ]; then
    echo "❌ Error: collectstatic failed."
    exit 1
fi

# Step 4: Clean previous build artifacts
echo "🗑️ Cleaning old build artifacts..."
rm -rf "${PROJECT_DIR}/dist"
rm -rf "${PROJECT_DIR}/build/ExpenseTracker"

# Step 5: Validate the icon file exists
if [ ! -f "${ICON_PATH}" ]; then
    echo "❌ Error: Icon file not found at ${ICON_PATH}. Ensure it exists."
    exit 1
fi

# Step 6: Build the app with PyInstaller
echo "🚀 Building the app with PyInstaller..."
eval "${PYINSTALLER_CMD}"
if [ $? -ne 0 ]; then
    echo "❌ Error: PyInstaller build failed."
    exit 1
fi

# Step 7: Ensure the .app bundle exists
if [ ! -d "${APP_PATH}" ]; then
    echo "❌ Error: ${APP_PATH} not found. PyInstaller may have failed."
    exit 1
fi

# Step 8: Unmount any previous disk images
if mount | grep -q "/Volumes/${APP_NAME}"; then
    echo "🔄 Unmounting existing DMG..."
    hdiutil detach -force "/Volumes/${APP_NAME}"
fi

# Step 9: Delete existing .dmg file if present
if [ -f "${DMG_PATH}" ]; then
    echo "🗑️ Removing old .dmg file..."
    rm -f "${DMG_PATH}"
fi

# Step 10: Create a temporary directory for .dmg contents
echo "📁 Creating temporary directory..."
mkdir -p "${TEMP_DIR}"

# Step 11: Copy the .app bundle to the temporary directory
echo "📂 Copying .app bundle to temporary directory..."
cp -R "${APP_PATH}" "${TEMP_DIR}/"
if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to copy .app bundle."
    exit 1
fi

# Step 12: Create a symbolic link to the Applications folder
echo "🔗 Creating Applications shortcut..."
ln -s /Applications "${TEMP_DIR}/Applications"
if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to create Applications shortcut."
    exit 1
fi

# Step 13: Create the .dmg file with increased space
echo "💾 Creating .dmg file..."
hdiutil create -volname "${APP_NAME}" -srcfolder "${TEMP_DIR}" -ov -format UDZO -size 300m "${DMG_PATH}"
if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to create .dmg file."
    exit 1
fi

# Step 14: Clean up the temporary directory
echo "🧹 Cleaning up..."
rm -rf "${TEMP_DIR}"

echo "✅ Script completed successfully! The .dmg file is created without signing or notarization."
echo "📂 You can find it at: ${DMG_PATH}"