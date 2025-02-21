# expense_tracker/cli.py
import os
import sys
from django.core.management import execute_from_command_line


def main():
    # Set the settings module if not already set
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "expense_tracker.settings")
    # Execute Django management commands (e.g., runserver)
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
