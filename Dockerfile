# Use a slim Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies if needed
# (e.g. gcc, curl if your libs require them)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project code
COPY . .

# Expose a port if you want to run an API server later (e.g. FastAPI/Flask)
EXPOSE 8080

# Default command: run your agent entrypoint
# Update this to the right module/function for your project
CMD ["python", "-m", "strands_agentcore.external_api"]
