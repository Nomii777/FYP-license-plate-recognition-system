# Dictionary of registered license plates with additional vehicle information
registered_plates = {
    # Format: "PLATE_NUMBER": {"owner": "Name", "model": "Vehicle Model", "status": "Registered/Stolen/etc."}
    "LXA1234": {
        "owner": "John Doe",
        "model": "Toyota Camry 2020",
        "status": "Registered"
    },
    "LEA5678": {
        "owner": "Jane Smith",
        "model": "Honda Civic 2019",
        "status": "Registered"
    },
    "353BA": {
        "owner": "Jane Smith",
        "model": "TOYOTA LANDCRUISER 2023",
        "status": "Registered"
    },
    "BY6002TB7": {
        "owner": "Robert Johnson",
        "model": "Ford F-150 2021",
        "status": "Registered"
    },
    "XC40": {
        "owner": "Robert Johnson",
        "model": "Toyota Camry 2021",
        "status": "Registered"
    },
    "83H22122": {
        "owner": "Sarah Williams",
        "model": " HONDA 125 2022",
        "status": "Registered"
    },
    "59E121500": {
        "owner": "Michael Brown",
        "model": "CD 70 2018",
        "status": "Registered"
    },
    "M22BLS": {
        "owner": "Michael Brown",
        "model": "Chevrolet Malibu 2018",
        "status": "Registered"
    }
}

def check_plate_registration(plate_number):
    """
    Check if a license plate is registered in the database
    
    Args:
        plate_number (str): The license plate number to check
        
    Returns:
        dict: Dictionary with registration info if found, None otherwise
    """
    # Clean the plate number (remove spaces and make uppercase)
    cleaned_plate = plate_number.replace(" ", "").upper()
    
    # Check if plate exists in database
    if cleaned_plate in registered_plates:
        return registered_plates[cleaned_plate]
    else:
        return None

def get_all_registered_plates():
    """
    Get all registered license plates
    
    Returns:
        dict: Copy of the registered plates dictionary
    """
    return registered_plates.copy()