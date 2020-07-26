#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    try:
        from django.core.management import execute_from_command_line
        from django.conf import settings
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    try:
        is_auto = not bool(sys.argv[1])
    except IndexError:
        is_auto = True

    if is_auto:
        sys.argv.append('runserver')
        sys.argv.append('0.0.0.0:{port}'.format(port=settings.SETTINGS_MANAGE.get('SERVER_PORT')))
        sys.argv.append('--noreload')
        sys.argv.append('--insecure')
        execute_from_command_line([sys.argv[0], 'collectstatic', '--noinput'])
        execute_from_command_line([sys.argv[0], 'migrate'])
        import webbrowser
        webbrowser.open("http://localhost:{port}".format(port=settings.SETTINGS_MANAGE.get('SERVER_PORT')))
        execute_from_command_line(sys.argv)
    else:
        execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
