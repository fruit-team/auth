import os
import re
import hmac
import hashlib
import base64
import logging

import boto3
import botocore.exceptions
from chalice import Chalice

logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Chalice(app_name='apple')

COGNITO_CLIENT_ID = os.environ.get('COGNITO_CLIENT_ID', '')
COGNITO_CLIENT_SECRET = os.environ.get('COGNITO_CLIENT_SECRET', '')


def get_secret_hash(username):
    msg = username + COGNITO_CLIENT_ID
    dig = hmac.new(
        str(COGNITO_CLIENT_SECRET).encode('utf-8'),
        msg=str(msg).encode('utf-8'),
        digestmod=hashlib.sha256
    ).digest()
    d2 = base64.b64encode(dig).decode()
    return d2


USERNAME_PATTERN = re.compile(r'^[a-zA-Z0-9]{2,15}')
EMAIL_PATTERN = re.compile(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,15}$')


def cognito_signup(username, email, password):
    if not USERNAME_PATTERN.match(username):
        return 'invalid username'

    if not EMAIL_PATTERN.match(email):
        return 'invalid email'

    client = boto3.client('cognito-idp')
    try:
        client.sign_up(
            ClientId=COGNITO_CLIENT_ID,
            SecretHash=get_secret_hash(username),
            Username=username,
            Password=password,
            UserAttributes=[{
                'Name': 'email',
                'Value': email,
            }],
            ValidationData=[{
                'Name': "email",
                'Value': email
            }, {
                'Name': "custom:username",
                'Value': username
            }]
        )
    except client.exceptions.UsernameExistsException:
        return 'username already exists'
    except botocore.exceptions.ParamValidationError as e:
        print(dir(e), e.args, e.kwargs)
        return 'password should have caps, special chars, numbers'
    except Exception as e:
        logger.exception('cognito signup failed reason: {}'.format(e))
        return 'internal server error'

    # success
    return None


@app.route('/signup', methods=['POST'])
def signup():
    '''
    http POST $(chalice url)signup username=tester email=tester@fruit.team password=1234
    http POST http://127.0.0.1:8000/signup username=tester email=tester@fruit.team password=1234
    '''
    body = app.current_request.json_body
    username = body['username']
    email = body['email']
    password = body['password']

    client = boto3.client('cognito-idp')

    error = cognito_signup(username, email, password)
    if error:
        return {'success': False, 'message': error}
    return {'success': True, 'message': 'ok'}


@app.route('/')
def index():
    '''
    http GET $(chalice url)
    '''
    return {'hello': 'world'}


@app.route('/hello/{name}')
def hello_name(name):
    '''
    http GET $(chalice url)hello/james
    '''
    # '/hello/james' -> {"hello": "james"}
    return {'hello': name}


@app.route('/users', methods=['POST'])
def create_user():
    '''
    http POST $(chalice url)users id=tester name=john
    '''
    # This is the JSON body the user sent in their POST request.
    user_as_json = app.current_request.json_body
    # We'll echo the json body back to the user in a 'user' key.
    return {'user': user_as_json}
