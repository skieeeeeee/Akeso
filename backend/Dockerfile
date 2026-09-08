# MediKiosk API
FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# System packages: libgomp is required by the ONNX runtime used for local OCR.
RUN apt-get update \
 && apt-get install -y --no-install-recommends libgomp1 curl \
 && rm -rf /var/lib/apt/lists/*

# Dependencies first, so a code change does not invalidate the layer.
COPY requirements.txt requirements-ocr.txt ./
RUN pip install -r requirements.txt -r requirements-ocr.txt

COPY app ./app
COPY alembic ./alembic
COPY alembic.ini ./

# Uploads live on a volume; a container restart must not lose a patient's
# document.
RUN mkdir -p /app/var/uploads
VOLUME ["/app/var"]

# Run as an unprivileged user.
RUN useradd --create-home --uid 10001 medikiosk \
 && chown -R medikiosk:medikiosk /app
USER medikiosk

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s \
    CMD curl -fsS http://127.0.0.1:8000/health || exit 1

# Migrations are applied on boot so a fresh managed database is usable
# immediately. `$PORT` is honoured for Railway/Render.
CMD ["sh", "-c", "alembic upgrade head && exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
