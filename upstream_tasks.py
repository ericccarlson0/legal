import os
import re
import time

from celery import Celery
from downstream_tasks import _old_c_transcript_ocr_in_range
from pathlib import Path
from pdf2image import pdfinfo_from_path
from plaintiff.plaintiffs import *
from util.constants import *
from util.x_logging import log_execution
from util.summaries import get_file_summary, get_text_summary
from util.transcripts import *
from util.transcripts_aws import *

prompts_map = {
    "LIABILITY": [PLA_LIA_BP_PROMPT, PLA_LIA_BP_SUMMARY],
    # [PLA_LIA_FF_PROMPT, PLA_LIA_FF_SUMMARY],
    "DAMAGES": [PLA_DAM_BP_PROMPT, PLA_DAM_BP_SUMMARY],
    # [PLA_DAM_FF_PROMPT, PLA_DAM_FF_SUMMARY],
    "CREDIBILITY": [PLA_CRED_BP_PROMPT, PLA_CRED_BP_SUMMARY], 
    # [PLA_CRED_FF_PROMPT, PLA_CRED_FF_SUMMARY],
    "PROBLEMS": [PLA_PROB_BP_PROMPT, PLA_PROB_BP_SUMMARY],
    # [PLA_PROB_FF_PROMPT, PLA_PROB_FF_SUMMARY]
}

app = Celery(
    'upstream_tasks', # app.import_name,
    backend='redis://localhost:6379', # backend=app.config['CELERY_RESULT_BACKEND'],
    # backend='rpc://',
    broker='redis://localhost:6379', # app.config['CELERY_BROKER_URL'],
)

# class ContextTask(Celery.Task):
#     def __call__(self, *args, **kwargs):
#         with app.app_context():
#             return self.run(*args, **kwargs)

# celery_app.Task = ContextTask

# `celery -A your_application.celery worker`
# `celery multi start w1 -A proj -l INFO --pidfile=/var/run/celery/%n.pid --logfile=/var/log/celery/%n%I.log`
# celery_app.AsyncResult(res.id)

SMALL_TIME = 1
MEDIUM_TIME = 4
LONG_TIME = 16

@app.task(queue='q1')
@log_execution(TRANSCRIBE_TASK, True)
def c_transcript(file_id: int):
    # FIXME (REMOVE CHECK)
    if not check_transcript_p1_file(file_id):
        res = c_transcript_p1(file_id)
        # res.status == 'FAILURE' | 'SUCCESS'?
        print(f'result {res}', flush=True)

    # FIXME (REMOVE CHECK)
    if not check_transcript_p2_file(file_id):
        res = c_transcript_p2(file_id)
        # res.status == 'FAILURE' | 'SUCCESS'?
        print(f'result {res}', flush=True) 

# FULL TRANSCRIPT
@app.task(queue='q1')
def c_transcript_p1(file_id: int):
    pdf_fpath = pdf_fpath_of(file_id)
    if pdf_has_text(pdf_fpath):
        # FIXME
        transcript = transcript_compare_quarters_single(pdf_fpath)
    else:
        transcript = c_transcript_ocr(file_id)

    txt_full_fpath = os.path.join(TRANSCRIPT_FULL_DIR, f'{file_id}.txt')
    print(f'text full fpath {txt_full_fpath}')
    Path(txt_full_fpath).touch()
    with open(txt_full_fpath, 'w') as f:
        f.write(transcript)

    return True

# COND TRANSCRIPT
@app.task(queue='q1')
def c_transcript_p2(file_id: int):
    with open(os.path.join(TRANSCRIPT_FULL_DIR, f'{file_id}.txt'), 'r') as f:
        transcript = f.read()

    transcript = condensed_transcript(transcript)

    txt_cond_fpath = os.path.join(TRANSCRIPT_COND_DIR, f'{file_id}.txt')

    Path(txt_cond_fpath).touch()
    with open(txt_cond_fpath, 'w') as f:
        f.write(transcript)

    return True

@app.task(queue='q1')
def c_transcript_ocr(file_id: int):
    print('c_transcript_ocr')

    pages = textract_pdf_to_image(file_id)
    transcript = transcript_textract_pages(pages)

    return transcript

PAGE_GROUP_N = 8
# DEPRECATED
@app.task(queue='q1')
def _old_c_transcript_ocr(fname: str):
    pdfinfo = pdfinfo_from_path(fname)

    n_pages = pdfinfo["Pages"]
    print(f'n pages {n_pages}', flush=True)

    async_results = []
    for p in range(1, n_pages+1, PAGE_GROUP_N):
        print(f'{p} to {min(p+PAGE_GROUP_N-1, n_pages)}', flush=True)
        res = _old_c_transcript_ocr_in_range.delay(fname, p, min(p+PAGE_GROUP_N-1, n_pages))
        async_results.append(res)

        time.sleep(MEDIUM_TIME)
    
    n = len(async_results)

    transcripts = [None for _ in range(n)]
    c = 0
    while(c < n):
        ready_indices = set()
        for i, res in enumerate(async_results):
            if res is not None and res.ready():
                ready_indices.add(i)
        
        for i in ready_indices:
            transcripts[i] = async_results[i].result
            async_results[i] = None
        
        c += len(ready_indices)
        print('res count', c)

        time.sleep(MEDIUM_TIME)
    
    ret = ' '.join(transcripts)
    ret = re.sub('\s+', ' ', ret)

    return ret

@app.task(queue='q1')
@log_execution(SUMMARIZE_TASK, True)
def c_summarize(file_id: str, topic: str):
    if topic not in prompts_map:
        raise Exception(f"{topic} not in " + ",".join([k for k in prompts_map.keys()]))
    
    try:
        p1, p2 = prompts_map[topic]

        summary_intermediate = get_file_summary(file_id, prompt=p1)
        print(f'summary, stage 1, {len(summary_intermediate)}')
        summary_intermediate_fpath = os.path.join(SUMMARY_INT_DIR, f'{file_id}-{topic}.txt')
        with open(summary_intermediate_fpath, 'w') as f:
            f.write(summary_intermediate)

        summary = get_text_summary(summary_intermediate, p2, do_seg=False)
        print(f'summary, stage 2, {len(summary)}')
        summary_full_fpath = os.path.join(SUMMARY_FINAL_DIR, f'{file_id}-{topic}.txt')
        with open(summary_full_fpath, 'w') as f:
            f.write(summary)

    except Exception as e:
        return f"Error in generating summary from PDF.\n{e}"
    
    print('done, summary', flush=True)
    
    return True

if __name__ == '__main__':
    app.start()
