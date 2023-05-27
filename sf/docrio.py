import base64
import os
import json
import requests

from auth.jwt import get_token
from util.directories import FILE_INFO_DIR

if os.environ.get('DEV_ENV'):
    GATEWAY = "https://api.214375601255.genesisapi.com/v1/"
else:
    GATEWAY = "https://api.339287139604.genesisapi.com/v1/"

def check_pdf_download(file_id: int):
    fpath = os.path.join(FILE_INFO_DIR, f'{file_id}.pdf')

    if not os.path.isfile(fpath):
        signed_url = get_signed_url(file_id)
        response = requests.get(signed_url, allow_redirects=True)
        
        ct = response.headers.get('content-type')
        if ct != 'application/pdf':
            return "not application/pdf"

        open(fpath, 'wb').write(response.content)

def get_signed_url(file_id: int) -> str:
    TOKEN = get_token()
    
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.get(GATEWAY + 'files?Id=' + file_id,
                            headers=headers)
    return response.json()['Records'][0]['SignedUrl']

def init_file_apigateway(fname: str, content_type: str, token: str):
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json',
    }

    data = [ {
        "Name": fname,
        "litify_docs__File_Type__c": content_type,
    } ]

    response = requests.post(GATEWAY + "files",
                             headers=headers,
                             data=json.dumps(data))
    
    return response

def upload_file_apigateway(signed_url: str, base64_str: str, content_type: str):
    headers = {
        'Content-Type': content_type
    }

    response = requests.put(
        signed_url,
        data=base64.b64decode(base64_str), # TODO
        headers=headers,
    )

    return response

def complete_file_apigateway(id: str, token: str):
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json',
    }

    data = { "Ids" : [ id ] }

    response = requests.post(GATEWAY + "files/complete",
                             headers=headers,
                             data=json.dumps(data))
    
    return response

def upload_base64(fname: str, base64_str: str, content_type: str = 'application/pdf'):
    token = get_token()

    response = init_file_apigateway(fname, content_type, token)
    print('POST to /files', response)

    resp_dict = json.loads(response.content.decode('utf-8'))
    id = resp_dict[fname]['Id']
    signed_url = resp_dict[fname]['SignedUrl']

    response = upload_file_apigateway(signed_url, base64_str, content_type)
    print('POST to SignedURL', response)

    response = complete_file_apigateway(id, token)
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
