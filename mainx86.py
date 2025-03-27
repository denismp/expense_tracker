import os
import sys
import time
import threading
import requests
import signal
import shutil
import traceback
import subprocess

from AppKit import (
    NSApplication, NSImage, NSApplicationActivationPolicyRegular,
    NSCriticalRequest, NSObject
)
from Foundation import NSLog

from django.core.management import execute_from_command_line

# Globals
ICON_PATH = os.path.join(os.path.dirname(sys.argv[0]), "icons/icon.icns")
delegate = None  # Keep reference to AppDelegate

LOG_DIR = os.path.expanduser("~/Library/Application Support/ExpenseTracker")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "output.log")


def log_error(msg):
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write("=== ERROR ===\n")
            f.write(msg + "\n")
            f.write(traceback.format_exc() + "\n")
    except Exception:
        pass


def ensure_writable_database():
    """Copy db.sqlite3 to user-writable location if bundled."""
    try:
        if getattr(sys, 'frozen', False):
            bundled_db_path = os.path.join(sys._MEIPASS, 'db.sqlite3')
            writable_db_path = os.path.join(LOG_DIR, 'db.sqlite3')

            if not os.path.exists(writable_db_path):
                print("📄 Copying db.sqlite3 to writable location...")
                shutil.copy2(bundled_db_path, writable_db_path)
            else:
                print("📂 Using existing writable database.")

            os.environ['DJANGO_DB_PATH'] = writable_db_path
    except Exception:
        log_error("Failed to ensure writable DB")


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
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expense_tracker.settings')
        execute_from_command_line(['manage.py', 'runserver', '127.0.0.1:8000', '--noreload'])
    except Exception:
        log_error("Failed to start Django server")
        force_quit()


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
    """Open the default browser to the app URL using macOS-safe call."""
    try:
        subprocess.run(["open", "http://127.0.0.1:8000"])
    except Exception:
        log_error("Failed to open browser")


if __name__ == '__main__':
    # Early launch marker for debugging
    try:
        with open("/tmp/expensetracker_start.log", "w") as f:
            f.write("✅ App reached entry point\n")
    except Exception:
        pass

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        ensure_writable_database()
        set_app_icon_and_delegate()

        server_thread = threading.Thread(target=start_server)
        server_thread.start()

        if wait_for_server("http://127.0.0.1:8000"):
            print("✅ Server is ready!")
            open_browser()
            NSApplication.sharedApplication().run()
        else:
            print("❌ Error: Server did not start within 30 seconds.")
            log_error("Server timeout")
            sys.exit(1)
    except Exception as e:
        log_error("Unhandled error in main" + e)
        force_quit()
