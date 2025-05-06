#!/bin/bash

# Step 0: Define paths and clean build directories
APP_NAME="ExpenseTracker"
PROJECT_DIR="$HOME/git/expense_tracker"
DIST_DIR="${PROJECT_DIR}/dist"
BUILD_DIR="${PROJECT_DIR}/build"
APP_PATH="${DIST_DIR}/${APP_NAME}.app"
DMG_PATH="${DIST_DIR}/${APP_NAME}.dmg"
TEMP_DIR="${DIST_DIR}/dmg_contents"
ICON_PATH="${PROJECT_DIR}/icons/icon.icns"
MAC_DB_PATH="$HOME/Library/Application Support/ExpenseTracker/db.sqlite3"
ENTITLEMENTS_PLIST="entitlements.mac.plist"
ENTITLEMENTS_PATH="${BUILD_DIR}/${ENTITLEMENTS_PLIST}"
TEMP_ENTITLEMENTS_BACKUP="${PROJECT_DIR}/.entitlements_backup.plist"
CONDA_ENV="expense_tracker_env"

echo "🧹 Cleaning previous build artifacts..."
# Backup entitlements file if it exists
if [ -f "${ENTITLEMENTS_PATH}" ]; then
    cp "${ENTITLEMENTS_PATH}" "${TEMP_ENTITLEMENTS_BACKUP}"
fi

rm -rf "${DIST_DIR}" "${BUILD_DIR}" "${PROJECT_DIR}/${APP_NAME}.spec"
mkdir -p "${DIST_DIR}" "${BUILD_DIR}"

# Restore entitlements file if it was backed up
if [ -f "${TEMP_ENTITLEMENTS_BACKUP}" ]; then
    mv "${TEMP_ENTITLEMENTS_BACKUP}" "${ENTITLEMENTS_PATH}"
fi

# Step 1: Activate the Conda environment
echo "🔄 Activating Conda environment: ${CONDA_ENV}"
source /opt/anaconda3/etc/profile.d/conda.sh
conda activate "${CONDA_ENV}" || { echo "❌ Failed to activate Conda environment."; exit 1; }

# Step 2: Set environment variables
echo "🛠️ Setting USE_POSTGRES=false"
export USE_POSTGRES=false

# Step 3: Reset DB and run migrations
echo "🧹 Removing old DBs..."
rm -f db.sqlite3 "${MAC_DB_PATH}"

echo "🧱 Running Django migrations..."
cd "${PROJECT_DIR}" || exit
python manage.py makemigrations || exit 1
python manage.py migrate || exit 1

echo "👤 Creating superuser..."
export DJANGO_SUPERUSER_USERNAME=admin
export DJANGO_SUPERUSER_EMAIL=denisputnam@gmail.com
export DJANGO_SUPERUSER_PASSWORD=${DB_PASSWORD}
python manage.py createsuperuser --noinput || exit 1

# Step 4: Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput || exit 1

# Step 5: Validate icon exists
if [ ! -f "${ICON_PATH}" ]; then
    echo "❌ Icon file not found at ${ICON_PATH}."
    exit 1
fi

# Step 6: Build .app using PyInstaller
PYINSTALLER_CMD="pyinstaller --windowed --noconsole --onefile \
  --name=${APP_NAME} \
  --icon=${ICON_PATH} \
  --osx-bundle-identifier=com.denisputnam.expensetracker \
  --add-data \"db.sqlite3:.\" \
  --add-data \".env:.env\" \
  --add-data \"static:static\" \
  --add-data \"staticfiles:staticfiles\" \
  --add-data \"expense_tracker/templates:expense_tracker/templates\" \
  --add-data \"expense_tracker/apps/expenses/templates:expense_tracker/apps/expenses/templates\" \
  --add-data \"expense_tracker/apps/accounts/templates:expense_tracker/apps/accounts/templates\" \
  mainx86.py"

echo "🚀 Building .app with PyInstaller..."
eval "${PYINSTALLER_CMD}" || exit 1

# Step 7: Verify .app was built
if [ ! -d "${APP_PATH}" ]; then
    echo "❌ Build failed: ${APP_PATH} not found."
    exit 1
fi

# Step 8: Prepare DMG contents
echo "📁 Preparing .dmg folder..."
mkdir -p "${TEMP_DIR}"
cp -R "${APP_PATH}" "${TEMP_DIR}/" || exit 1
ln -s /Applications "${TEMP_DIR}/Applications" || exit 1

# Step 9: Build DMG
echo "💾 Creating DMG..."
hdiutil create -volname "${APP_NAME}" -srcfolder "${TEMP_DIR}" -ov -format UDZO -size 300m "${DMG_PATH}" || exit 1

# Step 10: Cleanup
echo "🧹 Cleaning up temporary files..."
rm -rf "${TEMP_DIR}"

echo "✅ DMG built successfully: ${DMG_PATH}"