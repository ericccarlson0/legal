import sys
sys.path.append("/Users/ericcarlson/Desktop/Projects/re-act") # FIXME

import os
import re

from pypdf import PdfReader
from util.str_util import strip_whitespace, strip_line_numbers, is_numbered, find_first_n

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

def depo_transcript(depo_dir, fname: str, top_margin: int = 0, bottom_margin: int = 0) -> str:
    reader = PdfReader(os.path.join(depo_dir, fname))

    box = reader.pages[0].mediabox
    print('w', box.width, 'h', box.height)

    body_arr = []
    # IGNORE HEADER, FOOTER
    def visitor_body(text, cm, tm, font_dict, font_size):
        y = tm[5]
        if y < top_margin or y > int(box.height - bottom_margin):
            return

        body_arr.append(extract_dotted(text) if '·' in text else text)

    page_transcripts = []
    for i, p in enumerate(reader.pages):
        body_arr.clear()
        p.extract_text(visitor_text=visitor_body)

        body_arr = strip_whitespace(body_arr)
        if len(body_arr) == 0:
            print("EMPTY")
            continue

        if not is_numbered(body_arr):
            print(body_arr[0])
            print(body_arr[1])
            print(body_arr[2], '...')
            print("NOT NUMBERED")
            continue

        first_n = find_first_n(body_arr)
        body_arr = strip_line_numbers(body_arr, n=first_n)
        body_arr = strip_whitespace(body_arr)

        print(i)

        transcript = ' '.join(body_arr)
        print(len(transcript), 'letters')
        page_transcripts.append(transcript)

    ret = ' '.join(page_transcripts)
    ret = re.sub(' +', ' ', ret)

    return ret
