# Use a lightweight Python Alpine image as the base image
FROM python:3.12-alpine

# Install any required system dependencies (e.g., build tools, libraries)
# For example, libxml2 and libxslt are needed for lxml, a common dependency of BeautifulSoup
# and musl-dev is often needed for compiling some Python packages
RUN apk add --no-cache \
    postgresql-dev

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt && \ 
    mv .env.sample .env

# Command to run the Python script
CMD ["python", "src/fuel.py"]  # Replace with your script file
