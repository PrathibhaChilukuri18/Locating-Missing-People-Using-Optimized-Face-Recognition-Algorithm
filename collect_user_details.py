import os
import json
import shutil

def create_base_directories():
    """
    Create base directories for details and images if they don't exist.
    """
    try:
        # Create details directory if it doesn't exist
        if not os.path.exists("details"):
            os.mkdir("details")
            print("Created base directory: details")

        # Create Images directory if it doesn't exist
        if not os.path.exists("Images"):
            os.mkdir("Images")
            print("Created base directory: Images")
    except Exception as e:
        print(f"An error occurred while creating base directories: {e}")
        return False
    return True

def collect_user_details():
    """
    Collect user details from input and store them in variables.
    """
    print("Please enter your details below:")

    name = input("Name: ").strip()
    gender = input("Gender (Male/Female/Other): ").strip()
    age = input("Age: ").strip()
    father_name = input("Father's Name: ").strip()
    mother_name = input("Mother's Name: ").strip()
    dob = input("Date of Birth (YYYY-MM-DD): ").strip()
    mobile_number = input("Mobile Number: ").strip()
    email = input("Email Address: ").strip()
    address = input("Address: ").strip()
    pincode = input("Pincode: ").strip()
    image_path = input("Path to image file (e.g., /path/to/image.jpg): ").strip()

    user_details = {
        "Name": name,
        "Gender": gender,
        "Age": age,
        "Father's Name": father_name,
        "Mother's Name": mother_name,
        "Date of Birth": dob,
        "Mobile Number": mobile_number,
        "Email": email,
        "Address": address,
        "Pincode": pincode,
        "Image Path": image_path
    }

    print("\nDetails collected successfully:")
    for key, value in user_details.items():
        print(f"{key}: {value}")

    return user_details

def save_user_details(user_details):
    """
    Save user details as a JSON file in the details directory.

    Parameters:
        user_details (dict): Dictionary containing user information.
    
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        # Create a safe filename by replacing spaces with underscores
        safe_filename = user_details["Name"].replace(" ", "_")
        
        # Create the full path for the details file
        details_path = os.path.join("details", f"{safe_filename}_details.json")
        
        # Write details to JSON file
        with open(details_path, 'w') as f:
            json.dump(user_details, f, indent=4)
        
        print(f"User details saved to: {details_path}")
        return True
    except Exception as e:
        print(f"An error occurred while saving user details: {e}")
        return False

def save_image_to_directory(user_details):
    """
    Save the provided image file to a user-specific subdirectory in Images.

    Parameters:
        user_details (dict): Dictionary containing user information.
    
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        image_path = user_details["Image Path"]
        
        # Validate image path
        if not os.path.isfile(image_path):
            print("The provided image path does not exist or is not a file.")
            return False

        # Create safe directory name by replacing spaces with underscores
        safe_dirname = user_details["Name"].replace(" ", "_")
        
        # Create user-specific directory in Images
        user_image_dir = os.path.join("Images", safe_dirname)
        os.makedirs(user_image_dir, exist_ok=True)
        
        # Get the file extension
        file_extension = os.path.splitext(image_path)[1]
        
        # Construct the target path
        target_path = os.path.join(user_image_dir, f"profile_image{file_extension}")

        # Copy the image to the target directory
        shutil.copy(image_path, target_path)
        print(f"Image saved to: {target_path}")
        return True
    except Exception as e:
        print(f"An error occurred while saving the image: {e}")
        return False

def main():
    # Create base directories
    if not create_base_directories():
        print("Failed to create base directories. Exiting.")
        return

    # Collect user details
    user_details = collect_user_details()

    # Save user details as JSON
    details_saved = save_user_details(user_details)

    # Save user image
    image_saved = save_image_to_directory(user_details)

    # Provide final status
    if details_saved and image_saved:
        print("User details and image saved successfully.")
    elif details_saved:
        print("User details saved, but the image could not be saved.")
    else:
        print("Failed to save user details and image.")

if __name__ == "__main__":
    main()