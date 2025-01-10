import cv2
import pytesseract
from PIL import Image
import os
import requests
from io import BytesIO
import numpy as np
# Set the Tesseract path (Windows only)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

# Set the TESSDATA_PREFIX environment variable
os.environ['TESSDATA_PREFIX'] = r'C:\Program Files (x86)\Tesseract-OCR'

# Function to download an image from a URL
def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        return image
    else:
        raise Exception(f"Failed to download image. HTTP Status Code: {response.status_code}")

# URL of the CAPTCHA image
captcha_url = "https://adsl.tci.ir/panel/captcha/?r=1736507265"  # Replace with the actual URL

# Download the CAPTCHA image
try:
    image = download_image(captcha_url)
    image.save("CAPTCHA.jpg")  # Save the image locally (optional)
    print("Image downloaded successfully.")
except Exception as e:
    print(e)
    exit()

# Convert the image to OpenCV format (numpy array)
image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply adaptive thresholding
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

# Remove noise using morphological operations
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)

# Display the preprocessed image for debugging
cv2.imshow('Processed Image', opening)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Extract text using Tesseract
custom_config = r'--oem 3 --psm 8 outputbase digits'  # Try different --psm values
text = pytesseract.image_to_string(opening, config=custom_config)

# Print raw Tesseract output for debugging
print("Raw Tesseract Output:", text)

# Clean the extracted text
cleaned_text = ''.join(filter(str.isdigit, text))

print("Extracted Text:", cleaned_text)