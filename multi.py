# import cv2
# import numpy as np
# import time

# # Start video capture
# cap = cv2.VideoCapture(0)
# time.sleep(2)  # Give time for the camera to adjust

# # Capture the background
# ret, background = cap.read()
# if not ret:
#     print("Error: Could not capture background.")
#     cap.release()
#     exit()

# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         break
    
#     # Convert frame to HSV
#     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
#     # Define range for multiple colors
#     lower_white = np.array([0, 0, 200])
#     upper_white = np.array([180, 30, 255])
    
#     lower_blue = np.array([90, 50, 50])
#     upper_blue = np.array([130, 255, 255])
    
#     lower_red1 = np.array([0, 120, 70])
#     upper_red1 = np.array([10, 255, 255])
#     lower_red2 = np.array([170, 120, 70])
#     upper_red2 = np.array([180, 255, 255])
    
#     # Create masks for detecting multiple colors
#     mask_white = cv2.inRange(hsv, lower_white, upper_white)
#     mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
#     mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
#     mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    
#     mask_red = mask_red1 + mask_red2
#     mask = mask_white + mask_blue + mask_red
#     mask_inv = cv2.bitwise_not(mask)
    
#     # Extract the parts of the frame that are not masked colors
#     res1 = cv2.bitwise_and(frame, frame, mask=mask_inv)
#     res2 = cv2.bitwise_and(background, background, mask=mask)
    
#     # Combine both results
#     final_output = cv2.addWeighted(res1, 1, res2, 1, 0)
    
#     # Show output
#     cv2.imshow('Invisibility Cloak', final_output)
    
#     # Break on pressing 'q'
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release resources
# cap.release()
# cv2.destroyAllWindows()







import cv2
import numpy as np
import time

def select_color():
    print("Select a color for invisibility:")
    print("1: White")
    print("2: Blue")
    print("3: Red")
    choice = input("Enter the number of your choice: ")
    
    if choice == '1':
        return np.array([0, 0, 200]), np.array([180, 30, 255])
    elif choice == '2':
        return np.array([90, 50, 50]), np.array([130, 255, 255])
    elif choice == '3':
        return np.array([0, 120, 70]), np.array([180, 255, 255])
    else:
        print("Invalid choice, defaulting to Blue.")
        return np.array([90, 50, 50]), np.array([130, 255, 255])

# Select color range
lower_color, upper_color = select_color()

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
    
    # Create mask for the selected color
    mask = cv2.inRange(hsv, lower_color, upper_color)
    mask_inv = cv2.bitwise_not(mask)
    
    # Extract the parts of the frame that are not the selected color
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
