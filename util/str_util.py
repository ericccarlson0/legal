from typing import List, Tuple

# FUNCTION TO STRIP WHITESPACE
def strip_whitespace(line_arr: List[str]) -> List[str]:
    ret = []
    for line in line_arr:
        if len(line) > 0 and not line.isspace():
            ret.append(line)
    
    return ret

# FUNCTION TO STRIP LINE NUMBERS
def strip_line_numbers(line_arr: List[str], n: int = 1) -> List[str]:

    ret = []
    for i, line in enumerate(line_arr):
        if i == 0 and not line.split(' ')[0].isnumeric():
            continue   

        n_str = str(n)
        if len(line) >= len(n_str) and line[:len(n_str)] == n_str:
            n += 1
            line = line[len(n_str):]
        
        ret.append(line)
    
    return ret

# FUNCTION TO FIND FIRST N
def find_first_n(line_arr: List[str]) -> int:
    line = line_arr[0] if line_arr[0].split(' ')[0].isnumeric() else line_arr[1]

    return int(line.split(' ')[0])

# FUNCTION TO TELL WHETHER LINES ARE NUMBERED
def is_numbered(line_arr: List[str]) -> bool:
    try:
        tokens = line_arr[0].split(' ')
        _ = int(tokens[0])
        return True
    except:
        return False

# FUNCTION TO COUNT SPACES
def count_spaces(s: str) -> int:
    ret = 0
    for c in s:
        if c == ' ':
            ret += 1
    
    return ret

# FUNCTION TO RETURN STRING BEFORE SUFFIX
def string_before(s: str, suffix: str, include: bool = False) -> str:
    l = len(suffix)
    for i in range(len(s), l, -1):
        if s[i-l :i] == suffix:
            return s[ :i] if include else s[ :i-l]
    
    raise Exception(f'Did not find suffix {suffix}')

# FUNCTION TO RETURN STRING AFTER PREFIX
def string_after(s: str, prefix: str, include: bool = False) -> str:
    l = len(prefix)
    for i in range(len(s) - l):
        if s[i: i+l] == prefix:
            return s[i: ] if include else s[i+l: ]
    
    raise Exception(f'Did not find prefix {prefix}.')

MAX_CUT_LEN = 8192
# TODO: Ask the AI to cut out the introduction?
possible_prefixes = [
    "P R O C E E D I N G S",
    "P R O C E E D I N G",
    "PROCEEDINGS",
    "PROCEEDING",
    "THE REPORTER",
    "(Formal Federal deposition read-in waived by all parties present",
    "Formal Federal deposition read-in waived by all parties present",
]
def cut_before_prefix(s: str) -> str:
    for prefix in possible_prefixes:
        l = len(prefix)
        cut_len = min((len(s) - l) // 2, MAX_CUT_LEN)
        for i in range(cut_len):
            if s[i: i+l] == prefix:
                return s[i+l: ]
        # print('did not find', prefix)
    
    return s

possible_suffixes = [
    "(End of deposition",
    "End of depositions",
    "* * * END OF DEPOSITION",
    "CHANGES AND SIGNATURE",
    "(Deposition concluded at",
    "Deposition concluded at",
    "I have us off record at",
    "(End of proceedings",
    "End of proceedings"
]
def cut_after_suffix(s: str) -> str:
    for suffix in possible_suffixes:
        l = len(suffix)
        cut_len = min((len(s) - l) // 2, MAX_CUT_LEN)
        for i in range(len(s), len(s) - cut_len, -1):
            if (s[i-l :i] == suffix):
                return s[ :i-l]
        # print('did not find', suffix)
    
    return s


# FUNCTION TO CUT TEXT WITH TOO MANY TOKENS
def cut_at_q(s: str) -> Tuple[str, str]:
    p = len(s) // 2

    while s[p: p+2] != 'Q.':
        p += 1
    
    return s[:p], s[p:]