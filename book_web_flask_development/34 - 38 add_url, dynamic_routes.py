from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Hello world!</h1>'


@app.route('/1')
def route1():
    return '<h1>Hello , route1 </h1>'


def route2():
    return '<h1>Hello, route2 </h1>'


# dynamic routes
@app.route('/<string:id>')
def dynamic_route(id):
    prefix = 'id'
    id_int = id[2:]
    return '<h1>Hello, {}, how are you today?</h1>'.format(id_int)


app.add_url_rule('/2', 'route2_name', route2)

if __name__ == '__main__':
    app.run(debug=True)
