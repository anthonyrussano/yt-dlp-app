# Use the official Python base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask app files to the container
COPY . .

# Expose the Flask app port
EXPOSE 5000

# Set the entry point command
CMD ["python", "app.py"]
