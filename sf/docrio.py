import requests
from auth.jwt import get_token

def get_signed_url(file_id: int) -> str:
    TOKEN = get_token()
    
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.get('https://api.339287139604.genesisapi.com/v1/files?Id=' + file_id,
                            headers=headers)
    return response.json()['Records'][0]['SignedUrl']
