from flask import Flask, render_template, request, url_for, redirect, g
from flask_sqlalchemy import SQLAlchemy
from models import Attachment, Category, IssueHistory, Issue, Role, Status, User
from config import db_credentals


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_credentals
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/admin')
def admin():
    return render_template('adminPage.html')


@app.route('/user_page')
def user_page():
    users = db.session.query(User).all()
    return render_template('userPage.html', users=users)


@app.route('/user_form', methods=['GET', 'POST'])
def user_form():
    if request.method == 'GET' and request.args.get('id') is None:
        return render_template('userForm.html')

    elif request.method == 'POST':
        data = request.form.to_dict()
        newuser = User(name=data['user_name'], alias=data['user_alias'], email=data['user_email'],
                       password=None, role_id=data['user_role'], avatar=None, delete_date=None)
        db.session.add(newuser)
        db.session.commit()
        return redirect(url_for('user_page'))


@app.route('/user_edit', methods=['GET', 'POST'])
def user_edit():
    if request.method == 'GET':
        user = db.session.query(User).get(request.args.get('id'))
        return render_template('userForm.html', user=user)

    elif request.method == 'POST':
        data = request.form.to_dict()

        user = db.session.query(User).get(data.get('user_id'))
        user.name = data['user_name']
        user.alias = data['user_alias']
        user.role_id = data['user_role']
        if data['user_delete_date']:
            user.delete_date = data['user_delete_date']
        else:
            user.delete_date = None

        db.session.commit()
        return redirect(url_for('user_page'))
