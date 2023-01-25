FROM python:3.9

# Set the working directory in the container
WORKDIR /flask-api

# Copy the requirements file to the container
COPY requirements.txt .

# Install the necessary dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY . .

# Expose the necessary ports
EXPOSE 5000

# Run the application
CMD ["python", "main.py"]