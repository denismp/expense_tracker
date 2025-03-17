import os
import sys
import time
import threading
import webbrowser
import requests
import signal
from django.core.management import execute_from_command_line

# Flag to signal server shutdown
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
    """Handle the interrupt signal to shut down the server."""
    global shutdown_flag
    shutdown_flag = True
    print("Shutting down the server...")


if __name__ == '__main__':
    # Set up signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    # Start the server in a separate thread
    server_thread = threading.Thread(target=start_server)
    server_thread.start()

    # Wait for the server to be ready
    url = 'http://127.0.0.1:8000/'
    if wait_for_server(url):
        print("Server is ready!")
        open_browser()
        # Keep the main thread running until interrupted
        while not shutdown_flag:
            time.sleep(1)
        # Wait for the server thread to finish
        server_thread.join()
    else:
        print("Error: Server did not start within 30 seconds.")
        sys.exit(1)
