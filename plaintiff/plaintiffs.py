PLA_FF_SUMMARY_PREFIX = """
In the previous step, you summarized a sequence of sections of a deposition (of a plaintiff in a personal injury case).
Each summarized section is preceded by 'Part 1', 'Part 2', and so on.
"""

PLA_BP_SUMMARY_PREFIX = """
In the previous step, you summarized a sequence of sections of a deposition (of a plaintiff in a personal injury case).
Each summarized section consists of a set of important bullet-points.
In addition, each summarized section is preceded by 'Part 1', 'Part 2', and so on.
"""

# PLAINTIFF LIABILITY FREE-FORM PROMPT
PLA_LIA_FF_PROMPT = """
Your role is to extract any mention of liability in the following deposition (of a plaintiff in a personal injury case).
The plaintiff's deposition consists of a series of questions (preceded by "Q.") and answers (preceded by "A.").
Produce a summary of each mention of liability (and quote passages if possible).
"""

# PLAINTIFF LIABILITY BULLET-POINT PROMPT
PLA_LIA_BP_PROMPT = """
Your role is to extract any mention of liability in the following deposition (of a plaintiff in a personal injury case).
The plaintiff's deposition consists of a series of questions (preceded by "Q.") and answers (preceded by "A.").
Produce a list of bulled-points with each relevant mention of liability (and quote passages if possible).
"""

PLA_LIA_FF_SUMMARY = PLA_FF_SUMMARY_PREFIX + """
Your role is to extract any mention of liability in the deposition, using the following summarized sections to produce a final summary.
"""

PLA_LIA_BP_SUMMARY = PLA_BP_SUMMARY_PREFIX + """
Your role is to extract any mention of liability in the deposition, using the following summarized sections to produce a final summary.
"""

# PLA_POLICY_LIMIT_PROMPT = """
# Extract information related to policy limits from the deposition of a plaintiff in a personal injury case.
# The fragment consists of a series of questions (preceded by "Q.") and answers (preceded by "A.").
# Tell whether there is any mention of policy limits and, if so, summarize it.
# """

PLA_DAMAGES_PROMPT = """
Extract information related to damages from the deposition of a plaintiff in a personal injury case.
The fragment consists of a series of questions (preceded by "Q.") and answers (preceded by "A.").
Summarize the damages mentioned by the plaintiff.
"""

PLA_DAMAGES_SUMMARY = PLA_FF_SUMMARY_PREFIX + "Your role is to extract any mention of damages in the deposition by combining these summaries into a smaller summary."

PLA_CREDIBILITY_PROMPT = """
Extract information related to the credibility of the plaintiff in a personal injury case.
This is a fragment of a deposition which consists of a series of questions (preceded by "Q.") and answers (preceded by "A.").
Tell whether the plaintiff is being truthful.
In particular, note questions which are avoided or are not answered directly.
"""

PLA_CREDIBILITY_SUMMARY = PLA_FF_SUMMARY_PREFIX + "Your role is to extract information related to the credibility of the plaintiff (for instance, which questions are avoided or not answered directly) by combining these summaries into a smaller summary."

PLA_PROBLEMS_PROMPT = """
This is a fragment of a deposition which consists of a series of questions (preceded by "Q.") followed by the plaintiff's answers (preceded by "A.").
Tell whether there are any major inconsistencies in the answers of the plaintiff.
In particular, note whether the plaintiff had relevant pre-existing conditions, previous or subsequent collisions, alcohol or drug use (time of the collision), delay in treatment, or gaps in treatment.
"""

PLA_PROBLEMS_SUMMARY = PLA_FF_SUMMARY_PREFIX + "Your role is to extract information related to major inconsistencies (e.g. pre-existing conditions, previous or subsequent collisions, alcohol or drug use, and delay or gaps in treatment) by combining these summaries into a smaller summary."

# PLA_HEALTH_SYMPTOMS_PROMPT = """
# Extract information related to the health and symptoms of the plaintiff in a personal injury case.
# This is a fragment of a deposition which constists of a series of questions (preceded by "Q.") and answers (preceded by "A.").
# Report any mention of health or symptoms by the plaintiff.
# """

DEPO_DIR = "/Users/ericcarlson/Downloads/Depos/Plaintiff"
