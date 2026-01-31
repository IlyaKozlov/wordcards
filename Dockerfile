# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Ensure pip is up-to-date
RUN pip install --no-cache-dir --upgrade pip
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
# Copy the src folder into the image
COPY src/ ./src/

# Copy the .env file from the project root (same level as src/)
# This makes environment variables defined in .env available at runtime
COPY .env ./

# Install Python dependencies from src/requirements.txt
# (This will fail at build time if src/requirements.txt does not exist)


# Ensure Python output is sent straight to the terminal (no buffering)
ENV PYTHONUNBUFFERED=1

# Expose the desired port
EXPOSE 2218
ENV PYTHONPATH=/app/src
# Run the application
CMD ["python3", "src/api/main.py"]
