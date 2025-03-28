import os
import sys
import time
import threading
import webbrowser
import requests
import signal
import shutil

from AppKit import (
    NSApplication, NSImage, NSApplicationActivationPolicyRegular,
    NSCriticalRequest, NSObject
)
from Foundation import NSLog

from django.core.management import execute_from_command_line

# Globals
ICON_PATH = os.path.join(os.path.dirname(sys.argv[0]), "icons/icon.icns")
delegate = None  # Keep reference to AppDelegate


def ensure_writable_database():
    """Copy db.sqlite3 to user-writable location if bundled."""
    if getattr(sys, 'frozen', False):
        bundled_db_path = os.path.join(sys._MEIPASS, 'db.sqlite3')
        writable_db_path = os.path.expanduser('~/Library/Application Support/ExpenseTracker/db.sqlite3')
        os.makedirs(os.path.dirname(writable_db_path), exist_ok=True)

        if not os.path.exists(writable_db_path):
            print("📄 Copying db.sqlite3 to writable location...")
            shutil.copy2(bundled_db_path, writable_db_path)
        else:
            print("📂 Using existing writable database.")

        os.environ['DJANGO_DB_PATH'] = writable_db_path


def force_quit():
    """Forcefully terminate the app and all threads using SIGKILL."""
    print("🛑 Force quitting application with SIGKILL...")
    time.sleep(0.1)
    os.kill(os.getpid(), signal.SIGKILL)


def signal_handler(signum, frame):
    """Handle SIGINT and SIGTERM by triggering force_quit."""
    force_quit()


class AppDelegate(NSObject):
    def applicationShouldTerminate_(self, sender):
        """Handle Dock 'Quit' event."""
        NSLog("🍎 Dock 'Quit' clicked — initiating force quit.")
        force_quit()
        return 0  # Prevent default quit behavior


def set_app_icon_and_delegate():
    """Setup NSApp, icon, bounce, and delegate for Dock quit handling."""
    global delegate

    app = NSApplication.sharedApplication()
    app.setActivationPolicy_(NSApplicationActivationPolicyRegular)

    delegate = AppDelegate.alloc().init()
    app.setDelegate_(delegate)

    if os.path.exists(ICON_PATH):
        image = NSImage.alloc().initWithContentsOfFile_(ICON_PATH)
        app.setApplicationIconImage_(image)

    bounce_id = app.requestUserAttention_(NSCriticalRequest)

    def stop_bounce():
        time.sleep(2)
        app.cancelUserAttentionRequest_(bounce_id)

    threading.Thread(target=stop_bounce, daemon=True).start()
    app.finishLaunching()


def start_server():
    """Start the Django server in a thread."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expense_tracker.settings')
    execute_from_command_line(['manage.py', 'runserver', '8000', '--noreload'])


def wait_for_server(url, timeout=30):
    """Wait for the server to be ready."""
    start = time.time()
    while True:
        try:
            requests.get(url)
            return True
        except requests.ConnectionError:
            pass
        if time.time() - start > timeout:
            return False
        time.sleep(1)


def open_browser():
    """Open the default browser to the app URL."""
    webbrowser.open('http://127.0.0.1:8000')


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    ensure_writable_database()
    set_app_icon_and_delegate()

    server_thread = threading.Thread(target=start_server)
    server_thread.start()

    if wait_for_server("http://127.0.0.1:8000"):
        print("✅ Server is ready!")
        open_browser()

        # Start macOS native event loop
        NSApplication.sharedApplication().run()
    else:
        print("❌ Error: Server did not start within 30 seconds.")
        sys.exit(1)
