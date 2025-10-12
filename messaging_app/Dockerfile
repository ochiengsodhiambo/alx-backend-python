# Use an official Python runtime as a parent image
FROM python:3.10

# Prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt into the container
COPY requirements.txt /app/

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app code into the container
COPY . /app/

# Expose the port ["-p"]Django will run on
EXPOSE 8000

# Start the Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

