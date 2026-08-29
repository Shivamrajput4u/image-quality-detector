FROM python:3.12-slim

WORKDIR /app

# opencv-python-headless still needs libglib at the OS level even without a GUI
RUN apt-get update && apt-get install -y --no-install-recommends libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY ml ./ml

# data/ itself is mounted as a volume at runtime (see docker-compose.yml);
# these just ensure a fresh container has somewhere to write before that
# mount is in place.
RUN mkdir -p data/uploads data/clean data/samples

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
