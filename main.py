from flask import Flask, request, jsonify
from flask_cors import CORS
from prompts import bp as prompts_bp
from sf.docrio import check_pdf_download, get_signed_url, upload_base64
from upstream_tasks import c_transcript, c_summarize
from util.constants import *
from util.transcripts import check_transcript
from util.summaries import check_summary
from util.x_logging import get_progress, get_unique_filepath

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
    print(f'/internal/summarize {file_id} {topic}', flush=True)
    
    return _summarize(file_id, topic)

def _summarize(file_id, topic):
    res = check_summary(file_id, topic)
    print('_summarize', bool(res))

    if not res:
        c_summarize.delay(file_id, topic)
        return { "finished": False }

    return { 
        "finished": True,
        "summary": res,
    }

@app.route("/internal/transcribe", methods=['POST'])
def transcribe():
    form_data = request.form
    file_id = form_data["id"]
    print(f'/internal/transcribe {file_id}', flush=True)

    return _transcribe(file_id)

def _transcribe(file_id):
    try:
        check_pdf_download(file_id)
    except Exception as e:
        message = f"File Download did not work. (Is the FileInfo ID incorrect?)\n{e}"
        return jsonify({ 
            "finished": False,
            "error": message,
        })

    finished = check_transcript(file_id)
    print('_transcribe', finished)

    if not finished:
        c_transcript.delay(file_id)
        return jsonify({ "finished": False })
    
    return jsonify({ "finished": True })

@app.route("/internal/transcript_progress", methods=['POST'])
def get_transcript_progress():
    form_data = request.form
    file_id = form_data["id"]
    print(f'/internal/transcript_progress {file_id}', flush=True)

    logging_fpath = get_unique_filepath(TRANSCRIBE_TASK, file_id)
    progress = get_progress(logging_fpath)

    return jsonify({ "progress": progress })

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

@app.route("/internal/dev", methods=['GET'])
def get_dev():
    if os.environ.get('DEV_ENV'):
        return f"DEV_ENV set to {os.environ.get('DEV_ENV')}"
    else:
        return "DEV_ENV not set"