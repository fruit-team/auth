from chalice import Chalice

app = Chalice(app_name='apple')


@app.route('/signup')
def signup():
    '''
    http GET $(chalice url)signup id=tester name=james
    '''

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
