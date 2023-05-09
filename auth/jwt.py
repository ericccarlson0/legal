import os
import requests
import time
import jwt # PyJWT
from cryptography.hazmat.primitives import serialization

def get_token():
    # print('get_token')
    
    curr_jwt = get_jwt()
    curr_token = jwt_to_token(curr_jwt)

    # DEAL WITH CASE: JWT EXPIRED
    return curr_token if curr_token else jwt_to_token(get_new_jwt())

def jwt_to_token(curr_jwt: str) -> str:
    # print('jwt_to_token')

    headers = { 
        'Content-Type': 'application/x-www-form-urlencoded',
        'accept': 'application/json',
    }

    data = {
        'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
        'assertion': curr_jwt,
    }

    BASE_URL = os.getenv('SALESFORCE_BASE_URL')
    response = requests.post(BASE_URL + '/services/oauth2/token',
                            headers=headers,
                            data=data)
    try:
        return response.json()['access_token']
    except:
        return None

def get_jwt() -> str:
    # print('get_jwt')

    AUTH_DIR = os.getenv('SERVICE_AUTH_DIR')
    if not os.path.isfile(AUTH_DIR + 'jwt.txt'):
        return get_new_jwt()
        
    with open (AUTH_DIR + 'jwt.txt', 'r') as jwt_file:
        # print('JWT file exists.')
        curr_jwt = jwt_file.read()
    
    return curr_jwt

def get_new_jwt() -> str:
    # print('get_new_jwt')

    ISS = os.getenv('SERVICE_ISS')
    SUB = os.getenv('SERVICE_SUB')
    AUD = os.getenv('SERVICE_AUD')
    AUTH_DIR = os.getenv('SERVICE_AUTH_DIR')

    # header = { 'alg': 'RS256' }

    payload = {
        'iss': ISS,
        'sub': SUB,
        'aud': AUD,
        'exp': str(int(time.time()) + 3600)
    }

    private_key = open(AUTH_DIR + 'server.key', 'r').read()
    key = serialization.load_pem_private_key(private_key.encode(), password=None)

    token = jwt.encode(
        payload=payload,
        key=key,
        algorithm='RS256'
    )

    if not os.path.isfile(AUTH_DIR + 'jwt.txt'):
        with open(AUTH_DIR + 'jwt.txt', 'x') as jwt_file:
            None
    with open(AUTH_DIR + 'jwt.txt', 'w') as jwt_file:
        jwt_file.write(token)
    with open(AUTH_DIR + 'jwt.txt', 'r') as jwt_file:
        print('can read JWT', jwt_file.read())

    return token
