#!/bin/sh
# MediKiosk API container entrypoint.
#
# Migrations run before the server binds, so a fresh managed database is
# usable on first boot and a redeploy picks up new migrations without a
# separate step.
set -e

echo "==> applying migrations"
alembic upgrade head

if [ "${SEED_DEMO_PATIENTS}" = "true" ]; then
  # Upserts by mobile number, so this is safe on every restart.
  echo "==> seeding demo patients"
  python -m app.cli seed
fi

echo "==> starting API on port ${PORT:-8000}"
exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"
