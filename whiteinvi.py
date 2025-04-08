import cv2
import numpy as np
import time

# Start video capture
cap = cv2.VideoCapture(0)
time.sleep(2)  # Give time for the camera to adjust

# Capture the background
ret, background = cap.read()
if not ret:
    print("Error: Could not capture background.")
    cap.release()
    exit()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convert frame to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Define range for white color
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 30, 255])
    
    # Create mask for detecting white color
    mask = cv2.inRange(hsv, lower_white, upper_white)
    mask_inv = cv2.bitwise_not(mask)
    
    # Extract the parts of the frame that are not white
    res1 = cv2.bitwise_and(frame, frame, mask=mask_inv)
    res2 = cv2.bitwise_and(background, background, mask=mask)
    
    # Combine both results
    final_output = cv2.addWeighted(res1, 1, res2, 1, 0)
    
    # Show output
    cv2.imshow('Invisibility Cloak', final_output)
    
    # Break on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
