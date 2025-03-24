# Use official Python image
FROM python:3.9

# Install system dependencies
RUN apt-get update && apt-get install -y tesseract-ocr libtesseract-dev

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 (Flask default)
EXPOSE 5000

# Run the application
CMD ["gunicorn", "-b", "0.0.0.0:5000", "main:app"]
