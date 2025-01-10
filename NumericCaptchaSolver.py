import cv2
import pytesseract
from PIL import Image
import os

# Set the Tesseract path (Windows only)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

# Set the TESSDATA_PREFIX environment variable
os.environ['TESSDATA_PREFIX'] = r'C:\Program Files (x86)\Tesseract-OCR'

# Load the CAPTCHA image
image = cv2.imread('CAPTCHA.jpg')

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply adaptive thresholding
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

# Remove noise using morphological operations
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)

# Display the preprocessed image for debugging
cv2.imshow('Processed Image', opening)
cv2.destroyAllWindows()

# Extract text using Tesseract
custom_config = r'--oem 3 --psm 8 outputbase digits'  # Try different --psm values
text = pytesseract.image_to_string(opening, config=custom_config)

# Print raw Tesseract output for debugging
print("Raw Tesseract Output:", text)

# Clean the extracted text
cleaned_text = ''.join(filter(str.isdigit, text))

print("Extracted Text:", cleaned_text)