import os
from flask import Flask, render_template, request, redirect, make_response, session, url_for, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_migrate import Migrate
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# todo lern flask context
# todo learn explicitly bootstrap framework
# todo check forms via request.form data
# todo SQL db do not have a server.. read about it

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

# /// - relative path
# //// - absolute path
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# secret key is used against cross-site request forgery (CSRF)
# SCRF is when a form is send on behalf of the registered user
app.config['SECRET_KEY'] = 'some string that hard to guess'

db = SQLAlchemy(app)

# Content Delivery Network (CDN), f.e. bootstrap includes jQuery.js that is needed for flask Moments
bootstrap = Bootstrap(app)
moment = Moment(app)
migrate = Migrate(app ,db)

@app.shell_context_processor
def make_shell_context():
    return dict(
        roles=Role.query.all(),
        users=User.query.all()
    )

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    user_role = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    datetime_created = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<Task %r>' % self.id


app.app_context().push()


# @app.route('/delete/<int:id>')
# def delete(id):
#     task_to_delete = Todo.query.get_or_404(id)
#
#     try:
#         db.session.delete(task_to_delete)
#         db.session.commit()
#         return redirect('/')
#     except:
#         return 'There was a problem deleting that task'
#
#
#
# @app.route('/update/<int:id>', methods=['GET', 'POST'])
# def update(id):
#     task = Todo.query.get_or_404(id)
#     if request.method == 'POST':
#         task.content = request.form['content']
#
#         try:
#             db.session.commit()
#             return redirect('/')
#         except:
#             return 'There was an issue updating your task'
#     else:
#         return render_template('update.html', task=task)


# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         task_content = request.form['content']
#         new_task = Task(content=task_content)
#
#         try:
#             db.session.add(new_task)
#             db.session.commit()
#             return redirect('/')
#         except:
#             return 'There was an issue adding your task'
#     else:
#         tasks = Task.query.order_by(Task.date_created).all()
#         return render_template('index.html', tasks=tasks, current_time=datetime.utcnow())


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


# custom error page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


# custom error page
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500


@app.route('/')
def index():
    return render_template('index.html', current_time=datetime.utcnow())


# basic form example todo check with request.form
@app.route('/form', methods=['GET', 'POST'])
def fileform():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('formfile.html', form=form, name=name)


# session example
@app.route('/form2', methods=['GET', 'POST'])
def fileform2():
    form = NameForm()
    if form.validate_on_submit():
        session['name2'] = request.form['name']
        return redirect(url_for('fileform2'))
    return render_template('formfile.html', form=form, name=session.get('name2'))


# flashing example
@app.route('/form3', methods=['GET', 'POST'])
def fileform3():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name3')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed you name!')
        session['name3'] = request.form['name']
        return redirect(url_for('fileform3'))
    return render_template('formfile.html', form=form, name=session.get('name3'))

# db example
@app.route('/form4', methods=['GET', 'POST'])
def fileform4():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        user_role = Role.query.filter_by(name='User').first()
        if user is None:
            user = User(username=form.name.data, role=user_role)
            try:
                db.session.add(user)
                db.session.commit()
            except:
                flash('We could not add a new user')
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('fileform4'))
    return render_template(
        'formfile.html',
        form=form,
        name=session.get('name'),
        known=session.get('known', False)
    )

@app.route('/user/<name>')
def greet_user(name):
    return render_template('user.html', name=name)


if __name__ == "__main__":
    app.run(debug=True)
