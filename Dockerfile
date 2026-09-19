FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN groupadd --gid 1000 app && useradd --uid 1000 --gid app --create-home app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=app:app . .

RUN chmod +x entrypoint.sh && chown -R app:app /app

USER app

EXPOSE 8000

# Interim target until task-038 adds a dedicated health endpoint; update together.
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD python -c "import http.client; connection = http.client.HTTPConnection('127.0.0.1', 8000, timeout=2); connection.request('GET', '/'); status = connection.getresponse().status; raise SystemExit(status >= 500)" || exit 1

ENTRYPOINT ["./entrypoint.sh"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
