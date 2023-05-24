from flask import Flask, request, jsonify
from flask_cors import CORS
from plaintiff.plaintiffs import *
from prompts import bp as prompts_bp
from sf.docrio import check_pdf_download, get_signed_url, upload_base64
from tasks import celery_app
from util.summaries import get_file_summary, get_text_summary
from util.transcripts import check_transcript

prompts_map = {
    "LIABILITY": [PLA_LIA_BP_PROMPT, PLA_LIA_BP_SUMMARY],
    # [PLA_LIA_FF_PROMPT, PLA_LIA_FF_SUMMARY],
    "DAMAGES": [PLA_DAM_BP_PROMPT, PLA_DAM_BP_SUMMARY],
    # [PLA_DAM_FF_PROMPT, PLA_DAM_FF_SUMMARY],
    "CREDIBILITY": [PLA_CRED_BP_PROMPT, PLA_CRED_BP_SUMMARY], 
    # [PLA_CRED_FF_PROMPT, PLA_CRED_FF_SUMMARY],
    "PROBLEMS": [PLA_PROB_BP_PROMPT, PLA_PROB_BP_SUMMARY],
    # [PLA_PROB_FF_PROMPT, PLA_PROB_FF_SUMMARY]
}

app = Flask(__name__)
app.register_blueprint(prompts_bp, url_prefix="/internal/prompts")
# print(app.url_map)
CORS(app)

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

    if topic not in prompts_map:
        return f"{topic} not in " + ",".join([k for k in prompts_map.keys()])
    
    try:
        p1, p2 = prompts_map[topic]
        summary_in_parts = get_file_summary(file_id, prompt=p1)

        return get_text_summary(summary_in_parts, p2, do_seg=False)

    except Exception as e:
        return f"Error in generating summary from PDF.\n{e}"

@app.route("/internal/transcribe", method=['POST'])
def transcribe():
    form_data = request.form
    file_id = form_data["id"]

    try:
        check_pdf_download(file_id)
    except Exception as e:
        # FIXME: JSON
        return f"File Download did not work. (Is the FileInfo ID incorrect?)\n{e}"

    try:
        finished = check_transcript(file_id)
    except Exception as e:
        # FIXME: JSON
        return f"File Transcript did not work.\n{e}"
    
    if finished:
        return jsonify({ finished: True })

    print('async celery transcript')
    celery_app.transcript.delay(file_id) # FIXME
    
    return jsonify({ finished: False })

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
