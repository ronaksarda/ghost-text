FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
WORKDIR /app
COPY requirements.txt .
# The browser version must match the pinned playwright package, so install it here rather than use a prebuilt image.
RUN pip install --no-cache-dir -r requirements.txt && python -m playwright install --with-deps chromium
COPY . .
RUN useradd --create-home ghost && chown -R ghost /app
USER ghost
EXPOSE 8080
# --proxy-headers: behind Caddy the app must see https, so the extension download points at the https origin.
CMD ["sh", "-c", "uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8080} --proxy-headers --forwarded-allow-ips='*'"]
