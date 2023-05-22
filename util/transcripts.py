import cv2
import os
import pytesseract
import re

from pdf2image import convert_from_path
from pypdf import PdfReader

from util.str_util import strip_whitespace, strip_line_numbers, is_numbered, find_first_n

MAGIC_NUMBER = 3072

# A temporary path for intermediate files.
TEMP_PATH = os.path.join(os.getcwd(), "temp")
if not os.path.isdir(TEMP_PATH):
    os.mkdir(TEMP_PATH)

def pdf_has_text(fname: str) -> bool:
    reader = PdfReader(fname)

    count = 0
    for i, p in enumerate(reader.pages):
        count += len(p.extract_text())
    
    if count < MAGIC_NUMBER:
        return False
    
    return True

def extract_dotted(s: str) -> str:
    line_arr = []
    curr = ""
    for c in s:
        if c == '·' or c == ' ':
            if len(curr) > 0:
                line_arr.append(curr)
                curr = ""
        else:
            curr += c
    
    return ' '.join(line_arr)

def depo_transcript(fname: str, top_margin: int = 0, bottom_margin: int = 0, 
                    left_margin: int = 0, right_margin: int = 0) -> str:
    reader = PdfReader(fname)

    box = reader.pages[0].mediabox
    # print('w', box.width, 'h', box.height)

    body_arr = []
    # IGNORE HEADER, FOOTER
    def visitor_body(text, cm, tm, font_dict, font_size):
        _, _, _, _, x, y = tm
        if y < top_margin or y > int(box.height - bottom_margin):
            return
        if x < left_margin or x > int(box.width - right_margin):
            return

        body_arr.append(extract_dotted(text) if '·' in text else text)

    page_transcripts = []
    for i, p in enumerate(reader.pages):
        body_arr.clear()
        p.extract_text(visitor_text=visitor_body)

        body_arr = strip_whitespace(body_arr)
        if len(body_arr) == 0:
            # print("EMPTY")
            continue

        if not is_numbered(body_arr):
            print("\nNOT NUMBERED")
            continue

        first_n = find_first_n(body_arr)
        body_arr = strip_line_numbers(body_arr, n=first_n)
        body_arr = strip_whitespace(body_arr)

        # print(i)

        transcript = ' '.join(body_arr)
        # print(len(transcript), 'letters')
        page_transcripts.append(transcript)

    ret = ' '.join(page_transcripts)
    ret = re.sub('\s+', ' ', ret)

    return ret

def depo_transcript_quarters(fname: str, l_margin: int = 75, r_margin: int = 75, 
                             t_margin: int = 75, b_margin: int = 75):
    reader = PdfReader(fname)

    box = reader.pages[0].mediabox

    body_arr = []

    def get_region_visitor(x_min, x_max, y_min, y_max):
        def visitor(text, cm, tm, font_dict, font_size):
            _, _, _, _, x, y = tm
            if y < y_min or y > y_max:
                return
            if x < x_min or x > x_max:
                return
            
            body_arr.append(extract_dotted(text) if '·' in text else text)
        
        return visitor

    page_transcripts = []
    regions = [
        [l_margin, box.width // 2, box.height // 2, int(box.height - b_margin)],
        [l_margin, box.width // 2, t_margin, box.height // 2],
        [box.width // 2, int(box.width - r_margin), box.height // 2, int(box.height - b_margin)],
        [box.width // 2, int(box.width - r_margin), t_margin, box.height // 2],
    ]
    for i, p in enumerate(reader.pages):
        if i < 1:
            continue

        for x_min, x_max, y_min, y_max in regions:
            body_arr.clear()
            p.extract_text(visitor_text=get_region_visitor(x_min, x_max, y_min, y_max))

            body_arr = strip_whitespace(body_arr)
            if len(body_arr) == 0:
                # print("\nEMPTY\n")
                continue

            try:
                first_n = find_first_n(body_arr)
                body_arr = strip_line_numbers(body_arr, n=first_n)
            except:
                print("\nNOT NUMBERED")
                continue

            body_arr = strip_whitespace(body_arr)

            # print(i, f'({x_min}, {x_max}, {y_min}, {y_max})')

            transcript = ' '.join(body_arr)
            transcript = re.sub('\s+', ' ', transcript)
            # print(len(transcript), 'letters')
            page_transcripts.append(transcript)

    ret = ' '.join(page_transcripts)
    ret = re.sub('\s+', ' ', ret)

    return ret

def depo_transcript_ocr(fname):
    pages = convert_from_path(fname)

    print('converted pages')

    page_transcripts = []
    for i, p in enumerate(pages):
        print(i)
        
        fname = os.path.join(TEMP_PATH, f'{i}.jpeg')
        p.save(fname, 'JPEG')

        arr = cv2.imread(fname)
        _, arr = cv2.threshold(arr, 130, 255, cv2.THRESH_BINARY)
        # TODO: 100 OK?
        arr = arr[100:-100, 100:-100, :]

        # TODO: OEM? PSM 5?
        transcript = pytesseract.image_to_string(arr)
        transcript = re.sub('\s+', ' ', transcript)
        page_transcripts.append(transcript)
    
    print('produced page transcripts')

    for i in range(len(pages)):
        os.remove(os.path.join(TEMP_PATH, f'{i}.jpeg'))
    
    print('removed temp files')
    
    ret = ' '.join(page_transcripts)
    ret = re.sub('\s+', ' ', ret)

    print('combined transcripts')

    return ret
