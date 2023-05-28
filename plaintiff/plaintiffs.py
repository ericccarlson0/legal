## PREFIXES

PLA_FF_SUMMARY_PREFIX = """
In the previous step, you summarized a sequence of sections of a deposition (of a plaintiff in a personal injury case).
Each summarized section is preceded by 'Part 1', 'Part 2', and so on.
"""

PLA_BP_SUMMARY_PREFIX = """
In the previous step, you summarized a sequence of sections of a deposition (of a plaintiff in a personal injury case).
Each summarized section consists of a set of important bullet-points.
In addition, each summarized section is preceded by 'Part 1', 'Part 2', and so on.
"""

## LIABILITY

# PLAINTIFF LIABILITY FREE-FORM PROMPT
PLA_LIA_FF_PROMPT = """
Your role is to extract any mention of liability in the following deposition (of a plaintiff in a personal injury case).
The fragment consists of a series of questions (preceded by "Q.") and answers (preceded by "A.").
Produce a summary of each mention of liability by the plaintiff.
"""

# PLAINTIFF LIABILITY BULLET-POINT PROMPT
PLA_LIA_BP_PROMPT = """
Your role is to extract any mention of liability in the following deposition (of a plaintiff in a personal injury case).
The fragment consists of a series of questions (preceded by "Q.") and answers (preceded by "A.").
Produce a bullet-point for each relevant mention of liability.
"""

PLA_LIA_FF_SUMMARY = PLA_FF_SUMMARY_PREFIX + """
Your role is to extract any mention of liability in the deposition;
use the following summarized sections to produce a final summary.
"""

PLA_LIA_BP_SUMMARY = PLA_BP_SUMMARY_PREFIX + """
Your role is to extract any mention of liability in the deposition;
use the following summarized sections to produce a final list of bullet-points.
"""

## DAMAGES

PLA_DAM_FF_PROMPT = """
Your role is to information related to damages in the following deposition (of a plaintiff in a personal injury case).
The fragment consists of a series of questions (preceded by "Q.") and answers (preceded by "A.").
Produce a summary of each mention of damages by the plaintiff.
"""

PLA_DAM_BP_PROMPT = """
Your role is to extract any mention of damages in the following deposition (of a plaintiff in a personal injury case).
The fragment consists of a series of questions (preceded by "Q.") and answers (preceded by "A.").
Produce a bullet-point for each relevant mention of damages.
"""

PLA_DAM_FF_SUMMARY = PLA_FF_SUMMARY_PREFIX + """
Your role is to extract any mention of damages in the deposition;
use the following summarized sections to produce a final summary.
"""

PLA_DAM_BP_SUMMARY = PLA_BP_SUMMARY_PREFIX + """
Your role is to extract any mention of damages in the deposition;
use the following summarized sections to produce a final list of bullet-points.
"""

## CREDIBILITY

PLA_CRED_FF_PROMPT = """
Your role is to extract information related to the credibility of the plaintiff in a personal injury case.
This is a fragment of a deposition which consists of a series of questions (preceded by "Q.") and answers (preceded by "A.").
Note, in particular, whether any questions are avoided or not answered directly.
"""

PLA_CRED_FF_SUMMARY = PLA_FF_SUMMARY_PREFIX + """
Your role is to extract information related to the credibility of the plaintiff in the deposition (for instance, whether questions are avoided or not answered directly);
use the following summarized sections to produce a final summary.
"""

PLA_CRED_BP_PROMPT = """
Your role is to extract information related to the credibility of the plaintiff in a personal injury case.
The following deposition fragment consists of a series of questions (preceded by "Q.") and answers (preceded by "A.").
Produce a bullet point for each relevant piece of information.
Note, in particular, whether any questions are avoided or not answered directly.
"""

PLA_CRED_BP_SUMMARY = PLA_BP_SUMMARY_PREFIX + """
Your role is to extract information related to the credibility of the plaintiff in the deposition (for instance, whether questions are avoided or not answered directly);
use the following summarized sections to produce a final list of bullet-points.
"""

## PROBLEMS

PLA_PROB_FF_PROMPT = """
The following is a fragment of a deposition which consists of a series of questions (preceded by "Q.") and answers (preceded by "A.").
Tell whether there are any "major problems" in the answers of the plaintiff.
In particular, note whether the plaintiff had pre-existing conditions, previous or subsequent collisions, alcohol or drug use (time of the collision), delay in treatment, or gaps in treatment.
"""

PLA_PROB_FF_SUMMARY = PLA_FF_SUMMARY_PREFIX + """
Your role is to extract the "major problems" (pre-existing conditions, previous or subsequent collisions, alcohol or drug use, and delay or gaps in treatment) in the answers of the plaintiff;
use the following summarized sections to produce a final summary.
"""

PLA_PROB_BP_PROMPT = """
The following is a fragment of a deposition which consists of a series of questions (preceded by "Q.") and answers (preceded by "A.").
Produce a bullet-point for each "major problem" in the answers of the plaintiff.
In particular, note whether the plaintiff had pre-existing conditions, previous or subsequent collisions, alcohol or drug use (time of the collision), delay in treatment, or gaps in treatment.
"""

PLA_PROB_BP_SUMMARY = """
Your role is to extract the "major problems" (pre-existing conditions, previous or subsequent collisions, alcohol or drug use, and delay or gaps in treatment) in the answers of the plaintiff;
use the following summarized sections to produce a final list of bullet-points.
"""

DEPO_DIR = "/Users/ericcarlson/Desktop/Reyes Browne/Depos/Plaintiff"
