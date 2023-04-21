
from plaintiff.plaintiffs import PLA_MAJOR_PROBLEMS_PROMPT
from util.summaries import pdf_summary

if __name__ == '__main__':
    ret = pdf_summary("America Cuaresma Full.pdf", PLA_MAJOR_PROBLEMS_PROMPT)
    print(ret)
