import cv2
import numpy as np
import time
import tkinter as tk
from tkinter import ttk

def select_color(choice):
    if choice == 'White':
        return np.array([0, 0, 200]), np.array([180, 30, 255])
    elif choice == 'Blue':
        return np.array([90, 50, 50]), np.array([130, 255, 255])
    elif choice == 'Red':
        return np.array([0, 120, 70]), np.array([180, 255, 255])
    else:
        return np.array([90, 50, 50]), np.array([130, 255, 255])

def start_invisibility_effect():
    selected = color_var.get()
    lower_color, upper_color = select_color(selected)
    
    cap = cv2.VideoCapture(0)
    time.sleep(2)
    
    ret, background = cap.read()
    if not ret:
        print("Error: Could not capture background.")
        cap.release()
        return
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_color, upper_color)
        mask_inv = cv2.bitwise_not(mask)
        
        res1 = cv2.bitwise_and(frame, frame, mask=mask_inv)
        res2 = cv2.bitwise_and(background, background, mask=mask)
        
        final_output = cv2.addWeighted(res1, 1, res2, 1, 0)
        
        cv2.imshow('Invisibility Cloak', final_output)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

# Create GUI
root = tk.Tk()
root.title("Invisibility Cloak")
root.geometry("300x200")

tk.Label(root, text="Select a color for invisibility:").pack(pady=10)
color_var = tk.StringVar(value="Blue")

color_menu = ttk.Combobox(root, textvariable=color_var, values=["White", "Blue", "Red"])
color_menu.pack(pady=5)

tk.Button(root, text="Start", command=start_invisibility_effect).pack(pady=10)

tk.Label(root, text="Press 'q' to exit").pack()
root.mainloop()
