FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
  && rm -rf /var/lib/apt/lists/*

# Upgrade pip/setuptools to avoid build quirks
RUN python -m pip install --upgrade pip setuptools wheel

# Install requirements
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Copy project
COPY . /app

EXPOSE 8000
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]