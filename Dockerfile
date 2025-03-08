FROM docker.arvancloud.ir/python:3.11

# Set the working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY src/ ./

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose the port Django runs on
EXPOSE 8000

# Default command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

