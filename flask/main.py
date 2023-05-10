import os
import re
import requests
from flask import Flask, request
from flask_cors import CORS
from util.summaries import pdf_summary
from sf.docrio import get_signed_url, upload_base64
from plaintiff.plaintiffs import PLA_LIABILITY_PROMPT, PLA_DAMAGES_PROMPT, PLA_CREDIBILITY_PROMPT, PLA_MAJOR_PROBLEMS_PROMPT

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
    if not os.path.isfile(fname):
        signed_url = get_signed_url(file_id)
        response = requests.get(signed_url, allow_redirects=True)
        
        ct = response.headers.get('content-type')
        if ct != 'application/pdf':
            return "not application/pdf"

        open(fname, 'wb').write(response.content)

    # REMOVED POLICY_LIMIT, HEALTH_SYMPTOMS
    if topic == "LIABILITY":
        prompt = PLA_LIABILITY_PROMPT
    elif topic == "DAMAGES":
        prompt = PLA_DAMAGES_PROMPT
    elif topic == "CREDIBILITY":
        prompt = PLA_CREDIBILITY_PROMPT
    elif topic == "MAJOR_PROBLEMS":
        prompt = PLA_MAJOR_PROBLEMS_PROMPT

    try:
        return pdf_summary(fname, prompt=prompt)
    except:
        return "Error in generating summary from PDF."

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
