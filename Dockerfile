FROM python:3.12-slim

WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install curl
RUN apt-get update && apt-get install -y curl

# Setup periodic healthcheck
#HEALTHCHECK --interval=1m --timeout=3s CMD curl -s -f -H "Accept: application/json" http://localhost:8000/health

# Expose port
EXPOSE 8000

# Start application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
