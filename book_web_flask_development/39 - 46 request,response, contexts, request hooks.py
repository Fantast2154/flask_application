from flask import Flask, request, make_response, redirect, abort

# todo learn flask contexts

app = Flask(__name__)

# request hooks are part of the code, registered as decorators
# that must run before or after a request
# supported hooks:
"""
before_request

before_first_request

after_request

teardown_request - run after even if error occurred
"""


@app.route('/')
def index():
    # flask request object
    user_agent = request.headers.get('User-Agent')
    return '<p>Your browser is {}</p>'.format(user_agent)

# request errors:
"""
400 request error
404 does not exist
200 request was successful
302 redirect to the location, shown in header

"""
@app.route('/resp')
def response_example():
    # return consists of tuple with 3 arguments:
    # body, status code, dictionary_header
    return '<p>Your browser is {}</p>'.format('Response example'), 400

@app.route('/resp2')
def better_response_example():
    # flask response object

    response = make_response('<h1>This documents carries a cookie!</h1>')
    response.set_cookie('answer', '42')
    return response

@app.route('/resp3')
def redirect_response():
    # flask response object
    return redirect('https://google.com/')

@app.route('/resp4')
def error_handler():
    # flask response object
    #if bla bla bla
    abort(400)
    return '<h1>Page was successfully loaded.</h1>'


# how flask understands which request in which?
    # in particular in a multi-thread server
    # solutions - contexts

# there are two contexts in Flask:
# 1. applications context: current_app g (temp storage)
# 2. request context: request, session

# application context
"""
from hello import app
from flask import current_app
current_app.name
app_ctx = app.app_context()
app_ctx.push()
current_app.name
app.url_map
"""

# from hello import app
# app.url_map (defined routes + static (!)


if __name__ == '__main__':
    app.run(debug=True)
