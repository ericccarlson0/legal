import os
import time

from plaintiff.plaintiffs import DEPO_DIR
from pypdf import PdfReader
from util.str_util import cut_after_suffix, cut_before_prefix
from util.transcripts import transcript_single, transcript_quarters
from upstream_tasks import c_transcript

args = [
    ["America Cuaresma Full.pdf", 75, 75, 75, 75, True],
    # ["Brandon Fields Full.pdf", 50, 50, 50, 50, False], # FIXME (no text through PyPDF)
    ["Edwin Munoz Martinez.pdf", 75, 75, 75, 75, True],
    # ["Fermin Leija Full.pdf", 50, 50, 50, 50, False], # FIXME (no text through PyPDF)
    ["Jamie Olivarez Full.pdf", 50, 50, 50, 50, False],
    # ["Kaland Fernanders Full.pdf", 50, 50, 50, 50, False], # FIXME (no text through PyPDF)
    ["Kevin Scott Harris Full.pdf", 50, 50, 50, 50, False],
    ["Michael Diles Full.pdf", 75, 75, 75, 75, True],
    # ["Patrick Parker Full.pdf", 50, 50, 50, 50, False], # FIXME (bad quality? OBSTRUCTED)
    # ["Scott Lund Full.pdf", 0, 0, 0, 0, False], # FIXME (bad quality?)
    # ["Sofia Tames Full.pdf", 0, 0, 0, 0, False], # FIXME (bad quality?)
    # ["Tiwan Spencer Full.pdf", 0, 0, 0, 0, False], # FIXME (no text through PyPDF)
    # ["Victoria Williams Full.pdf", 0, 0, 0, 0, False] # FIXME (pypdf.errors.DependencyError: PyCryptodome is required for AES algorithm)
]

fnames = [
    "America Cuaresma Full.pdf",
    "Brandon Fields Full.pdf",
    "Edwin Munoz Martinez.pdf",
    "Fermin Leija Full.pdf",
    "Jamie Olivarez Full.pdf",
    "Kaland Fernanders Full.pdf",
    "Kevin Scott Harris Full.pdf",
    "Michael Diles Full.pdf",
    "Patrick Parker Full.pdf",
    "Scott Lund Full.pdf",
    "Sofia Tames Full.pdf", 
    "Tiwan Spencer Full.pdf",
]

ids = [
    'a2O6e000003dBlrEAE',
    'a2O6e000003dBn4EAE',
    'a2O6e000003dsGIEAY',
    'a2O6e000003g4t0EAA',
    'a2O6e000003eFHdEAM',
    'a2O6e000003dRRGEA2',
    'a2O6e000003eH4WEAU',
    'a2O6e000003eiD1EAI',
    'a2O6e000003dpjaEAA',
    'a2O6e000003fj0MEAQ',
    'a2O6e000003eH5KEAU'
]

prev_t = time.time()
for i, id in enumerate(ids):
    print('...')
    
    res = c_transcript(id)

    t = time.time()
    dt = t - prev_time
    prev_time = t

    print(i, dt)

# for i, (fname, t, b, r, l, quarters) in enumerate(args):
#     print(f'({i}) {fname}')
#     if quarters:
#         transcript = depo_transcript_quarters(os.path.join(DEPO_DIR, fname), t, b, r, l)
#     else:
#         transcript = depo_transcript(os.path.join(DEPO_DIR, fname), t, b, r, l)
#     prev_len = len(transcript)
#     print(prev_len)

#     transcript = cut_after_suffix(transcript)
#     if len(transcript) == prev_len:
#         print('Did not find suffix')
#     prev_len = len(transcript)
#     print(prev_len)

#     transcript = cut_before_prefix(transcript)
#     if len(transcript) == prev_len:
#         print('Did not find prefix')
#     prev_len = len(transcript)
#     print(prev_len)

#     print(transcript[:256] + '...')
#     print('...' + transcript[-256:])
