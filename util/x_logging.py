from datetime import datetime
from pathlib import Path
from util.constants import *

import functools
import json
import os
import pickle
import re

# FIXME: ARBITRARY
MAX_FILENAME_LEN = 256

class TaskInProgressException(Exception):
    pass

class TaskFinishedException(Exception):
    pass

def filename_str(arg: str):
    ret = arg.replace(' ', '-').replace('_', '-').replace('/', '_')
    ret = re.sub(r'[^a-zA-Z0-9-_.]', '', ret)

    return ret

def save_res_pickle(res, dname, *args):
    fname = '-'.join(filename_str(arg) for arg in args)
    fname += '-' + datetime.now().strftime('%H:%M:%S-%d:%m:%Y')
    fname += '.pkl'

    dir = os.path.join(RES_LOG_DIR, dname)
    if not os.path.isdir(dir):
        os.mkdir(dir)

    with open(os.path.join(dir, fname), 'wb') as oup:
        pickle.dump(res, oup, pickle.HIGHEST_PROTOCOL)

def check_in_progress(fpath: str):
    if not os.path.isfile(fpath):
        return
    
    with open(fpath, 'r') as f:
        ob = json.loads(f.read())
        if 'end_time' in ob:
            raise TaskFinishedException(f'{fpath} already finished')
        else:
            start_time = ob['start_time']

            raise TaskInProgressException(f'{fpath} has been in progress from {start_time}')

def start_progress(fpath: str):
    ob = {
        'start_time': datetime.now().strftime('%H:%M:%S-%d:%m:%Y'),
        'progress': 0.0
    }
    Path(fpath).touch()
    with open(fpath, 'w') as f:
        f.write(json.dumps(ob))

def end_progress(fpath: str):
    with open(fpath, 'r') as rf:
        ob = json.loads(rf.read())
        ob['progress'] = 1.0
        ob['end_time'] = datetime.now().strftime('%H:%M:%S-%d:%m:%Y')
    
    with open(fpath, 'w') as wf:
        wf.write(json.dumps(ob))

def log_progress(fpath: str, progress: float):
    # TODO: if not os.path.isfile(fpath):

    with open(fpath, 'r') as rf:
        ob = json.loads(rf.read())
        ob['progress'] = progress
    
    with open(fpath, 'w') as wf:
        wf.write(json.dumps(ob))

def get_progress(fpath: str):
    ret = 0.0
    with open(fpath, 'r') as rf:
        ob = json.loads(rf.read())
        ret = ob['progress']
    
    return ret

# The unique path used for logging a function.
def get_unique_filepath(funcname, *args):
    arg_str = '-'.join(filename_str(arg) for arg in args)
    if len(arg_str) + len(funcname) > MAX_FILENAME_LEN:
        raise Exception(f'Function signature cannot be turned into a filename. {len(arg_str)} chars is too much for the arguments.')
    filename = funcname + '-' + arg_str

    return os.path.join(TASK_LOG_DIR, filename)

def log_execution(label: str, do_pickle: bool = True):
    def outer(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            fpath = get_unique_filepath(label, *args) # **kwargs

            check_in_progress(fpath)
            start_progress(fpath)

            res = func(*args, **kwargs)
            if do_pickle:
                save_res_pickle(res, label, *args)

            end_progress(fpath)

            return res
        
        return wrapper

    return outer
