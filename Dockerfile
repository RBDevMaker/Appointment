FROM public.ecr.aws/docker/library/python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt \
    && pip install --no-cache-dir boto3 pymysql cryptography

# Copy application code
COPY . .

# Expose port
EXPOSE 8088

# Run the application
CMD ["sh", "-c", "python manage.py migrate && gunicorn hairdresser_django.wsgi:application --bind 0.0.0.0:${PORT:-8000}"]
