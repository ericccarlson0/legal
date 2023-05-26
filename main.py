from flask import Flask, request, jsonify
from flask_cors import CORS
from prompts import bp as prompts_bp
from sf.docrio import check_pdf_download, get_signed_url, upload_base64
from tasks import c_transcript, c_summarize
from util.transcripts import check_transcript
from util.summaries import check_summary

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
    
    summary = check_summary(file_id, topic)
    if not summary:
        c_summarize.delay(file_id, topic)
        return { "finished": False }

    return { 
        "finished": True,
        "summary": summary,
    }

@app.route("/internal/transcribe", methods=['POST'])
def transcribe():
    form_data = request.form
    file_id = form_data["id"]

    try:
        check_pdf_download(file_id)
    except Exception as e:
        message = f"File Download did not work. (Is the FileInfo ID incorrect?)\n{e}"
        return jsonify({ "error": message })

    finished = check_transcript(file_id)

    if not finished:
        print('No transcript.')
        c_transcript.delay(file_id)
        return jsonify({ "finished": False })

    return jsonify({ "finished": True })

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
