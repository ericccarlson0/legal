import base64
import os
import json
import requests
from auth.jwt import get_token

GATEWAY = "https://api.339287139604.genesisapi.com/v1/"
if os.environ.get('DEV_ENV'):
    GATEWAY = "https://api.214375601255.genesisapi.com/v1/"

FILE_INFO_DIR = 'downloaded-file-info'

def check_download(file_id: int, fname: str):
    if not os.path.isfile(fname):
        signed_url = get_signed_url(file_id)
        response = requests.get(signed_url, allow_redirects=True)
        
        ct = response.headers.get('content-type')
        if ct != 'application/pdf':
            return "not application/pdf"

        open(os.path.join(FILE_INFO_DIR, fname), 'wb').write(response.content)

def get_signed_url(file_id: int) -> str:
    TOKEN = get_token()
    
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.get(GATEWAY + 'files?Id=' + file_id,
                            headers=headers)
    return response.json()['Records'][0]['SignedUrl']

def upload_base64(fname: str, base64_str: str, content_type: str = 'application/pdf'):
    TOKEN = get_token()

    # POST TO FILES
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer ' + TOKEN,
        'Content-Type': 'application/json',
    }

    data = [ {
        "Name": fname,
        "litify_docs__File_Type__c": content_type,
    } ]
    response = requests.post(GATEWAY + "files",
                             headers=headers,
                             data=json.dumps(data))
    print('POST to /files', response)
    resp_dict = json.loads(response.content.decode('utf-8'))
    id = resp_dict[fname]['Id']
    signed_url = resp_dict[fname]['SignedUrl']

    # UPLOAD FILE
    headers = {
        'Content-Type': content_type
    }

    response = requests.put(
        signed_url,
        data=base64.b64decode(base64_str), # TODO
        headers=headers,
    )
    print('upload to SignedURL', response)

    # POST TO FILES/COMPLETE
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer ' + TOKEN,
        'Content-Type': 'application/json',
    }

    data = { "Ids" : [ id ] }

    response = requests.post(GATEWAY + "files/complete",
                             headers=headers,
                             data=json.dumps(data))
    print('POST to /files/complete', response)

    return response.content

def upload_to_presigned_url(fp: str, signed_url: str, content_type: str = 'application/pdf'):
    headers = {
        'Content-Type': content_type
    }

    with open(fp, 'rb') as data:
        response = requests.put(
            signed_url,
            data=data,
            headers=headers,
        )
    
    return response