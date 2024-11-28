import json
from functools import wraps
from jose import jwt
from urllib.request import urlopen

AUTH0_DOMAIN = 'YOUR_AUTH0_DOMAIN'
ALGORITHMS = ['RS256']
API_IDENTIFIER = 'YOUR_API_IDENTIFIER'

# Fetch the Auth0 public keys for JWT validation
def get_jwk():
    url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
    response = urlopen(url)
    return json.loads(response.read())

def requires_auth(permission=''):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = None
            if 'Authorization' in request.headers:
                token = request.headers['Authorization'].split()[1]
            if not token:
                abort(401)

            try:
                unverified_header = jwt.get_unverified_header(token)
                if unverified_header is None:
                    raise Exception('Token header is missing')

                rsa_key = {}
                for key in get_jwk()['keys']:
                    if key['kid'] == unverified_header['kid']:
                        rsa_key = {
                            'kty': key['kty'],
                            'kid': key['kid'],
                            'use': key['use'],
                            'n': key['n'],
                            'e': key['e']
                        }
                if rsa_key:
                    payload = jwt.decode(token, rsa_key, algorithms=ALGORITHMS, audience=API_IDENTIFIER)
            except Exception as e:
                abort(401)
            return f(payload, *args, **kwargs)

        return decorated_function
    return wrapper
