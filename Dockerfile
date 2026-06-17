# Use a lightweight official Python runtime
FROM python:3.10-slim

# Set system work directories
WORKDIR /app

# Install system dependencies needed for premium image compression & rendering
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Clone project environment configurations
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything else into the container
COPY . .

# Expose Streamlit's default networking traffic port
EXPOSE 8501

# Run sanity check health parameters
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Boot the custom configuration
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]