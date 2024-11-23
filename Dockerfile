# Use an official Python image as the base image
FROM python:latest

WORKDIR /usr/src/network_trf_analyzer

COPY requirements.txt ./

# Update the system and install dependencies
RUN apt-get update && apt-get install -y \
    # Add any additional system packages here if necessary
    && pip install --no-cache-dir -r requirements.txt \
    && apt autoremove \
    && rm -rf /var/lib/apt/lists/*

COPY . .

# Set the default command for the container (optional)
CMD [ "python", "./network_trf_analyzer.py" ] # Replace app.py with your entry point if necessary


