import sys
sys.path.append("/Users/ericcarlson/Desktop/Projects/re-act") # FIXME

from typing import List
from util.str_util import count_spaces

# DIVIDE STRING BASED ON ALLOWED TOKENS
def divide_by_tokens(s: str, max_tokens: int) -> List[str]:
    spaces = count_spaces(s)
    n_segments = spaces // max_tokens + 1
    print(n_segments, 'segments')

    segments = []
    prev_p = 0
    for i in range(1, n_segments):
        curr_p = (i * len(s)) // n_segments
        # MOVE TO NEXT Q
        while s[curr_p: curr_p+2] != 'Q.':
            if curr_p+2 >= len(s):
                raise Exception('Question (Q.) not found!')
            curr_p += 1
        
        segments.append(s[prev_p: curr_p])
        prev_p = curr_p
    
    segments.append(s[prev_p:])

    return segments
