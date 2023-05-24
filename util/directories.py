import os

LEGAL_BASE_DIR = os.getenv('LEGAL_BASE_DIR')

FILE_INFO_DIR = os.path.join(LEGAL_BASE_DIR, 'downloads')
if not os.path.isdir(FILE_INFO_DIR):
    os.mkdir(FILE_INFO_DIR)
TRANSCRIBE_TEXT_DIR = os.path.join(LEGAL_BASE_DIR, 'transcripts')
if not os.path.isdir(TRANSCRIBE_TEXT_DIR):
    os.mkdir(TRANSCRIBE_TEXT_DIR)
