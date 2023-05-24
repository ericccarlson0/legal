import cv2
import os
import pytesseract
import re

from pathlib import Path
from pdf2image import convert_from_path
from pypdf import PdfReader

from util.str_util import strip_whitespace, strip_line_numbers, is_numbered, find_first_n
from util.str_util import cut_after_suffix, cut_before_prefix
from util.directories import TRANSCRIBE_TEXT_DIR, FILE_INFO_DIR

class NoPdfTextException(Exception):
    pass
    
MAGIC_NUMBER = 3072

# A temporary path for intermediate files.
TEMP_DIR = os.path.join(os.getcwd(), "temp")
if not os.path.isdir(TEMP_DIR):
    os.mkdir(TEMP_DIR)

def check_transcript(fname_prefix: str):
    return os.path.isfile(os.path.join(TRANSCRIBE_TEXT_DIR, f'{fname_prefix}.txt'))

def write_transcript(fname_prefix: str):
    pdf_fpath = os.path.join(FILE_INFO_DIR, f'{fname_prefix}.pdf')
    print(f'pdf fpath {pdf_fpath}', flush=True)
    transcript = condensed_transcript(pdf_fpath)

    txt_fpath = os.path.join(TRANSCRIBE_TEXT_DIR, f'{fname_prefix}.txt')
    print(f'txt fpath {txt_fpath}', flush=True)
    Path(txt_fpath).touch()
    with open(txt_fpath, 'w') as f:
        f.write(transcript)

def condensed_transcript(fpath: str) -> str:
    transcript = depo_transcript(fpath)
    transcript = cut_after_suffix(transcript)
    transcript = cut_before_prefix(transcript)

    return transcript

def pdf_has_text(fpath: str) -> bool:
    reader = PdfReader(fpath)

    count = 0
    for i, p in enumerate(reader.pages):
        count += len(p.extract_text())
    
    return count >= MAGIC_NUMBER

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

def depo_transcript(fpath: str, l_margin: int = 0, r_margin: int = 0, t_margin: int = 0, b_margin: int = 0) -> str:
    if pdf_has_text(fpath):
        return transcript_quarters(fpath, l_margin, r_margin, t_margin, b_margin)
    else:
        return transcript_ocr(fpath, l_margin, r_margin, t_margin, b_margin)

def transcript_quarters(fpath: str, l_margin: int = 0, r_margin: int = 0, t_margin: int = 0, b_margin: int = 0):
    reader = PdfReader(fpath)

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
        # FIXME: FRAGILE
        if i < 1:
            continue

        for x_min, x_max, y_min, y_max in regions:
            body_arr.clear()
            p.extract_text(visitor_text=get_region_visitor(x_min, x_max, y_min, y_max))

            body_arr = strip_whitespace(body_arr)
            if len(body_arr) == 0:
                continue

            try:
                first_n = find_first_n(body_arr)
                body_arr = strip_line_numbers(body_arr, n=first_n)
            except:
                print("\nNOT NUMBERED")
                continue

            body_arr = strip_whitespace(body_arr)

            transcript = ' '.join(body_arr)
            transcript = re.sub('\s+', ' ', transcript)
            page_transcripts.append(transcript)

    ret = ' '.join(page_transcripts)
    ret = re.sub('\s+', ' ', ret)

    return ret

def transcript_single(fpath: str, l_margin: int = 0, r_margin: int = 0, t_margin: int = 0, b_margin: int = 0):
    reader = PdfReader(fpath)

    box = reader.pages[0].mediabox

    body_arr = []
    def visitor_body(text, cm, tm, font_dict, font_size):
        _, _, _, _, x, y = tm
        if y < t_margin or y > int(box.height - b_margin):
            return
        if x < l_margin or x > int(box.width - r_margin):
            return

        body_arr.append(extract_dotted(text) if '·' in text else text)

    page_transcripts = []
    for i, p in enumerate(reader.pages):
        body_arr.clear()
        p.extract_text(visitor_text=visitor_body)

        body_arr = strip_whitespace(body_arr)
        if len(body_arr) == 0:
            continue

        if not is_numbered(body_arr):
            print("\nNOT NUMBERED")
            continue

        # FIXME: FRAGILE
        first_n = find_first_n(body_arr)
        body_arr = strip_line_numbers(body_arr, n=first_n)
        body_arr = strip_whitespace(body_arr)

        transcript = ' '.join(body_arr)
        page_transcripts.append(transcript)

    ret = ' '.join(page_transcripts)
    ret = re.sub('\s+', ' ', ret)

    return ret

def transcript_ocr(fname: str):
    pages = convert_from_path(fname)

    page_transcripts = []
    for i, p in enumerate(pages):
        print(i, flush=True)
        
        fname = os.path.join(TEMP_DIR, f'{i}.jpeg')
        p.save(fname, 'JPEG')

        arr = cv2.imread(fname)
        _, arr = cv2.threshold(arr, 130, 255, cv2.THRESH_BINARY)
        arr = arr[100:-100, 100:-100, :] # TODO: 100 OK?

        transcript = pytesseract.image_to_string(arr) # TODO: OEM? PSM 5?
        transcript = re.sub('\s+', ' ', transcript)
        page_transcripts.append(transcript)

    for i in range(len(pages)):
        os.remove(os.path.join(TEMP_DIR, f'{i}.jpeg'))
    
    ret = ' '.join(page_transcripts)
    ret = re.sub('\s+', ' ', ret)

    return ret
