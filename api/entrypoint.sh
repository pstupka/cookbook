#!/bin/sh
set -e

alembic upgrade head
python init_admin.py
exec uvicorn app.main:app --host 0.0.0.0 --workers 4
