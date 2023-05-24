import openai
import os
import util.setup_openai

from util.directories import TRANSCRIBE_TEXT_DIR
from util.token_util import divide_by_tokens
from util.transcripts import depo_transcript, MAGIC_NUMBER

def get_file_summary(fname_prefix: str, prompt: str) -> str:
    fpath = os.path.join(TRANSCRIBE_TEXT_DIR, f'{fname_prefix}.txt')
    with open(fpath, 'r') as f:
        transcript = f.read()

    return get_text_summary(transcript, prompt)

def get_text_summary(input: str, prompt: str, do_seg: bool = True) -> str:
    if do_seg:
        segments = divide_by_tokens(input, MAGIC_NUMBER)
        ret = ""
        for i, s in enumerate(segments):
            print('segment', i)
            content = get_completion(s, prompt)
            ret += f'Part {i+1}.\n{content}\n'
        
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
