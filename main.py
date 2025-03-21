import os
import sys
import time
import threading
import webbrowser
import requests
import signal
import shutil
# import pathlib

# macOS GUI activation using AppKit and Foundation
from AppKit import (
    NSApplication, NSImage, NSApplicationActivationPolicyRegular,
    NSCriticalRequest
)
from Foundation import NSRunLoop, NSDate

from django.core.management import execute_from_command_line

# Path to the icon file (relative to app bundle or source dir)
ICON_PATH = os.path.join(os.path.dirname(sys.argv[0]), "icons/icon.icns")

# Flag to control server shutdown
shutdown_flag = False


def ensure_writable_database():
    """If bundled, copy db.sqlite3 from app bundle to user's Library folder."""
    if getattr(sys, 'frozen', False):
        # Bundled db path inside the PyInstaller package
        bundled_db_path = os.path.join(sys._MEIPASS, 'db.sqlite3')
        writable_db_path = os.path.expanduser('~/Library/Application Support/ExpenseTracker/db.sqlite3')

        # Ensure target directory exists
        os.makedirs(os.path.dirname(writable_db_path), exist_ok=True)

        # Copy only if it doesn't already exist
        if not os.path.exists(writable_db_path):
            print("📄 Copying db.sqlite3 to writable location...")
            shutil.copy2(bundled_db_path, writable_db_path)
        else:
            print("📂 Using existing writable database.")

        # Tell Django to use the writable copy
        os.environ['DJANGO_DB_PATH'] = writable_db_path


def set_app_icon():
    """Ensure the application icon appears in the Dock and stops bouncing."""
    app = NSApplication.sharedApplication()
    app.setActivationPolicy_(NSApplicationActivationPolicyRegular)

    # Set custom icon if available
    if os.path.exists(ICON_PATH):
        image = NSImage.alloc().initWithContentsOfFile_(ICON_PATH)
        app.setApplicationIconImage_(image)

    # Bounce to grab attention, then stop it
    bounce_id = app.requestUserAttention_(NSCriticalRequest)

    def stop_bounce():
        time.sleep(2)
        app.cancelUserAttentionRequest_(bounce_id)

    threading.Thread(target=stop_bounce, daemon=True).start()
    app.finishLaunching()


def start_server():
    """Start the Django development server."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expense_tracker.settings')
    execute_from_command_line(['manage.py', 'runserver', '8000', '--noreload'])


def wait_for_server(url, timeout=30):
    """Wait until the server is ready by checking the URL."""
    start_time = time.time()
    while True:
        try:
            requests.get(url)
            return True
        except requests.ConnectionError:
            pass
        if time.time() - start_time > timeout:
            return False
        time.sleep(1)


def open_browser():
    """Open the default web browser to the server URL."""
    webbrowser.open('http://127.0.0.1:8000')


def signal_handler(signum, frame):
    """Gracefully handle termination."""
    global shutdown_flag
    shutdown_flag = True
    print("Shutting down the server...")


if __name__ == '__main__':
    # Catch Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    # Prepare writable database
    ensure_writable_database()

    # Set up macOS icon and app state
    set_app_icon()

    # Start Django server in background
    server_thread = threading.Thread(target=start_server)
    server_thread.start()

    # Wait for server then open browser
    if wait_for_server("http://127.0.0.1:8000"):
        print("✅ Server is ready!")
        open_browser()

        # Enter macOS run loop to keep app "alive"
        run_loop = NSRunLoop.currentRunLoop()
        while not shutdown_flag:
            run_loop.runUntilDate_(NSDate.dateWithTimeIntervalSinceNow_(0.5))

        server_thread.join()
    else:
        print("❌ Error: Server did not start within 30 seconds.")
        sys.exit(1)
