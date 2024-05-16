#!/bin/bash
if [[ -z "${PORT}" ]]; then
    PORT=8000
fi

if [[ -z "${WORKERS}" ]]; then
    WORKERS=4
fi

echo "Running FastAPI App..."
echo "Port: ${PORT}"
echo "Workers: ${WORKERS}"

gunicorn config.asgi:fastapp \
    --timeout 30 \
    --graceful-timeout 30 \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    --worker-class=uvicorn.workers.UvicornWorker \
    --workers=${WORKERS} \
    --bind=0.0.0.0:${PORT}
