import os
import re
import requests

from auth.jwt import get_token
from flask import Flask, request
from flask_cors import CORS
from util.summaries import pdf_summary
from plaintiff.plaintiffs import PLA_LIABILITY_PROMPT, PLA_DAMAGES_PROMPT, PLA_CREDIBILITY_PROMPT, PLA_MAJOR_PROBLEMS_PROMPT

app = Flask(__name__)
CORS(app)

TOKEN = get_token()

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

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return "index v4"

    elif request.method == 'POST':
        form_data = request.form
        textblock = [k for k in form_data][0]
        
        return "you posted " + textblock

@app.route("/summarize", methods=['GET'])
def summarize_info():
    return "Pass a FileInfo Record Id and Topic to summarize the file."

@app.route("/summarize", methods=['POST'])
def summarize():
    form_data = request.form

    file_id = form_data["id"]
    topic = form_data["topic"]
    
    fname = file_id + '.pdf'
    if not os.path.isfile(fname):
        headers = {
            'accept': 'application/json',
            'Authorization': 'Bearer ' + TOKEN
        }
        response = requests.get('https://api.339287139604.genesisapi.com/v1/files?Id=' + file_id,
                                headers=headers)
        signedUrl = response.json()['Records'][0]['SignedUrl']
        response = requests.get(signedUrl, allow_redirects=True)
        
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
