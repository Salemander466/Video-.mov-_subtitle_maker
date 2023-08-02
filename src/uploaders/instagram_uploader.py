#!/usr/bin/env python
# coding: utf-8

# In[12]:


get_ipython().system('pip install Pillow opencv-python-headless matplotlib')




# In[17]:


get_ipython().system('pip install pyautogui')


# In[19]:





# In[21]:





# In[33]:


import cv2
import numpy as np
from PIL import ImageGrab
import matplotlib.pyplot as plt
import time
import pyautogui

def find_and_click(image_path, type_string=None):
    # Take a screenshot
    screenshot_pil = ImageGrab.grab()
    screenshot = np.array(screenshot_pil)
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Read the input image
    input_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Match the input image within the screenshot
    result = cv2.matchTemplate(screenshot_gray, input_image, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # Draw a rectangle around the matched area
    top_left = max_loc
    bottom_right = (top_left[0] + input_image.shape[1], top_left[1] + input_image.shape[0])
    cv2.rectangle(screenshot, top_left, bottom_right, (0, 255, 0), 2)

    # Calculate the center of the detected area
    center_x = (top_left[0] + bottom_right[0]) // 2
    center_y = (top_left[1] + bottom_right[1]) // 2

    # Click the center of the detected area
    pyautogui.click(x=center_x, y=center_y)

    if type_string:
        # Type the string
        pyautogui.typewrite(type_string)
        # Press enter
        pyautogui.press('enter')

    return screenshot

# Delay the execution by 5 seconds
time.sleep(5)

# First image and click
input_image_path1 = r"C:\Users\teams\Downloads\1imageinsta"
screenshot1 = find_and_click(input_image_path1)

# Wait 1 second
time.sleep(1)

# Second image and click
input_image_path2 = r"C:\Users\teams\Downloads\2imageinsta"  # Update with the correct path
screenshot2 = find_and_click(input_image_path2)

# Wait 1 second
time.sleep(1)

# Third image, click, type string, and press enter
input_image_path3 = r"C:\Users\teams\Downloads\3imageinsta.png"  # Update with the correct path
string_to_copy = r"C:\Users\teams\Untitled Folder\output.mov"  # Update with the correct string
screenshot3 = find_and_click(input_image_path3, type_string=string_to_copy)


# Wait 1 second
time.sleep(3)

# Fourth image and click
input_image_path4 = r"C:\Users\teams\Downloads\4imageinsta.png"  # Update with the correct path
screenshot4 = find_and_click(input_image_path4)


# Wait 1 second
time.sleep(2)

# 5 image and click
input_image_path4 = r"C:\Users\teams\Downloads\5imageinsta.png"  # Update with the correct path
screenshot4 = find_and_click(input_image_path4)


# Wait 1 second
time.sleep(2)

# 6 image and click
input_image_path4 = r"C:\Users\teams\Downloads\6imageinsta.png"  # Update with the correct path
screenshot4 = find_and_click(input_image_path4)

# Wait 1 second
time.sleep(2)

# 6 image and click
input_image_path4 = r"C:\Users\teams\Downloads\6imageinsta.png"  # Update with the correct path
screenshot4 = find_and_click(input_image_path4)

# Wait 1 second
time.sleep(2)

input_image_path7 = r"C:\Users\teams\Downloads\7imageinsta.png"  # Update with the correct path
string_to_paste = "lmao"  # Update with the string you want to paste
screenshot7 = find_and_click(input_image_path7, type_string=string_to_paste)

time.sleep(2)

# 6 image and click
input_image_path4 = r"C:\Users\teams\Downloads\8imageinsta.png"  # Update with the correct path
screenshot4 = find_and_click(input_image_path4)


