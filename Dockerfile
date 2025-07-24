FROM python:3.11-slim

# Install build dependencies for psycopg2
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      build-essential \
      libpq-dev \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip \
 && pip install -r requirements.txt

CMD ["python", "app.py"]
