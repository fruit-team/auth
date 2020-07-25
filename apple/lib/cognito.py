import os
import re
import hmac
import hashlib
import base64
import logging

import boto3
import botocore.exceptions

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

COGNITO_CLIENT_ID = os.environ.get('COGNITO_CLIENT_ID', '')
COGNITO_CLIENT_SECRET = os.environ.get('COGNITO_CLIENT_SECRET', '')

USERNAME_PATTERN = re.compile(r'^[a-zA-Z0-9]{2,15}')
EMAIL_PATTERN = re.compile(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,15}$')


def get_secret_hash(username):
    msg = username + COGNITO_CLIENT_ID
    dig = hmac.new(
        str(COGNITO_CLIENT_SECRET).encode('utf-8'),
        msg=str(msg).encode('utf-8'),
        digestmod=hashlib.sha256
    ).digest()
    d2 = base64.b64encode(dig).decode()
    return d2


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
        return 'password should have caps, special chars, numbers'
    except Exception as e:
        logger.exception('cognito signup failed reason: {}'.format(e))
        return 'An internal server error occurred.'

    # success
    return None
