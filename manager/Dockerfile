FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

# Set working directory
WORKDIR /app

# Prevent Python from writing pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install additional system packages if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download Playwright Chromium binary
RUN playwright install chromium

# Copy remaining source code
COPY . .

# Expose port (Railway dynamic allocation)
EXPOSE 8080

# Command to run the manager
CMD ["python", "launch_manager.py"]
