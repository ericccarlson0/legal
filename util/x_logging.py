from datetime import datetime
from pathlib import Path
from util.directories import TASK_LOG_DIR, RES_LOG_DIR

import functools
import json
import os
import pickle
import re
import time
import uuid

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
            t = ob['end_time'] - ob['start_time']
            raise TaskFinishedException(f'{fpath} finished in {t} seconds.')
        else:
            start_time = ob['start_time']

            raise TaskInProgressException(f'{fpath} has been in progress from {start_time}')

def start_progress(fpath: str):
    ob = {
        'start_time': datetime.now().strftime('%H:%M:%S-%d:%m:%Y')
    }
    Path(fpath).touch()
    with open(fpath, 'w') as f:
        f.write(json.dumps(ob))

def end_progress(fpath: str):
    with open(fpath, 'r') as f:
        ob = json.loads(f.read())
        ob['end_time'] = datetime.now().strftime('%H:%M:%S-%d:%m:%Y')
    
    with open(fpath, 'w') as f:
        f.write(json.dumps(ob))

def log_execution(do_pickle: bool = True):
    def outer(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            arg_str = '-'.join(filename_str(arg) for arg in args)
            if len(arg_str) + len(func.__name__) > MAX_FILENAME_LEN:
                raise Exception(f'Function signature cannot be turned into a filename. {len(arg_str)} chars is too much for the arguments.')
            
            fname = func.__name__ + '-' + arg_str
            fpath = os.path.join(TASK_LOG_DIR, fname)

            check_in_progress(fpath)
            start_progress(fpath)

            res = func(*args, **kwargs)
            if do_pickle:
                save_res_pickle(res, func.__name__, *args)
                print('pickled', func.__name__)

            end_progress(fpath)

            return res
        
        return wrapper

    return outer
