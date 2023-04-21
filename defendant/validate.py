from defendant.defendants import DEPO_DIR
from util.str_util import cut_after_suffix, cut_before_prefix
from util.transcripts import depo_transcript

args = [
  ["Corina Olivarez Full.pdf", 50, 50],
  ["Grace Bergeron Full.pdf", 0, 0],
  ["Abel Montes de Oca Full.pdf", 75, 75],
  ["Bridget Clower Full.pdf", 0, 0]
]

for i, (fname, t, b) in enumerate(args):
  print(f'({i}) {fname}')
  transcript = depo_transcript(DEPO_DIR, fname, top_margin=t, bottom_margin=b)
  prev_len = len(transcript)
  print(prev_len)

  transcript = cut_after_suffix(transcript)
  if len(transcript) == prev_len:
    print(transcript)
  prev_len = len(transcript)
  print(prev_len)

  transcript = cut_before_prefix(transcript)
  if len(transcript) == prev_len:
    print(transcript)
  prev_len = len(transcript)
  print(prev_len)
