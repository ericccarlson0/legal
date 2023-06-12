import cv2
import os
import pytesseract
import re
import uuid

from celery import Celery
from pdf2image import convert_from_path
from util.directories import *

# A temporary path for intermediate files.
TEMP_DIR = os.path.join(os.getcwd(), "temp")
if not os.path.isdir(TEMP_DIR):
    os.mkdir(TEMP_DIR)

app = Celery(
    'downstream_tasks',
    backend='redis://localhost:6379',
    broker='redis://localhost:6379',
)

@app.task(queue='q2')
def c_transcript_ocr_single_page(fpath, s: int):
    converted_page = convert_from_path(fpath, dpi=100, first_page=s, last_page=s, grayscale=True)

    for page in converted_page:
        single_page = page
        break

    rand_id = str(uuid.uuid4())

    fname = os.path.join(TEMP_DIR, f'{rand_id}.jpeg')
    print('created', fname, flush=True)
    single_page.save(fname, 'JPEG')

    arr = cv2.imread(fname)
    # _, arr = cv2.threshold(arr, 130, 255, cv2.THRESH_BINARY)
    arr = arr[100:-100, 100:-100, :] # TODO: 100 OK?

    transcript = pytesseract.image_to_string(arr) # TODO: OEM? PSM 5?
    transcript = re.sub('\s+', ' ', transcript)

    os.remove(fname)
    print('removed', fname, flush=True)

    return transcript

@app.task(queue='q2')
def c_transcript_ocr_in_range(fpath, s: int, e: int):
    converted_pages = convert_from_path(fpath, dpi=100, first_page=s, last_page=e, grayscale=True)

    transcript_list = []

    rand_id = str(uuid.uuid4())

    for i, page in enumerate(converted_pages):
        fname = os.path.join(TEMP_DIR, f'{rand_id}-{i}.jpeg')
        # print('created', fname, flush=True)
        page.save(fname, 'JPEG')
    
        arr = cv2.imread(fname)
        _, arr = cv2.threshold(arr, 130, 255, cv2.THRESH_BINARY)
        arr = arr[100:-100, 100:-100, :] # TODO: 100 OK?

        transcript = pytesseract.image_to_string(arr) # TODO: OEM? PSM 5?
        transcript = re.sub('\s+', ' ', transcript)
        transcript_list.append(transcript)

        os.remove(fname)
        # print('removed', fname, flush=True)
    
    ret = ' '.join(transcript_list)
    ret = re.sub('\s+', ' ', ret)

    return ret
