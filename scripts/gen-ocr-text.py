import cv2
import os
import pytesseract

from pdf2image import convert_from_path

FILE_PATH = "/Users/ericcarlson/Desktop/Reyes Browne/Depos/Plaintiff/Brandon Fields Full.pdf"
TEMP_PATH = os.path.join(os.getcwd(), "temp")
if not os.path.isdir(TEMP_PATH):
    os.mkdir(TEMP_PATH)

pages = convert_from_path(FILE_PATH)
print('loaded with pdf2image')

max_i = 4
for i, p in enumerate(pages):
    fname = os.path.join(TEMP_PATH, f'{i}.jpeg')
    p.save(fname, 'JPEG')

    arr = cv2.imread(fname)
    _, arr = cv2.threshold(arr, 130, 255, cv2.THRESH_BINARY)

    img_str = pytesseract.image_to_string(arr)

    print(i)
    print(img_str)

    if i >= max_i:
        break
