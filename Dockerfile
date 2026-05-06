FROM python:3.12-slim

# pandoc is the only system dep we need.
# (LibreOffice deferred — users round-trip legacy .doc themselves for now.)
RUN apt-get update && apt-get install -y --no-install-recommends \
        pandoc \
    && rm -rf /var/lib/apt/lists/*

# uv for fast, reproducible dep installs.
RUN pip install --no-cache-dir uv

WORKDIR /app

# Install deps first (cache-friendly layer).
COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen --no-dev

COPY app ./app

ENV PORT=8080
ENV PYTHONUNBUFFERED=1
EXPOSE 8080

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
