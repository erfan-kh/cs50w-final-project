#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """Run administrative tasks."""
    # Set the default Django settings module for the 'serverV1' project.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'serverV1.settings')

    try:
        # Import and execute Django's command-line utility.
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Raise an ImportError if Django is not installed or not available on the PYTHONPATH.
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # Execute the command-line utility with the given arguments.
    execute_from_command_line(sys.argv)

# If this script is run as the main program, execute the main function.
if __name__ == '__main__':
    main()
