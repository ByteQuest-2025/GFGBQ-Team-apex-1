# Use official Python slim image for smaller size
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Set environment variables
# Prevents Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# Copy requirements first (for Docker layer caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ./app ./app

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the application
# Using uvicorn with host 0.0.0.0 to accept external connections
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
