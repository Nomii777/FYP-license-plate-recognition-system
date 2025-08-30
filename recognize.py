import easyocr
import cv2
import os
from database import check_plate_registration

# Initialize the EasyOCR reader
reader = easyocr.Reader(['en'])

def recognize_plate_text(plate_image_path):
    """
    Recognize text from license plate image and check registration
    
    Args:
        plate_image_path (str): Path to the license plate image
        
    Returns:
        dict: Dictionary containing:
            - 'text': Recognized plate text
            - 'registration_info': Registration info if found, None otherwise
    """
    # Read the plate image
    plate_image = cv2.imread(plate_image_path)
    
    if plate_image is None:
        return {
            'text': "Could not read plate image",
            'registration_info': None
        }
    
    # Convert to grayscale
    gray_plate = cv2.cvtColor(plate_image, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding
    _, threshold_plate = cv2.threshold(gray_plate, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Save the thresholded image (optional)
    threshold_path = plate_image_path.replace('.jpg', '_threshold.jpg')
    cv2.imwrite(threshold_path, threshold_plate)
    
    # Perform OCR
    results = reader.readtext(threshold_plate, detail=0)
    
    # Join the results into a single string
    plate_text = ' '.join(results).upper()
    
    # Clean up the text (remove special characters, etc.)
    plate_text = ''.join(c for c in plate_text if c.isalnum() or c.isspace())
    
    if not plate_text:
        return {
            'text': "No text recognized",
            'registration_info': None
        }
    
    # Check plate registration
    registration_info = check_plate_registration(plate_text)
    
    return {
        'text': plate_text,
        'registration_info': registration_info
    }

    # return plate_text if plate_text else "No text recognized"