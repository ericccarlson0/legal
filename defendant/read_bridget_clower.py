# import sys
# sys.path.append(PROJECT_DIR) # FIXME

import openai
import util.setup_openai as setup_openai

from defendant.defendants import DEPO_DIR, DEF_JURY_SENTIMENT_PROMPT_2
from util.str_util import count_spaces, string_after, string_before
from util.token_util import divide_by_tokens
from util.transcripts import depo_transcript

transcript = depo_transcript(DEPO_DIR, "Bridget Clower Full.pdf", top_margin=0, bottom_margin=0)

transcript = string_after(transcript, 'P R O C E E D I N G S', include=False)

transcript = string_before(transcript, '(End of deposition at 3:16 p.m.)', include=False)

print(count_spaces(transcript), 'spaces')

segments = divide_by_tokens(transcript, 2560)

for i, s in enumerate(segments):
    print(i)

    messages = [
        {"role": "system", "content": DEF_JURY_SENTIMENT_PROMPT_2},
        {"role": "user", "content": s}
    ]
    
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                              messages=messages,
                                              temperature=.2)
    print('usage:', completion.usage)
    content = completion.choices[0].message.content
    print(content)
