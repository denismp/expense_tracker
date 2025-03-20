#!/bin/bash

# Define variables
APP_NAME="ExpenseTracker"
APP_PATH="/Users/denisputnam/git/expense_tracker/dist/${APP_NAME}.app"
DMG_NAME="${APP_NAME}.dmg"
DMG_PATH="/Users/denisputnam/git/expense_tracker/dist/${DMG_NAME}"
TEMP_DIR="/Users/denisputnam/git/expense_tracker/dist/dmg_contents"
CONDA_ENV="expense_tracker_env"
PYINSTALLER_CMD="pyinstaller --onedir --windowed --name=ExpenseTracker --osx-bundle-identifier=com.denisputnam.expense-tracker --add-data \"static:static\" --add-data \"expense_tracker/templates:expense_tracker/templates\" --add-data \"expense_tracker/apps/expenses/templates:expense_tracker/apps/expenses/templates\" --add-data \"expense_tracker/apps/accounts/templates:expense_tracker/apps/accounts/templates\" main.py"

# Step 1: Activate the Conda environment
echo "Activating Conda environment: ${CONDA_ENV}"
source /Users/denisputnam/opt/anaconda3/bin/activate "${CONDA_ENV}"
if [ $? -ne 0 ]; then
    echo "Error: Failed to activate Conda environment."
    exit 1
fi

# Step 2: Set the environment variable
echo "Setting USE_POSTGRES=false"
export USE_POSTGRES=false

# Step 3: Build the app with PyInstaller
echo "Building the app with PyInstaller..."
eval "${PYINSTALLER_CMD}"
if [ $? -ne 0 ]; then
    echo "Error: PyInstaller build failed."
    exit 1
fi

# Step 4: Create a temporary directory for .dmg contents
echo "Creating temporary directory..."
mkdir -p "${TEMP_DIR}"

# Step 5: Copy the .app bundle to the temporary directory
echo "Copying .app bundle to temporary directory..."
cp -R "${APP_PATH}" "${TEMP_DIR}/"
if [ $? -ne 0 ]; then
    echo "Error: Failed to copy .app bundle."
    exit 1
fi

# Step 6: Create a symbolic link to the Applications folder
echo "Creating Applications shortcut..."
ln -s /Applications "${TEMP_DIR}/Applications"
if [ $? -ne 0 ]; then
    echo "Error: Failed to create Applications shortcut."
    exit 1
fi

# Step 7: Create the .dmg file
echo "Creating .dmg file..."
hdiutil create -volname "${APP_NAME}" -srcfolder "${TEMP_DIR}" -ov -format UDZO "${DMG_PATH}"
if [ $? -ne 0 ]; then
    echo "Error: Failed to create .dmg file."
    exit 1
fi

# Step 8: Clean up the temporary directory
echo "Cleaning up..."
rm -rf "${TEMP_DIR}"

echo "Script completed. The .dmg file is created without signing or notarization."
echo "You can find it at: ${DMG_PATH}"