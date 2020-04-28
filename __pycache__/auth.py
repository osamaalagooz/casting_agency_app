import json
from flask import request, _request_ctx_stack, abort, session
from functools import wraps
from jose import jwt
import urllib.request as uri
import yaml

AUTH0_DOMAIN = 'castingagency.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'shows'

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header

def get_token_auth_header():
    if 'Authorization' not in session:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    header = session.get('Authorization')
    header_parts = header.split(' ')

    if len(header_parts) == 1:

        raise AuthError({
            "code": "invalid_header"
        }, 401)

    elif header_parts[0].lower() != "bearer":
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    return header_parts[1]


def check_permissions(permission, payload):
    if "permissions" not in payload:
        abort(400)

    if permission not in payload["permissions"]:
        abort(401)

    return True


def verify_decode_jwt(token):
    # GET THE PUBLIC KEY FROM AUTH0
    jsonurl = uri.urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    # GET THE DATA IN THE HEADER
    unverified_header = jwt.get_unverified_header(token)

    # CHOOSE OUR KEY
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            # USE THE KEY TO VALIDATE THE JWT
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            
            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
        'code': 'invalid_header',
        'description': 'Unable to find the appropriate key.'
    }, 400)



def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper

    return requires_auth_decorator

def get_access_token(code):
    url = 'https://castingagency.auth0.com/oauth/token'
    headers = {}
    headers['content-type'] = 'application/x-www-form-urlencoded'
    data = 'grant_type=authorization_code&client_id=ZjgUkMB9JxQbis2hVh1d2d9jfcyeTZQu&client_secret=1VcM6mSAy3OohWt6KZwwAxeDIZNTQTNHZi3rWEGcjOFbRQWKv3oLtnkLqG7xZ0Nn&code='+ code +'&redirect_uri=https://casting-agency-osama.herokuapp.com/'
    data = data.encode('ascii')
    req = uri.Request(url, data, headers )
    try:

        res = uri.urlopen(req)

    except uri.URLError as e:
            print('URL Error: ', e.reason) 
                
    except uri.HTTPError as e:
            print('HTTP Error code: ', e.code)
        
    else:  
        data_auth = res.read()       
        da = data_auth.decode('ascii')        
        dat = yaml.load(da, Loader=yaml.FullLoader)
        access_token = dat.get('access_token')
        session['Authorization'] = 'Bearer ' + access_token
        return access_token

def get_user_id(token):

    url2 = 'https://castingagency.auth0.com/userinfo'
    headers = {}
    headers['Authorization'] = 'Bearer ' + token 
    req2 = uri.Request(url2, headers=headers)

    try:

        res2 = uri.urlopen(req2)

    except uri.URLError as e:
            print('URL Error: ', e.reason) 
                
    except uri.HTTPError as e:
            print('HTTP Error code: ', e.code)
        
    else:

        user_info = res2.read()
        user_info_decoded = user_info.decode('ascii')
        user_info_valid = yaml.load(user_info_decoded, Loader=yaml.FullLoader)
    
        session['user_info'] = user_info_valid
        user_id = user_info_valid.get('sub')
        return user_id

def get_MGMT_API_ACCESS_TOKEN():

    url = 'https://' + AUTH0_DOMAIN + '/oauth/token'
    headers = {}
    headers['content-type'] = 'application/x-www-form-urlencoded'
    data = 'grant_type=client_credentials&client_id=ku7FNiai7lJUpY88ShrT040ESpDthC85&client_secret=DpZLfIiUJP0Pj808Ye_9bsekbgwnohsfR7zi_fkbt9xYpr4r_esEwHgBims-hFnD&audience=https://castingagency.auth0.com/api/v2/'
    data = data.encode('ascii')
    req = uri.Request(url, data, headers )
    try:

        res = uri.urlopen(req)

    except uri.URLError as e:
            print('URL Error: ', e.reason) 
                
    except uri.HTTPError as e:
            print('HTTP Error code: ', e.code)
        
    else:  
        data_auth = res.read()       
        data_decoded = data_auth.decode('ascii')        
        data_valid = yaml.load(data_decoded, Loader=yaml.FullLoader)
        mngm_api_token = data_valid.get('access_token')
        return mngm_api_token      
