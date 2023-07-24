from util.constants import *
import shutil

for dir in [TRANSCRIPT_FULL_DIR, TRANSCRIPT_COND_DIR, SUMMARY_INT_DIR, SUMMARY_FINAL_DIR, TASK_LOG_DIR]:
    shutil.rmtree(dir)
