import atexit
import ctypes
import io
import os
import shutil
import sys
import threading
import time
import traceback
import webbrowser
import tkinter as tk

try:
    import django
    from django.core.management import call_command
except ImportError:
    django = None

try:
    import psutil
    import pystray
    from PIL import Image
except ImportError:
    pystray = None
    psutil = None

tray_icon = None  # Global reference for access in on_quit()


def ensure_writable_database():
    """
    Ensure the database is writable by copying it to the user's AppData folder
    if needed.
    """
    try:
        if getattr(sys, "frozen", False):
            appdata_dir = os.getenv("APPDATA", os.path.expanduser("~"))
            db_dir = os.path.join(appdata_dir, "ExpenseTracker")
            os.makedirs(db_dir, exist_ok=True)
            db_path = os.path.join(db_dir, "db.sqlite3")

            if not os.path.exists(db_path):
                bundle_dir = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
                template_db = os.path.join(bundle_dir, "db.sqlite3")
                if os.path.exists(template_db):
                    shutil.copyfile(template_db, db_path)

            os.environ["DJANGO_DB_PATH"] = db_path
    except Exception as e:
        log_error(e)


def log_error(exception):
    """Log exceptions to 'error.log' in the %APPDATA%/ExpenseTracker folder."""
    try:
        log_dir = os.path.join(os.getenv("APPDATA"), "ExpenseTracker")
        os.makedirs(log_dir, exist_ok=True)
        error_log_path = os.path.join(log_dir, "error.log")
        with open(error_log_path, "a", encoding="utf-8", errors="replace") as f:
            f.write(f"Exception: {exception}\n")
            traceback.print_exc(file=f)
    except Exception:
        pass


def redirect_output_to_log():
    """Redirect stdout and stderr to UTF-8 encoded output.log."""
    log_dir = os.path.join(os.getenv("APPDATA", "."), "ExpenseTracker")
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "output.log")

    try:
        log_file = open(log_path, "a", buffering=1, encoding="utf-8", errors="replace")
        sys.stdout = io.TextIOWrapper(
            log_file.buffer, encoding="utf-8", line_buffering=True
        )
        sys.stderr = sys.stdout
        atexit.register(log_file.close)
    except Exception as e:
        log_error(e)


def on_quit():
    """Handle quit from tray or taskbar: kill Django thread and self."""
    try:
        if tray_icon:
            tray_icon.stop()
    except Exception:
        pass

    try:
        current_pid = os.getpid()
        proc_name = os.path.basename(sys.executable)
        for proc in psutil.process_iter(["pid", "name"]):
            if proc.info["pid"] != current_pid and proc.info["name"] == proc_name:
                proc.kill()
    except Exception:
        pass

    os._exit(0)


def create_taskbar_window():
    """Create a hidden taskbar window using Tkinter to appear on Windows taskbar."""
    try:
        app_id = "com.expensetracker.app"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    except Exception:
        pass

    root = tk.Tk()
    root.title("ExpenseTracker")
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")
    if os.path.exists(icon_path):
        try:
            root.iconbitmap(icon_path)
        except Exception:
            pass
    root.protocol("WM_DELETE_WINDOW", on_quit)
    root.iconify()  # Minimize to taskbar
    return root


def create_tray_icon():
    """Create a system tray icon with Quit option."""
    global tray_icon
    if pystray is None:
        return

    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")
    try:
        tray_image = Image.open(icon_path)
    except Exception:
        tray_image = None

    menu = pystray.Menu(pystray.MenuItem("Quit", lambda icon, item: on_quit()))
    tray_icon = pystray.Icon("ExpenseTracker", tray_image, "ExpenseTracker", menu)
    tray_icon.run()


def main():
    redirect_output_to_log()
    ensure_writable_database()

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "expense_tracker.settings")
    if django is not None:
        django.setup()

    # Override DB path from environment if set
    db_path = os.environ.get("DJANGO_DB_PATH")
    if db_path:
        from django.conf import settings

        settings.DATABASES["default"]["NAME"] = db_path

    server_thread = threading.Thread(
        target=lambda: call_command("runserver", "127.0.0.1:8000", "--noreload"),
        daemon=True,
    )
    server_thread.start()

    webbrowser.open("http://127.0.0.1:8000")

    taskbar_root = create_taskbar_window()

    tray_thread = threading.Thread(target=create_tray_icon, daemon=True)
    tray_thread.start()

    try:
        while True:
            taskbar_root.update()
            time.sleep(0.1)
    except tk.TclError:
        on_quit()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log_error(e)
        on_quit()
