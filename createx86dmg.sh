#!/bin/bash

APP_NAME="ExpenseTracker"
PROJECT_DIR="$HOME/git/expense_tracker"
DIST_DIR="${PROJECT_DIR}/dist"
APP_PATH="${DIST_DIR}/${APP_NAME}.app"
DMG_PATH="${DIST_DIR}/${APP_NAME}.dmg"
TEMP_DIR="${DIST_DIR}/dmg_contents"
CONDA_ENV="expense_tracker_env"
ICON_PATH="${PROJECT_DIR}/icons/icon.icns"
MAC_DB_PATH="$HOME/Library/Application Support/ExpenseTracker/db.sqlite3"
ENTITLEMENTS_PLIST="entitlements.mac.plist"
BUILD_DIR="${PROJECT_DIR}/build"
ENTITLEMENTS_PATH="${BUILD_DIR}/${ENTITLEMENTS_PLIST}"
TEMP_ENTITLEMENTS_BACKUP="${PROJECT_DIR}/.entitlements_backup.plist"

PYINSTALLER_CMD="pyinstaller --windowed --noconsole \
  --onefile \
  --name=${APP_NAME} \
  --icon=${ICON_PATH} \
  --osx-bundle-identifier=com.denisputnam.expensetracker \
  --add-data \"db.sqlite3:.\" \
  --add-data \"static:static\" \
  --add-data \"staticfiles:staticfiles\" \
  --add-data \"expense_tracker/templates:expense_tracker/templates\" \
  --add-data \"expense_tracker/apps/expenses/templates:expense_tracker/apps/expenses/templates\" \
  --add-data \"expense_tracker/apps/accounts/templates:expense_tracker/apps/accounts/templates\" \
  mainx86.py"

echo "🔄 Activating Conda environment: ${CONDA_ENV}"
source /opt/anaconda3/etc/profile.d/conda.sh
conda activate "${CONDA_ENV}"

echo "🧹 Cleaning previous DBs..."
rm -f db.sqlite3
rm -f "${MAC_DB_PATH}"

echo "🧱 Running migrations..."
cd "${PROJECT_DIR}" || exit
python manage.py makemigrations || exit 1
python manage.py migrate || exit 1

echo "👤 Creating superuser..."
export DJANGO_SUPERUSER_USERNAME=admin
export DJANGO_SUPERUSER_EMAIL=denisputnam@gmail.com
export DJANGO_SUPERUSER_PASSWORD=${DB_PASSWORD}
python manage.py createsuperuser --noinput || exit 1

echo "📦 Collecting static files..."
python manage.py collectstatic --noinput || exit 1

echo "🧹 Cleaning old build artifacts..."

# Back up entitlements.mac.plist if it exists
if [ -f "${ENTITLEMENTS_PATH}" ]; then
    cp "${ENTITLEMENTS_PATH}" "${TEMP_ENTITLEMENTS_BACKUP}"
fi

# Remove the entire build directory
rm -rf "${BUILD_DIR}"
mkdir -p "${BUILD_DIR}"

# Restore entitlements.mac.plist if it was backed up
if [ -f "${TEMP_ENTITLEMENTS_BACKUP}" ]; then
    mv "${TEMP_ENTITLEMENTS_BACKUP}" "${ENTITLEMENTS_PATH}"
fi

rm -rf "${DIST_DIR}"
rm -f "${PROJECT_DIR}/${APP_NAME}.spec"

echo "🚀 Building .app with PyInstaller..."
eval "${PYINSTALLER_CMD}" || exit 1

echo "📁 Preparing .dmg folder..."
mkdir -p "${TEMP_DIR}"
cp -R "${APP_PATH}" "${TEMP_DIR}/"
ln -s /Applications "${TEMP_DIR}/Applications"

echo "💾 Creating DMG..."
hdiutil create -volname "${APP_NAME}" -srcfolder "${TEMP_DIR}" -ov -format UDZO -size 300m "${DMG_PATH}" || exit 1

echo "🧹 Cleaning up..."
rm -rf "${TEMP_DIR}"

echo "✅ DMG built: ${DMG_PATH}"
