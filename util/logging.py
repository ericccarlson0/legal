from util.directories import TASK_LOG_DIR
from pathlib import Path

import functools
import json
import os
import time

# FIXME: ARBITRARY
MAX_FILENAME_LEN = 256

class TaskInProgressException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

def check_in_progress(fpath: str):
    if not os.path.isfile(fpath):
        return
    
    with open(fpath, 'r') as f:
        ob = json.loads(f.read())
        if 'end_time' not in ob:
            start_time = ob['start_time']
            prog_time = time.time() - start_time

            raise TaskInProgressException(f'{fpath} has been in progress for {prog_time} seconds.')

def start_progress(fpath: str, t: float):
    ob = {
        'start_time': t
    }
    Path(fpath).touch()
    with open(fpath, 'w') as f:
        f.write(json.dumps(ob))

def end_progress(fpath: str, t: float):
    with open(fpath, 'r') as f:
        ob = json.loads(f.read())
        ob['end_time'] = t
    
    with open(fpath, 'w') as f:
        f.write(json.dumps(ob))

def log_execution_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        arg_str = '-'.join(args)
        if len(arg_str) + len(func.__name__) > MAX_FILENAME_LEN:
            raise Exception(f'Function signature cannot be turned into a filename. {len(arg_str)} chars is too much for the arguments.')
        
        fname = func.__name__ + '-' + arg_str
        fpath = os.path.join(TASK_LOG_DIR, fname)

        check_in_progress(fpath)
        start_progress(fpath, time.time())

        res = func(*args, **kwargs)

        end_progress(fpath, time.time())
        # print(f'{func.__name__} took {t: .4f} seconds')

        return res
    
    return wrapper
