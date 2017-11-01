from datetime import datetime
from functools import wraps

from flask import flash, render_template, redirect, request, session, url_for

from app_builder import app, db
from forms.forms import LoginForm, UserForm
from models.users import Role, User


def admin_permissions(func):
    """Decorator to check admin rights to access some route."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not 'user_id' in session or session['role_id'] != 1:
            flash("Don't have access")
            return redirect(url_for('index'))
        return func(*args, **kwargs)
    return wrapper


def form_data_clean(data):
    """Remove unnessery fields from form.data."""
    data.pop('csrf_token', None)
    data.pop('submit_button', None)
    data.pop('id', None)
    return data


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/admin')
@admin_permissions
def admin():
    return render_template('admin_page.html')


@app.route('/user_page')
@admin_permissions
def user_page():
    users = db.session.query(User, Role).filter(
        User.role_id == Role.id).order_by(User.id).all()
    return render_template('user_page.html', users=users)


@app.route("/user_modify", methods=['GET', 'POST'])
@admin_permissions
def user_modify():
    form = UserForm(request.form)

    if 'id' in request.args:
        chosen_one = db.session.query(User).get(request.args.get('id'))
        form = UserForm(obj=chosen_one)

    if request.method == "GET":
        return render_template('user_modify.html', form=form)

    elif request.method == "POST":

        if form.validate_on_submit():
            if form.id.data:
                user = db.session.query(User).get(form.id.data)

                form.populate_obj(user)

                db.session.commit()
                flash("user modified")
            else:
                newuser = User(**form_data_clean(form.data))
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
            if user and user.password == form.password.data:
                session['user_id'] = user.id
                session['role_id'] = user.role_id
                flash('Wellcome %s' % user.name)
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
