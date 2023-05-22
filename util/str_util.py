from typing import List, Tuple

MAX_CUT_LEN = 8192

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

possible_prefixes = [
    "P R O C E E D I N G S",
    "P R O C E E D I N G",
    "PROCEEDINGS",
    "PROCEEDING",
    "THE REPORTER",
    "(On the record",
    "On the record",
    "(Formal Federal deposition read-in waived by all parties present",
    "Formal Federal deposition read-in waived by all parties present",
    "THE REPORTER: We are on the record",
    "COURT REPORTER: Today's date",
    "The witness will now be sworn in",
]
def cut_before_prefix(s: str) -> str:
    cut = len(s) // 2
    s_pre = s[:-cut]
    s_pre_rev = s_pre[::-1]

    min_x = 0
    min_prefix = ''

    for prefix in possible_prefixes:
        prefix_rev = prefix[::-1]
        x = s_pre_rev.find(prefix_rev)
        if x < min_x:
            min_x = x
            min_prefix = prefix

        # l = len(prefix)
        # cut_len = (len(s) - l) // 2

        # for i in range(max_prefix, cut_len):
        #     if s[i: i+l] == prefix:
        #         max_i = i
        #         max_prefix = prefix
        #         break # return s[i+l: ]
    
    print('prefix', min_prefix)
    l = len(min_prefix)

    c = cut+min_x+l
    # if c > 64:
    #     print(s[-c:-c+64])
    print(len(s), '->', len(s) - c, 'by removing prefix')

    return s[ :-c]

possible_suffixes = [
    "THE REPORTER: Off the record",
    "(End of deposition",
    "End of depositions",
    "* * * END OF DEPOSITION",
    "CHANGES AND SIGNATURE",
    "(Deposition concluded at",
    "Deposition concluded at",
    "I have us off record at",
    "(End of proceedings",
    "End of proceedings",
    "Deposition adjourned",
    "The deposition concluded",
    "CHANGES AND SIGNATURE",
]
def cut_after_suffix(s: str) -> str:
    cut = len(s) // 2
    s_end = s[cut:]

    min_x = len(s_end)
    min_suffix = ''

    for suffix in possible_suffixes:
        x = s_end.find(suffix)
        if x < min_x:
            min_x = x
            min_suffix = suffix

        # l = len(suffix)
        # cut_len = (len(s) - l) // 2

        # for i in range(min_i, len(s) - cut_len, -1):
        #     if (s[i-l :i] == suffix):
        #         min_i = i
        #         min_suffix = suffix
        #         break # return s[ :i-l]
    
    print('suffix', min_suffix)
    l = len(min_suffix)

    c = cut+min_x+l
    # if c >= 64:
    #     print(s[c-64:c], '...')
    print(len(s), '->', len(s) - c, 'by removing suffix')
    
    return s[c: ]


# FUNCTION TO CUT TEXT WITH TOO MANY TOKENS
def cut_at_q(s: str) -> Tuple[str, str]:
    p = len(s) // 2

    while s[p: p+2] != 'Q.':
        p += 1
    
    return s[:p], s[p:]