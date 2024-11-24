# Update the system and install dependencies
FROM python:3.11

# Set working directory
WORKDIR /usr/src/network_trf_analyzer

# Copy the requirements file
COPY requirements.txt ./

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-distutils \
    python3-setuptools \
    python3-pip \
    build-essential \
  && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*

# Upgrade pip and clear cache
RUN pip install --upgrade pip \
  && pip cache purge

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Default command to run the app
CMD ["python3", "./network_trf_analyzer.py"]
