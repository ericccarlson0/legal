DEF_LIABILITY_PROMPT = """
The following transcript is a fragment of the deposition of a defendent in a personal injury case.
It consists of a series of questions (preceded by "Q.") and answers (preceded by "A.").
Your role is to extract any mention of liability in the deposition and, if there is such a mention, to quote the relevant sentence(s).
(And if there is no mention of liability, say so.)
"""

DEF_JURY_SENTIMENT_PROMPT = """
The following transcript is a deposition in a personal injury case.
It consists of a series of questions (marked by "Q.") and answers (marked by "A.").
Tell how the witness would look to a jury (would a jury favor or disfavor them?).
"""

DEF_JURY_SENTIMENT_PROMPT_2 = """"
The following transcript is a fragment of a deposition in a personal injury case.
It consists of a series of questions (marked "Q.") and answers (marked "A.").
Based on how the witness would look to a jury, score the witness on a scale of 1 to 10.
"""

DEPO_DIR = "/Users/ericcarlson/Desktop/Reyes Browne/Depos/Defendant"
