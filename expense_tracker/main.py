import os
import sys
import time
import threading
import webbrowser
import requests
import signal

# macOS GUI activation using AppKit and Foundation
from AppKit import NSApplication, NSApplicationActivationPolicyRegular
from Foundation import NSRunLoop, NSDate

from django.core.management import execute_from_command_line

# Flag to control server shutdown
shutdown_flag = False


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
    # Handle Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    # Initialize macOS application context
    app = NSApplication.sharedApplication()
    app.setActivationPolicy_(NSApplicationActivationPolicyRegular)
    app.activateIgnoringOtherApps_(True)

    # Start the Django server in a background thread
    server_thread = threading.Thread(target=start_server)
    server_thread.start()

    # Wait until Django is up
    if wait_for_server("http://127.0.0.1:8000"):
        print("✅ Server is ready!")
        open_browser()

        # Enter the macOS run loop (keeps Dock icon and app state)
        run_loop = NSRunLoop.currentRunLoop()
        while not shutdown_flag:
            run_loop.runUntilDate_(NSDate.dateWithTimeIntervalSinceNow_(0.5))

        server_thread.join()
    else:
        print("❌ Error: Server did not start within 30 seconds.")
        sys.exit(1)
