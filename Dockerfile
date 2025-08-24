# Use an official lightweight Python image.
FROM python:3.10-slim

# Set the working directory in the container.
WORKDIR /app

# Copy the Python script into the container.
COPY hasher.py .

# The user will mount their directory to /data.
# This CMD sets the default directory to be hashed inside the container.
ENTRYPOINT ["python", "./hasher.py"]
CMD ["/data"]
