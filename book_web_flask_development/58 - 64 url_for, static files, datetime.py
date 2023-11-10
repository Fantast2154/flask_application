
from flask import Flask, url_for

app = Flask(__name__)

app.app_context().push()

@app.route('/')
def index():
    return '<h1>Hello</h1>'

@app.route('/user/<name>')
def user2(name):
    return '<h1>Hello, {}, how are you doing?</h1>'.format(name)

with app.test_request_context():
    print('URL:', end=' ')
    print(url_for('index'))
    print(url_for('user2', name='Dima', _external=True))
    print(url_for('user2', name='Boyko', _external=True))
    print(url_for('user2', name='John', page=2, version=1))
    print(url_for('static', filename='css/main.css', _external=True))


if __name__ == '__main__':
    app.run(debug=True)


"""
Links

url_for() helper function function that generates URLs from information stored in app's URL map


"""