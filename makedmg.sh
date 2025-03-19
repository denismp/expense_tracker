#!/bin/bash

# Define variables
APP_NAME="ExpenseTracker"                                 # Name of your application
APP_PATH="/Users/denisputnam/git/expense_tracker/dist/${APP_NAME}.app"  # Path to the .app bundle
DMG_NAME="${APP_NAME}.dmg"                               # Name of the output .dmg file
DMG_PATH="/Users/denisputnam/git/expense_tracker/dist/${DMG_NAME}"      # Path to the .dmg file
TEMP_DIR="/Users/denisputnam/git/expense_tracker/dist/dmg_contents"     # Temporary directory for .dmg contents
IDENTITY="Developer ID Application: Denis Putnam (2368694WQF)"           # Your Developer ID certificate
APPLE_ID="denisputnam@verizon.net"                     # Your Apple ID email
APP_PASSWORD="mbla-xgml-oeja-ptna"                # Your app-specific password
BUNDLE_ID="com.denisputnam.expense-tracker"              # Unique bundle identifier

# Step 1: Sign the .app bundle
echo "Signing the .app bundle..."
codesign --force --sign "${IDENTITY}" --options runtime "${APP_PATH}"
if [ $? -ne 0 ]; then
    echo "Error: Signing failed. Check your Developer ID certificate."
    exit 1
fi
codesign --verify --verbose "${APP_PATH}"  # Verify the signing

# Step 2: Create a temporary directory for .dmg contents
echo "Creating temporary directory..."
mkdir -p "${TEMP_DIR}"

# Step 3: Copy the .app bundle to the temporary directory
echo "Copying .app bundle to temporary directory..."
cp -R "${APP_PATH}" "${TEMP_DIR}/"
if [ $? -ne 0 ]; then
    echo "Error: Failed to copy .app bundle."
    exit 1
fi

# Step 4: Create the .dmg file
echo "Creating .dmg file..."
hdiutil create -volname "${APP_NAME}" -srcfolder "${TEMP_DIR}" -ov -format UDZO "${DMG_PATH}"
if [ $? -ne 0 ]; then
    echo "Error: Failed to create .dmg file."
    exit 1
fi

# Step 5: Clean up the temporary directory
echo "Cleaning up..."
rm -rf "${TEMP_DIR}"

# Step 6: Submit the .dmg for notarization
echo "Submitting .dmg for notarization..."
NOTARIZE_OUTPUT=$(xcrun altool --notarize-app --primary-bundle-id "${BUNDLE_ID}" \
    --username "${APPLE_ID}" --password "${APP_PASSWORD}" --file "${DMG_PATH}" 2>&1)
if [ $? -ne 0 ]; then
    echo "Error: Notarization submission failed."
    echo "$NOTARIZE_OUTPUT"
    exit 1
fi

# Extract the UUID from the notarization output
UUID=$(echo "$NOTARIZE_OUTPUT" | grep "RequestUUID" | awk '{print $3}')
if [ -z "$UUID" ]; then
    echo "Error: Could not retrieve notarization UUID."
    echo "$NOTARIZE_OUTPUT"
    exit 1
fi
echo "Notarization submitted. Request UUID: $UUID"

# Note: Notarization is asynchronous. You need to manually check the status and staple later.
echo "Wait for notarization to complete (may take minutes to hours)."
echo "To check status, run:"
echo "xcrun altool --notarization-info $UUID --username \"${APPLE_ID}\" --password \"${APP_PASSWORD}\""
echo "Once status is 'success', staple the ticket with:"
echo "xcrun stapler staple \"${DMG_PATH}\""

echo "Script completed. After notarization succeeds, test the .dmg on another Mac."