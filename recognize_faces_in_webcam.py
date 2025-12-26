import face_recognition
import imutils
import pickle
import numpy as np
import cv2
import os
import json

# Path to Haar cascade XML file for face detection
cascPathface = os.path.dirname(cv2.__file__) + "/data/haarcascade_frontalface_alt2.xml"
faceCascade = cv2.CascadeClassifier(cascPathface)

# Load the known faces and embeddings
try:
    with open('face_enc', "rb") as f:
        data = pickle.loads(f.read())
except Exception as e:
    print(f"Error loading face encodings: {e}")
    exit()

# Initialize video capture
print("Streaming started")
video_capture = cv2.VideoCapture(0)

def display_details(name):
    """
    Display user details from the corresponding JSON file.
    Opens a separate window showing the details.
    """
    # Create a details window
    detail_window = "User Details"
    
    try:
        # Construct the path to the JSON file
        json_file = os.path.join("details", f"{name.replace(' ', '_')}_details.json")
        
        # Check if the file exists
        if not os.path.exists(json_file):
            print(f"Details file not found for {name}")
            return
        
        # Read the JSON file
        with open(json_file, "r") as file:
            user_details = json.load(file)
        
        # Remove the last item (Image Path)
        user_details.pop("Image Path", None)
        
        # Create a white background image for displaying details
        details_image = np.ones((500, 600, 3), dtype=np.uint8) * 255
        
        # Set title
        cv2.putText(details_image, f"Details for {name}", (20, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        
        # Display each detail on the image
        y_offset = 100
        for key, value in user_details.items():
            detail_text = f"{key}: {value}"
            cv2.putText(details_image, detail_text, (20, y_offset), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 1)
            y_offset += 40
        
        # Show the details window
        cv2.imshow(detail_window, details_image)
    
    except Exception as e:
        print(f"Error displaying details for {name}: {e}")

while True:
    # Grab the frame from the video stream
    ret, frame = video_capture.read()
    
    if not ret:
        print("Failed to grab frame")
        break
    
    # Convert frame to grayscale for Haar cascade
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60), flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Convert the frame to RGB for face recognition
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Find face encodings in the frame
    locations = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, locations)
    
    names = []

    # Loop over facial embeddings
    for encoding in encodings:
        # Compare face encodings
        matches = face_recognition.compare_faces(data["encodings"], encoding)
        name = "Unknown"

        # Find the best match
        if True in matches:
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1
            name = max(counts, key=counts.get)

        names.append(name)

        # If a face is recognized, display the corresponding details
        if name != "Unknown":
            display_details(name)

    # Draw rectangles around faces and display the recognized name
    for ((top, right, bottom, left), name) in zip(locations, names):
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

    # Show the video feed
    cv2.imshow("Webcam", frame)

    # Break on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close windows
video_capture.release()
cv2.destroyAllWindows()