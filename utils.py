import cv2
import numpy as np

def preprocess_image(image):
    """Preprocess image for better plate detection"""
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply histogram equalization
    gray = cv2.equalizeHist(gray)
    
    # Apply bilateral filter
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    
    return gray

def find_plate_contours(image):
    """Find potential plate contours in an image"""
    # Edge detection
    edged = cv2.Canny(image, 170, 200)
    
    # Find contours
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    # Sort contours by area and keep top 10
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    
    return contours

def is_plate_contour(contour):
    """Check if a contour is likely to be a license plate"""
    perimeter = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
    
    # Check if it's a quadrilateral
    if len(approx) == 4:
        # Check aspect ratio (typical plates are wider than tall)
        x, y, w, h = cv2.boundingRect(approx)
        aspect_ratio = w / float(h)
        return 2.0 <= aspect_ratio <= 5.0
    return False