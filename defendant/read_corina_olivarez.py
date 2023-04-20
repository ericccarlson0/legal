import openai
import util.setup_openai as setup_openai

from defendant.defendants import DEPO_DIR, DEF_JURY_SENTIMENT_PROMPT_2
from util.str_util import count_spaces, string_after, string_before
from util.token_util import divide_by_tokens
from util.transcripts import depo_transcript

transcript = depo_transcript(DEPO_DIR, "Corina Olivarez Full.pdf", top_margin=50, bottom_margin=50)

print(count_spaces(transcript), 'spaces before cutting out prefix')

transcript = string_after(transcript, "THE REPORTER", include=True)

print(count_spaces(transcript), 'spaces before cutting out suffix')

transcript = string_before(transcript, "* * * END OF DEPOSITION * * *", include=False)

print(count_spaces(transcript), 'spaces')

segments = divide_by_tokens(transcript, 3072)

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
