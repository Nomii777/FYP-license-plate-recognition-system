import cv2
import numpy as np
import os
from datetime import datetime

def detect_license_plate(image_path):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        return None
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply bilateral filter to reduce noise while keeping edges sharp
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    
    # Find edges using Canny
    edged = cv2.Canny(gray, 170, 200)
    
    # Find contours
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    # Sort contours by area in descending order and keep top 10
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    
    plate_contour = None
    
    # Loop over contours to find the best rectangular contour
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
        
        # If the approximated contour has 4 points, we assume it's a rectangle
        if len(approx) == 4:
            plate_contour = approx
            break
    
    if plate_contour is None:
        return None
    
    # Create a mask for the license plate
    mask = np.zeros(gray.shape, np.uint8)
    cv2.drawContours(mask, [plate_contour], 0, 255, -1)
    
    # Bitwise AND to extract the license plate region
    plate = cv2.bitwise_and(image, image, mask=mask)
    
    # Get coordinates of the license plate contour
    x, y, w, h = cv2.boundingRect(plate_contour)
    
    # Crop the license plate
    plate_cropped = plate[y:y+h, x:x+w]
    
    # Save the cropped plate
    plate_filename = f"plate_{os.path.basename(image_path)}"
    plate_path = os.path.join(os.path.dirname(image_path), plate_filename)
    cv2.imwrite(plate_path, plate_cropped)
    
    return plate_path