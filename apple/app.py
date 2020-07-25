from chalice import Chalice

from lib.cognito import cognito_signup

app = Chalice(app_name='apple')


@app.route('/signup', methods=['POST'])
def signup():
    '''
    http POST $(chalice url)signup username=tester email=tester@fruit.team password=a@Bcd1234
    http POST http://127.0.0.1:8000/signup username=tester email=tester@fruit.team password=a@Bcd1234
    '''
    body = app.current_request.json_body
    username = body['username']
    email = body['email']
    password = body['password']

    error = cognito_signup(username, email, password)
    if error:
        return {'Code': 'SignupFailed', 'message': error}

    return {'Code': 'OK', 'message': 'success'}


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
