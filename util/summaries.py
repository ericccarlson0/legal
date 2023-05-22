import openai
import os
import util.setup_openai

from util.str_util import cut_after_suffix, cut_before_prefix
from util.token_util import divide_by_tokens
from util.transcripts import pdf_has_text, depo_transcript_ocr, depo_transcript_quarters, MAGIC_NUMBER
from sf.docrio import FILE_INFO_DIR

def get_pdf_summary(fname: str, prompt: str, l_margin: int = 75, r_margin: int = 75, 
                t_margin: int = 75, b_margin: int = 75) -> str:
    full_path = os.path.join(FILE_INFO_DIR, fname)
    if pdf_has_text(full_path):
        transcript = depo_transcript_quarters(full_path, l_margin, r_margin, t_margin, b_margin)
    else:
        transcript = depo_transcript_ocr(full_path)
    
    transcript = cut_after_suffix(transcript)
    transcript = cut_before_prefix(transcript)

    return get_text_summary(transcript, prompt)

def get_text_summary(input: str, prompt: str, do_seg: bool = True) -> str:
    if do_seg:
        segments = divide_by_tokens(input, MAGIC_NUMBER)
        ret = ""
        for i, s in enumerate(segments):
            content = get_completion(s, prompt)
            ret += f'Part {i+1}.\n{content}\n'
        
        return ret
    
    return get_completion(input, prompt)

def get_completion(s: str, prompt: str):
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": s}
    ]

    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                            messages=messages,
                                            temperature=.2)
    print('usage', completion.usage)
    content = completion.choices[0].message.content

    return content
