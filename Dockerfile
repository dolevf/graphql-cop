# Use the official Python 3 base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Add non root user
RUN useradd -m appuser
USER appuser

# Set the entry point to the Python script so arguments can be passed
ENTRYPOINT ["python", "graphql-cop.py"]
