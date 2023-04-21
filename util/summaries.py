import openai
import util.setup_openai

from plaintiff.plaintiffs import DEPO_DIR
from util.str_util import cut_after_suffix, cut_before_prefix
from util.token_util import divide_by_tokens
from util.transcripts import depo_transcript_quarters

def pdf_summary(fname: str, prompt: str, l_margin: int = 75, r_margin: int = 75, 
                t_margin: int = 75, b_margin: int = 75) -> str:
    transcript = depo_transcript_quarters(DEPO_DIR, fname, l_margin, r_margin, t_margin, b_margin)
    transcript = cut_after_suffix(transcript)
    transcript = cut_before_prefix(transcript)

    return text_summary(transcript, prompt)

def text_summary(input: str, prompt: str) -> str:
    segments = divide_by_tokens(input, 3072)

    ret = ""
    for i, s in enumerate(segments):
        print(i)

        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": s}
        ]

        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                messages=messages,
                                                temperature=.2)
        print('usage', completion.usage)
        content = completion.choices[0].message.content
        # print(content)
        ret += f'Part {i+1}. {content}\n'
    
    return ret