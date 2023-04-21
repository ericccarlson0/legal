from defendant.defendants import DEPO_DIR
from util.str_util import cut_after_suffix, cut_before_prefix
from util.transcripts import depo_transcript

args = [
  ["Corina Olivarez Full.pdf", 50, 50, 0, 0],
  ["Grace Bergeron Full.pdf", 0, 0, 0, 0],
  ["Abel Montes de Oca Full.pdf", 75, 75, 0, 0],
  ["Bridget Clower Full.pdf", 0, 0, 0, 0]
]

for i, (fname, t, b, r, l) in enumerate(args):
  print(f'({i}) {fname}')
  transcript = depo_transcript(DEPO_DIR, fname, t, b, r, l)
  prev_len = len(transcript)
  print(prev_len)

  transcript = cut_after_suffix(transcript)
  if len(transcript) == prev_len:
    print('Did not find suffix.')
  prev_len = len(transcript)
  print(prev_len)

  transcript = cut_before_prefix(transcript)
  if len(transcript) == prev_len:
    print('Did not find prefix.')
  prev_len = len(transcript)
  print(prev_len)
