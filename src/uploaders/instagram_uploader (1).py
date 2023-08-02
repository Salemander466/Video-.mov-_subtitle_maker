#!/usr/bin/env python
# coding: utf-8

# In[12]:


get_ipython().system('pip install Pillow opencv-python-headless matplotlib')




# In[55]:


get_ipython().system('pip install selenium')


# In[17]:


get_ipython().system('pip install pyautogui')


# In[10]:


import cv2
import numpy as np
from PIL import ImageGrab
import matplotlib.pyplot as plt
import time
import pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


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

loading_image_path = r"C:\Users\teams\Untitled Folder\insta_uploader_photos\loadingimageinsta.png"  # Path to loading image
break_image_path = r"C:\Users\teams\Untitled Folder\insta_uploader_photos\finishloadingimageinsta.png"


def is_loading_image_present():
    screenshot_pil = ImageGrab.grab()
    screenshot = np.array(screenshot_pil)
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    
    # Check for loading image
    loading_image = cv2.imread(loading_image_path, cv2.IMREAD_GRAYSCALE)
    result_loading = cv2.matchTemplate(screenshot_gray, loading_image, cv2.TM_CCOEFF_NORMED)
    _, max_val_loading, _, _ = cv2.minMaxLoc(result_loading)
    
    # Check for specific break image
    break_image = cv2.imread(break_image_path, cv2.IMREAD_GRAYSCALE)
    result_break = cv2.matchTemplate(screenshot_gray, break_image, cv2.TM_CCOEFF_NORMED)
    _, max_val_break, _, _ = cv2.minMaxLoc(result_break)
    
    if max_val_break > 0.8: # Threshold for detection of break image
        return 'break'
    
    return max_val_loading > 0.8 # Threshold for detection of loading image


def is_specific_image_present(image_path):
    # Take a screenshot
    screenshot_pil = ImageGrab.grab()
    screenshot = np.array(screenshot_pil)
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Read the specific image
    specific_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Match the specific image within the screenshot
    result = cv2.matchTemplate(screenshot_gray, specific_image, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(result)

    return max_val > 0.8  # Threshold for detection

def open_instagram_in_incognito():
    chrome_options = Options()
    chrome_options.add_argument("--incognito")  # Enable incognito mode

    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.get('https://www.instagram.com/')  # Open Instagram
    return driver


    
    
    
driver = open_instagram_in_incognito()

specific_image_path = r"C:\Users\teams\Untitled Folder\insta_uploader_photos\ifstartimageinsta.png"
time.sleep(15)
print("start program")
if is_specific_image_present(specific_image_path):
    
    print("Specific image found!")
    input_image_path4 = r"C:\Users\teams\Untitled Folder\insta_uploader_photos\cookimageinstsa.png"  # Update with the correct path
    screenshot4 = find_and_click(input_image_path4)
else:
    print("Specific image not found.")

# Delay the execution by 5 seconds
time.sleep(6)

input_image_path7 = r"C:\Users\teams\Untitled Folder\insta_uploader_photos\logimageinsta.png"  # Update with the correct path
string_to_paste = "the_new_www"  # Update with the string you want to paste
screenshot7 = find_and_click(input_image_path7, type_string=string_to_paste)

time.sleep(2)

input_image_path7 = r"C:\Users\teams\Untitled Folder\insta_uploader_photos\pasimageinsta.png"  # Update with the correct path
string_to_paste = "1204Kobe"  # Update with the string you want to paste
screenshot7 = find_and_click(input_image_path7, type_string=string_to_paste)

time.sleep(2)

# First image and click
input_image_path1 = r"C:\Users\teams\Untitled Folder\insta_uploader_photos\logbutimageinsta.png"
screenshot1 = find_and_click(input_image_path1)

time.sleep(10)


# First image and click
input_image_path1 = r"C:\Users\teams\Untitled Folder\insta_uploader_photos\1imageinsta.png"
screenshot1 = find_and_click(input_image_path1)

# Wait 1 second
time.sleep(2)

# Second image and click
input_image_path2 = r"C:\Users\teams\Untitled Folder\insta_uploader_photos\2imageinsta.png"  # Update with the correct path
screenshot2 = find_and_click(input_image_path2)

# Wait 1 second
time.sleep(2)

# Third image, click, type string, and press enter
input_image_path3 = r"C:\Users\teams\Untitled Folder\insta_uploader_photos\3imageinsta.png"  # Update with the correct path
string_to_copy = r"C:\Users\teams\Untitled Folder\output_yellow.mov"  # Update with the correct string
screenshot3 = find_and_click(input_image_path3, type_string=string_to_copy)


# Wait 1 second
time.sleep(9)




if is_specific_image_present(r"C:\Users\teams\Untitled Folder\insta_uploader_photos\ifreelimageinsta.png"):
    print("Specific image found!")
    time.sleep(3)
    input_image_path4 = r"C:\Users\teams\Untitled Folder\insta_uploader_photos\okimageinsta.png"  # Update with the correct path
    screenshot4 = find_and_click(input_image_path4)
else:
    print("Specific image not found.")

time.sleep(4)
# Fourth image and click
input_image_path4 = r"C:\Users\teams\Untitled Folder\insta_uploader_photos\4imageinsta.png"  # Update with the correct path
screenshot4 = find_and_click(input_image_path4)


# Wait 1 second
time.sleep(4)

# 5 image and click
input_image_path4 = r"C:\Users\teams\Untitled Folder\insta_uploader_photos\5imageinsta.png"  # Update with the correct path
screenshot4 = find_and_click(input_image_path4)


# Wait 1 second
time.sleep(4)

# 6 image and click
input_image_path4 = r"C:\Users\teams\Untitled Folder\insta_uploader_photos\6imageinsta.png"  # Update with the correct path
screenshot4 = find_and_click(input_image_path4)

# Wait 1 second
time.sleep(4)

# 6 image and click
input_image_path4 = r"C:\Users\teams\Untitled Folder\insta_uploader_photos\6imageinsta.png"  # Update with the correct path
screenshot4 = find_and_click(input_image_path4)

# Wait 1 second
time.sleep(2)

input_image_path7 = r"C:\Users\teams\Untitled Folder\insta_uploader_photos\7imageinsta.png"  # Update with the correct path
string_to_paste = "lmao"  # Update with the string you want to paste
screenshot7 = find_and_click(input_image_path7, type_string=string_to_paste)

time.sleep(2)

# 8 image and click
input_image_path4 = r"C:\Users\teams\Untitled Folder\insta_uploader_photos\8imageinsta.png"  # Update with the correct path
screenshot4 = find_and_click(input_image_path4)

time.sleep(6)

while True:
    loading_status = is_loading_image_present()
    if loading_status == 'break':
        print("Specific break image found, exiting loop...")
        break
    else:
        print("Loading image is present, waiting...")
        time.sleep(1)  # Wait for 1 second before checking again
 

time.sleep(3)
# 9 image and click
input_image_path4 = r"C:\Users\teams\Untitled Folder\insta_uploader_photos\9imageinsta.png"  # Update with the correct path
screenshot4 = find_and_click(input_image_path4)

time.sleep(3)
# 9 image and click
input_image_path4 = r"C:\Users\teams\Untitled Folder\insta_uploader_photos\9imageinsta.png"  # Update with the correct path
screenshot4 = find_and_click(input_image_path4)


time.sleep(5)

# 6 image and click
input_image_path4 = r"C:\Users\teams\Untitled Folder\insta_uploader_photos\logoutimageisnta.png"  # Update with the correct path
screenshot4 = find_and_click(input_image_path4)

time.sleep(6)

try:

    # 6 image and click
    input_image_path4 = r"C:\Users\teams\Untitled Folder\insta_uploader_photos\rimageisnta.png"  # Update with the correct path
    screenshot4 = find_and_click(input_image_path4)

    time.sleep(2)

    # 6 image and click
    input_image_path4 = r"C:\Users\teams\Untitled Folder\insta_uploader_photos\rimageisnta.png"  # Update with the correct path
    screenshot4 = find_and_click(input_image_path4)
    
    
except:
    print("end")
    
    
driver.quit()


# In[45]:


C:\Users\teams\Untitled Folder\output.mov
    


# In[ ]:




