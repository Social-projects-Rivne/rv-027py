from datetime import datetime
from flask import flash, render_template, redirect, \
                  request, session, url_for
from werkzeug.security import generate_password_hash, \
                              check_password_hash
from manage import app, db
from forms.forms import LoginForm, UserForm
from models.users import Role, User
from models.issues import Attachment, Category, Issue, \
                          IssueHistory, Status


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/admin')
def admin():
    if 'user_id' in session and session['role_id'] == 1:
        return render_template('admin_page.html')
    else:
        flash('No access ...')
        return redirect(url_for('index'))


@app.route('/user_page')
def user_page():
    users = db.session.query(User, Role).filter(
        User.role_id == Role.id).order_by(User.id).all()
    return render_template('user_page.html', users=users)


@app.route("/user_modify", methods=['GET', 'POST'])
def user_modify():
    form = UserForm(request.form)

    if 'id' in request.args:
        user = db.session.query(User).get(request.args.get('id'))
        form = UserForm(obj=user)

    if request.method == "GET":
        return render_template('user_modify.html', form=form)

    elif request.method == "POST":

        if form.validate_on_submit():
            if form.id.data:
                user = db.session.query(User).get(form.id.data)
                user.name = form.name.data
                user.alias = form.alias.data
                user.email = form.email.data
                user.role_id = form.role_id.data

                if form.delete_date.data:
                    user.delete_date = form.delete_date.data
                else:
                    user.delete_date = None

                db.session.commit()
                flash("user modified")
            else:
                newuser = User(name=form.name.data,
                               alias=form.alias.data,
                               email=form.email.data,
                               password=None,
                               role_id=form.role_id.data,
                               avatar=None,
                               delete_date=None)
                db.session.add(newuser)
                db.session.commit()
                flash("user added")
            return redirect(url_for('user_page'))
        else:
            flash("wrong data")
            return render_template('user_modify.html', form=form)


@app.route('/delete_user')
def delete_user():
    if 'id' in request.args:
        today = datetime.today().strftime('%Y-%m-%d')
        user = db.session.query(User).get(request.args.get('id'))
        user.delete_date = today
        db.session.commit()
        flash("user deleted")

    return redirect(url_for('user_page'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'GET':
        return render_template('login_page.html', form=form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = db.session.query(User).filter(
                User.email == form.email.data).first()
            if user.is_correct_password(form.password.data):
                session['user_id'] = user.id
                session['role_id'] = user.role_id
                flash('Welcome %s' % user.name)
                return redirect(url_for('index'))
            else: 
                flash('Incorrect login/password data...')
                return render_template('login_page.html', form=form)
        else:
            flash('Incorrect login/password data...')
            return render_template('login_page.html', form=form)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('role_id', None)
    flash("Logout success")
    return redirect(url_for('index'))
