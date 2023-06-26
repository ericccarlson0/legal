import os

LEGAL_BASE_DIR = os.getenv('LEGAL_BASE_DIR')

FILE_INFO_DIR = os.path.join(LEGAL_BASE_DIR, 'downloads')
if not os.path.isdir(FILE_INFO_DIR):
    os.mkdir(FILE_INFO_DIR)

TRANSCRIPT_FULL_DIR = os.path.join(LEGAL_BASE_DIR, 'transcripts-full')
if not os.path.isdir(TRANSCRIPT_FULL_DIR):
    os.mkdir(TRANSCRIPT_FULL_DIR)

TRANSCRIPT_COND_DIR = os.path.join(LEGAL_BASE_DIR, 'transcripts-cond')
if not os.path.isdir(TRANSCRIPT_COND_DIR):
    os.mkdir(TRANSCRIPT_COND_DIR)

SUMMARY_INT_DIR = os.path.join(LEGAL_BASE_DIR, 'summaries-int')
if not os.path.isdir(SUMMARY_INT_DIR):
    os.mkdir(SUMMARY_INT_DIR)

SUMMARY_FINAL_DIR = os.path.join(LEGAL_BASE_DIR, 'summaries-final')
if not os.path.isdir(SUMMARY_FINAL_DIR):
    os.mkdir(SUMMARY_FINAL_DIR)

LOG_DIR = os.path.join(LEGAL_BASE_DIR, 'logs')
if not os.path.isdir(LOG_DIR):
    os.mkdir(LOG_DIR)

TASK_LOG_DIR = os.path.join(LOG_DIR, 'tasks')
if not os.path.isdir(TASK_LOG_DIR):
    os.mkdir(TASK_LOG_DIR)

RES_LOG_DIR = os.path.join(LOG_DIR, 'res')
if not os.path.isdir(RES_LOG_DIR):
    os.mkdir(RES_LOG_DIR)

IMG_DIR = os.getenv('DEPO_IMG_DIR')
PLA_IMG_DIR = os.path.join(IMG_DIR, 'Plaintiff')
DEF_IMG_DIR = os.path.join(IMG_DIR, 'Defendant')
