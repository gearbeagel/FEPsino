FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /backend

RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

RUN chmod +x scripts/wait-for-db.sh
RUN chmod +x scripts/wait-for-sonar.sh
RUN chmod +x scripts/init-db.sh

EXPOSE 8000

