PLA_LIABILITY_PROMPT = """
Extract information related to damages from the deposition of a plaintiff in a personal injury case.
It consists of a series of questions (preceded by "Q.") and answers (preceded by "A.").
Your role is to extract any mention of liability in the deposition.
If the plaintiff mentions liability, quote the passage.
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

PLA_CREDIBILITY_PROMPT = """
Extract information related to the credibility of the plaintiff in a personal injury case.
This is fragment of a deposition which consists of a series of questions (preceded by "Q.") and answers (preceded by "A.").
Tell whether the plaintiff is being truthful.
In particular, note questions which are avoided or are not answered directly.
"""

PLA_MAJOR_PROBLEMS_PROMPT = """
This is a fragment of a deposition which consists of a series of questions (preceded by "Q.") followed by the plaintiff's answers (preceded by "A.").
Tell whether there are any major inconsistencies in the answers of the plaintiff.
In particular, note whether the plaintiff had relevant pre-existing conditions, previous or subsequent collisions, alcohol or drug use (time of the collision), delay in treatment, or gaps in treatment.
"""

# PLA_HEALTH_SYMPTOMS_PROMPT = """
# Extract information related to the health and symptoms of the plaintiff in a personal injury case.
# This is a fragment of a deposition which constists of a series of questions (preceded by "Q.") and answers (preceded by "A.").
# Report any mention of health or symptoms by the plaintiff.
# """

DEPO_DIR = "/Users/ericcarlson/Downloads/Depos/Plaintiff"
