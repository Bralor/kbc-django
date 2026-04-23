"""
Django settings for **pytest** only: SQLite in-memory.

- `manage.py runserver` / production: still uses `mysite.settings` (e.g. `.env` / MSSQL).
- `pytest`: set `DJANGO_SETTINGS_MODULE=mysite.settings_test` (see repo-root `pyproject.toml`).

**Important:** Do **not** run the snippet inside ``python manage.py shell``. That process
already loaded ``mysite.settings`` at startup; changing ``os.environ`` afterwards does
**not** reload settings, so you will still see MSSQL / ``blog_db``.

Use a **fresh** interpreter and set ``DJANGO_SETTINGS_MODULE`` **before** ``django.setup()``,
from the **repo root** (so ``mysite`` is importable; same as ``pythonpath`` in ``pyproject.toml``).
If you use plain ``python`` from another directory, set ``PYTHONPATH`` to the folder that
contains ``manage.py`` (the outer ``mysite`` project directory).

Interactive REPL: ``uv run python`` from repo root, then paste the lines in order—do not
import Django or models before setting the environment variable.

    uv run python -c "
    import os
    os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings_test'
    import django
    django.setup()
    from django.conf import settings
    db = settings.DATABASES['default']
    print('ENGINE:', db['ENGINE'])
    print('NAME:  ', repr(db['NAME']))
    "

Expected output includes ``django.db.backends.sqlite3`` and ``:memory:``.
"""
from .settings import *  # noqa: F403

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
