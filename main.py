import os
import sys
import time
import threading
import webbrowser
import requests
import signal
import shutil

# macOS GUI activation using AppKit and Foundation
from AppKit import (
    NSApplication, NSImage, NSApplicationActivationPolicyRegular,
    NSCriticalRequest, NSObject
)
from Foundation import NSRunLoop, NSDate, NSLog

from django.core.management import execute_from_command_line

# Path to the icon file (relative to app bundle or source dir)
ICON_PATH = os.path.join(os.path.dirname(sys.argv[0]), "icons/icon.icns")

# Flag to control shutdown loop
shutdown_flag = False


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


class AppDelegate(NSObject):
    def applicationShouldTerminate_(self, sender):
        """Intercept Dock → Quit and forcefully shut down."""
        NSLog("🍎 Dock 'Quit' clicked — initiating force quit.")
        force_quit()
        return 0  # Prevent normal exit


def set_app_icon():
    """Set app icon and stop bounce animation."""
    app = NSApplication.sharedApplication()
    app.setActivationPolicy_(NSApplicationActivationPolicyRegular)

    # Attach delegate for Dock quit handling
    delegate = AppDelegate.alloc().init()
    app.setDelegate_(delegate)

    if os.path.exists(ICON_PATH):
        image = NSImage.alloc().initWithContentsOfFile_(ICON_PATH)
        app.setApplicationIconImage_(image)

    # Bounce briefly, then stop
    bounce_id = app.requestUserAttention_(NSCriticalRequest)

    def stop_bounce():
        time.sleep(2)
        app.cancelUserAttentionRequest_(bounce_id)

    threading.Thread(target=stop_bounce, daemon=True).start()
    app.finishLaunching()


def start_server():
    """Start Django server."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expense_tracker.settings')
    execute_from_command_line(['manage.py', 'runserver', '8000', '--noreload'])


def wait_for_server(url, timeout=30):
    """Ping server until it responds or timeout."""
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
    """Open the app in the default browser."""
    webbrowser.open('http://127.0.0.1:8000')


def signal_handler(signum, frame):
    """Handle OS signals like Ctrl+C and SIGTERM."""
    force_quit()


def force_quit():
    """Forcefully terminate app and all threads."""
    global shutdown_flag
    shutdown_flag = True
    print("🛑 Force quitting application...")
    time.sleep(0.5)
    os._exit(0)  # Terminate all threads and subprocesses


if __name__ == '__main__':
    # Handle SIGINT (Ctrl+C) and SIGTERM
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    ensure_writable_database()
    set_app_icon()

    server_thread = threading.Thread(target=start_server)
    server_thread.start()

    if wait_for_server("http://127.0.0.1:8000"):
        print("✅ Server is ready!")
        open_browser()

        run_loop = NSRunLoop.currentRunLoop()
        while not shutdown_flag:
            run_loop.runUntilDate_(NSDate.dateWithTimeIntervalSinceNow_(0.5))

        server_thread.join()
        force_quit()
    else:
        print("❌ Error: Server did not start within 30 seconds.")
        sys.exit(1)
