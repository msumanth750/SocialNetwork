# Use a Python base image
FROM python:3.8-alpine

# Install system dependencies
RUN apk add --no-cache tzdata

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip \
    && apk add --no-cache gcc musl-dev libffi-dev openssl-dev \
    && pip install -r requirements.txt \
    && apk del gcc musl-dev libffi-dev openssl-dev

# Expose port 8000 for the Django development server
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
