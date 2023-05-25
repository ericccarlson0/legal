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
