from flask import Flask, request, jsonify
from PIL import Image
import pytesseract
import cv2
import numpy as np
import concurrent.futures
import os  # Import os to access environment variables

app = Flask(__name__)

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh

def solve_captcha(image):
    processed_image = preprocess_image(image)
    captcha_text = pytesseract.image_to_string(processed_image, config='--psm 8').strip()
    return captcha_text

@app.route('/solve_captcha', methods=['POST'])
def solve_captcha_endpoint():
    file = request.files.get('image')

    if not file:
        return jsonify({"error": "No file provided"}), 400

    image = Image.open(file.stream)
    image_np = np.array(image)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(solve_captcha, image_np)
        captcha_text = future.result()

    return jsonify({'captcha_text': captcha_text})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use PORT assigned by Railway
    app.run(host="0.0.0.0", port=port, threaded=True)
