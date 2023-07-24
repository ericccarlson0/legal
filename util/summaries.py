import openai
import os
import util.setup_openai

from util.constants import *
from util.token_util import divide_by_tokens
from util.transcripts import MIN_DEPO_CHAR_LEN

def get_file_summary(fname_prefix: str, prompt: str) -> str:
    fpath = os.path.join(TRANSCRIPT_COND_DIR, f'{fname_prefix}.txt')
    with open(fpath, 'r') as f:
        transcript = f.read()

    return get_text_summary(transcript, prompt)

def get_text_summary(input: str, prompt: str, do_seg: bool = True) -> str:
    if do_seg:
        segments = divide_by_tokens(input, MIN_DEPO_CHAR_LEN)
        ret = ""
        for i, s in enumerate(segments):
            print(f'segment {i}', flush=True)
            content = get_completion(s, prompt)
            print(f'done, segment {i}', flush=True)
            # TODO: (*)
            ret += f'\n{content}'
        
        return ret
    
    return get_completion(input, prompt)

def get_completion(s: str, prompt: str):
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": s}
    ]

    try:
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                messages=messages,
                                                temperature=.2)
    except openai.error.InvalidRequestError as e:
        raise Exception(f'{e}\nWith text,\n{s}')

    print('usage', completion.usage)
    content = completion.choices[0].message.content

    return content

def check_summary(file_id: str, topic: str) -> str:
    summary_fpath = os.path.join(SUMMARY_FINAL_DIR, f'{file_id}-{topic}.txt')
    if not os.path.isfile(summary_fpath):
        return None
    
    with open(summary_fpath) as f:
        ret = f.read()

    return ret
