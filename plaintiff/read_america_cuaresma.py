
from plaintiff.plaintiffs import PLA_PROBLEMS_PROMPT
from util.summaries import get_pdf_summary

if __name__ == '__main__':
    ret = get_pdf_summary("America Cuaresma Full.pdf", PLA_PROBLEMS_PROMPT)
    print(ret)
