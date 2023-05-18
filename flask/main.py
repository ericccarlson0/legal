from flask import Flask, request
from flask_cors import CORS
from util.summaries import get_pdf_summary, get_text_summary
from sf.docrio import check_download, get_signed_url, upload_base64
from plaintiff.plaintiffs import PLA_LIABILITY_PROMPT, PLA_DAMAGES_PROMPT, PLA_CREDIBILITY_PROMPT, PLA_PROBLEMS_PROMPT
from plaintiff.plaintiffs import PLA_LIABILITY_SUMMARY, PLA_DAMAGES_SUMMARY, PLA_CREDIBILITY_SUMMARY, PLA_PROBLEMS_SUMMARY

prompts_map = {
    "LIABILITY": [PLA_LIABILITY_PROMPT, PLA_LIABILITY_SUMMARY],
    "DAMAGES": [PLA_DAMAGES_PROMPT, PLA_DAMAGES_SUMMARY],
    "CREDIBILITY": [PLA_CREDIBILITY_PROMPT, PLA_CREDIBILITY_SUMMARY],
    "PROBLEMS": [PLA_PROBLEMS_PROMPT, PLA_PROBLEMS_SUMMARY]
}

app = Flask(__name__)
CORS(app)

SAMPLE_TEXT = """
Q. All right. Good morning. My name is Robin Ivey. I'm the attorney who is going to be taking your deposition this morning, and I represent the defendant in this lawsuit. Do you understand who I am and who I represent?
A. No. I don't know whom you are representing.
Q. Okay. So you understand that you had filed the lawsuit, correct?
A. Yes.
Q. Okay. And then that you sued a person, correct?
A. Yes.
Q. Okay. So I represent that person.
A. That's okay.
Q. All right. So you understand who I am and who I represent?
A. Yes. Yes. Yes. Now, I understand.
Q. Okay. Have you ever had your deposition taken before?
A. No. No.
Q. Okay. So I'm going to go over a few rules. So, Number One, you understand that you're under oath, right? 
. Correct. And I understand that perfectly well.
Q. And you understand that your testimony today would be the same kind of testimony if you were in front of a judge or a jury?
A. Of course. Yes, of course. Very perfectly well, yes.
"""

@app.route("/internal", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return "index v4"

    elif request.method == 'POST':
        form_data = request.form
        textblock = "\n".join([k for k in form_data])
        
        return "you posted " + textblock

@app.route("/internal/summarize", methods=['GET'])
def summarize_info():
    return "Pass a FileInfo Record Id and Topic to summarize the file."

@app.route("/internal/summarize", methods=['POST'])
def summarize():
    form_data = request.form

    file_id = form_data["id"]
    topic = form_data["topic"]
    
    fname = file_id + '.pdf'
    try:
        check_download(file_id, fname)
    except Exception as e:
        return f"File Download did not work. (Is the FileInfo ID incorrect?)\n{e}"

    if topic not in prompts_map:
        return f"{topic} not in " + ",".join([k for k in prompts_map.keys])
    
    try:
        p1, p2 = prompts_map[topic]
        summary_in_parts = get_pdf_summary(fname, prompt=p1)
        return get_text_summary(summary_in_parts, p2, do_seg=False)

    except Exception as e:
        return f"Error in generating summary from PDF.\n{e}"

@app.route("/internal/docrio/signed_url", methods=['GET'])
def docrio_signed_url():
    file_id = request.args.get("id", default=0, type=int)

    if file_id == 0:
        return "no file ID received from GET request"
    
    return get_signed_url(file_id)

@app.route("/internal/docrio/create", methods=['POST'])
def docrio_create():
    form_data = request.form

    fname = form_data['fname']
    base64_str = form_data['base64_str']
    content_type = form_data['content_type']

    return upload_base64(fname, base64_str, content_type=content_type)
