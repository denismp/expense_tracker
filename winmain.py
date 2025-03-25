import atexit
import io
import os
import sys
import threading
import traceback
import webbrowser

try:
    import django
    from django.core.management import call_command
except ImportError:
    django = None

try:
    import pystray
    from PIL import Image
except ImportError:
    pystray = None


def ensure_writable_database():
    """
    Ensure the database is writable by copying it to the user's AppData folder
    if needed.

    (Implementation details omitted for brevity; assume this function is
    defined elsewhere in the module.)
    """
    pass  # Placeholder for actual implementation


def log_error(exception):
    """Log exceptions to 'error.log' in the %APPDATA%/ExpenseTracker folder."""
    try:
        log_dir = os.path.join(os.getenv("APPDATA"), "ExpenseTracker")
        os.makedirs(log_dir, exist_ok=True)
        error_log_path = os.path.join(log_dir, "error.log")
        with open(error_log_path, "a", encoding="utf-8",
                  errors="replace") as f:
            f.write(f"Exception: {exception}\n")
            traceback.print_exc(file=f)
    except Exception:
        pass


def main():
    # Redirect stdout and stderr to UTF-8 encoded output.log
    log_dir = os.path.join(os.getenv("APPDATA", "."), "ExpenseTracker")
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "output.log")

    try:
        log_file = open(
            log_path, "a", buffering=1, encoding="utf-8", errors="replace"
        )
        sys.stdout = io.TextIOWrapper(
            log_file.buffer, encoding="utf-8", line_buffering=True
        )
        sys.stderr = sys.stdout
        atexit.register(log_file.close)
    except Exception as e:
        log_error(e)

    # App logic starts here
    ensure_writable_database()

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "expense_tracker.settings")
    if django is not None:
        django.setup()

    server_thread = threading.Thread(
        target=lambda: call_command(
            "runserver", "127.0.0.1:8000", "--noreload"
        ),
        daemon=True
    )
    server_thread.start()

    webbrowser.open("http://127.0.0.1:8000")

    if pystray is not None:
        icon_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "icon.ico"
        )
        try:
            tray_image = Image.open(icon_path)
        except Exception:
            tray_image = None

        def on_quit(icon, item):
            icon.stop()

        menu = pystray.Menu(pystray.MenuItem("Quit", on_quit))
        tray_icon = pystray.Icon(
            "ExpenseTracker", tray_image, "ExpenseTracker", menu
        )
        tray_icon.run()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log_error(e)
