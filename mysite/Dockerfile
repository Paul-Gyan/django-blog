# Use Python 3.12
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . .

# Set Python path
ENV PYTHONPATH=/app

# Run the app
CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8000", "--chdir", "/app"]