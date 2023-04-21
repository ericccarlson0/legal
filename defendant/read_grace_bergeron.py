# import sys
# sys.path.append(PROJECT_DIR) # FIXME

import openai
import util.setup_openai as setup_openai

from defendant.defendants import DEPO_DIR, DEF_LIABILITY_PROMPT
from util.str_util import string_after, string_before, count_spaces, cut_at_q
from util.transcripts import depo_transcript

transcript = depo_transcript(DEPO_DIR, "Grace Bergeron Full.pdf", top_margin=0, bottom_margin=0)

transcript = string_after(transcript, 'P R O C E E D I N G S', include=False)

transcript = string_before(transcript, '(Whereupon, this concludes proceedings', include=False)

print(count_spaces(transcript), 'spaces')

s1, s2 = cut_at_q(transcript)
print(count_spaces(s1), count_spaces(s2))

for s in [s1, s2]:
    messages = [
        {"role": "system", "content": DEF_LIABILITY_PROMPT},
        {"role": "user", "content": s}
    ]

    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    print('usage:', completion.usage)
    content = completion.choices[0].message.content
    print(content)
