import sys
sys.path.append("/Users/ericcarlson/Desktop/Projects/re-act") # FIXME

import openai
import os
import re
import util.setup_openai as setup_openai

from plaintiff.plaintiffs import DEPO_DIR, PLA_MAJOR_PROBLEMS_PROMPT
from pypdf import PdfReader
from util.str_util import strip_whitespace, strip_line_numbers, is_numbered, find_first_n, count_spaces
from util.str_util import string_after, string_before
from util.token_util import divide_by_tokens
from util.transcripts import depo_transcript, extract_dotted

reader = PdfReader(os.path.join(DEPO_DIR, "America Cuaresma Full.pdf"))

box = reader.pages[0].mediabox
print('w', box.width, 'h', box.height)

l_margin, r_margin = 75, 75
t_margin, b_margin = 75, 75

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
            print("\nEMPTY\n")
            continue

        first_n = find_first_n(body_arr)
        try:
            body_arr = strip_line_numbers(body_arr, n=first_n)
        except:
            print("\nNOT NUMBERED\n")
            print(body_arr[0])
            print(body_arr[1], '...\n')
        body_arr = strip_whitespace(body_arr)

        print(i, f'({x_min}, {x_max}, {y_min}, {y_max})')

        transcript = ' '.join(body_arr)
        transcript = re.sub(' +', ' ', transcript)
        print(len(transcript), 'letters')
        page_transcripts.append(transcript)

transcript = ' '.join(page_transcripts)
transcript = re.sub(' +', ' ', transcript)

transcript = string_after(transcript, "P R O C E E D I N G S", include=False)
transcript = string_before(transcript, "(End of proceedings.)", include=False)
# print(transcript)

segments = divide_by_tokens(transcript, 3072)

for i, s in enumerate(segments):
    print(i)

    messages = [
        {"role": "system", "content": PLA_MAJOR_PROBLEMS_PROMPT},
        {"role": "user", "content": s}
    ]

    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                              messages=messages,
                                              temperature=.2)
    print('usage:', completion.usage)
    content = completion.choices[0].message.content
    print(content)
