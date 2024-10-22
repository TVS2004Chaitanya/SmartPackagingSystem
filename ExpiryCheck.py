import pytesseract
import cv2 as cv
import re
from datetime import datetime
import time

def extract_dates(text):
    date_patterns = [
        r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",  # Matches dd/mm/yyyy or mm-dd-yyyy
        r"\b\d{1,2} [A-Za-z]+ \d{4}\b",        # Matches dd Month yyyy (e.g., 15 May 2020)
        r"\b[A-Za-z]+ \d{1,2}, \d{4}\b",       # Matches Month dd, yyyy (e.g., May 15, 2020)
        r"\b\d{4}-\d{2}-\d{2}\b"               # Matches yyyy-mm-dd
    ]
    
    found_dates = []
    
    for pattern in date_patterns:
        matches = re.findall(pattern, text)
        found_dates.extend(matches)
    
    return found_dates if found_dates else None

def convert_to_unix(dates):
    date_formats = [
        "%d/%m/%Y",  # Format: dd/mm/yyyy
        "%d-%m-%Y",  # Format: dd-mm-yyyy
        "%d %B %Y",  # Format: dd Month yyyy
        "%B %d, %Y", # Format: Month dd, yyyy
        "%Y-%m-%d"   # Format: yyyy-mm-dd
    ]
    
    unix_times = []  # List to hold Unix timestamps

    for date_str in dates:
        for date_format in date_formats:
            try:
                # Try parsing the date string with the current format
                date_obj = datetime.strptime(date_str, date_format)
                # Convert to Unix timestamp (seconds since the epoch)
                unix_time = date_obj.timestamp()
                unix_times.append(unix_time)  # Append to the list of Unix timestamps
                break  # Break if parsing is successful
            except ValueError:
                # Continue if the current format doesn't match
                continue
        else:
            unix_times.append(None)  # Append None if no format matched

    return unix_times  # Return the list of Unix timestamps

# Read the image
img = cv.imread("LogoCheck.jpg")

# Convert to grayscale for better OCR results
gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# Apply thresholding to make the text stand out more
_, thresh_img = cv.threshold(gray_img, 200, 255, cv.THRESH_BINARY_INV)
if thresh_img.any():
    cv.imshow("ThresholdImage", thresh_img)

# Use dilation to fill gaps in text
kernel = cv.getStructuringElement(cv.MORPH_RECT, (2, 2))
dilated_img = cv.dilate(thresh_img, kernel, iterations=1)

# Apply OCR with configuration for better detection of digits (like dates)
custom_config = r'--oem 3 --psm 11'  # 'psm 6' means assume a single uniform block of text
text = pytesseract.image_to_string(dilated_img, config=custom_config)

# Print the extracted text
print(text)
cv.waitKey(0)
# dates_found = extract_dates(text)
# unix_times = convert_to_unix(dates_found)
# # print(dates_found)
# # print(unix_times)
# # print(time.time())

# current_time = time.time()

# for date_str, unix_time in zip(dates_found, unix_times):
#     if unix_time is not None:
#         if unix_time < current_time:
#             print(f"{date_str} - Expired.")
#         else:
#             print(f"{date_str} - Not Expired.")
#     else:
#         print(f"{date_str} - Could not convert to Unix time.")

# cv.waitKey(0)

