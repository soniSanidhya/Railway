# Use an official lightweight Python image
FROM python:3.12-slim

# Install Tesseract-OCR and necessary dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy all files into the container
COPY . .

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Ensure Tesseract is correctly set up
ENV TESSERACT_PATH="/usr/bin/tesseract"
RUN echo "Tesseract path: $TESSERACT_PATH"

# Expose the port Flask runs on
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
