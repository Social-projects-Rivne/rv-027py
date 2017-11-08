from functools import wraps

from flask import flash, redirect, request, render_template, session, url_for
from sqlalchemy import or_

from app import app, db
from forms.forms import LoginForm, UserForm
from models.users import Role, User

ROLE_ADMIN = 1
ROLE_MODERATOR = 2
ROLE_USER = 3


def admin_permissions(func):
    """Decorator to check admin rights to access some route."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not 'user_id' in session or session['role_id'] != ROLE_ADMIN:
            flash("No access")
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return wrapper


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/admin')
@admin_permissions
def admin():
    return render_template('admin_page.html')


@app.route('/userpage')
@admin_permissions
def user_page():
    users = db.session.query(User, Role).filter(
        User.role_id == Role.id).order_by(User.id).all()
    return render_template('user_page.html', users=users)


@app.route('/useradd', methods=['GET', 'POST'])
@admin_permissions
def user_add():
    route_to = url_for('user_add')
    form = UserForm(request.form)

    if form.validate_on_submit():
        newuser = User()
        newuser.name = form.name.data
        newuser.alias = form.alias.data
        newuser.role_id = form.role_id.data
        newuser.email = form.email.data
        db.session.add(newuser)
        db.session.commit()
        flash("User added")
        return redirect(url_for('user_page'))

    return render_template('user_modify.html', form=form, route_to=route_to)


@app.route('/usermodify/<int:users_id>', methods=['GET', 'POST'])
@admin_permissions
def user_modify(users_id):
    route_to = url_for('user_modify', users_id=users_id)
    user = db.session.query(User).get(users_id)
    form = UserForm(request.form, obj=user)

    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        flash("User modified")
        return redirect(url_for('user_page'))

    return render_template('user_modify.html', form=form, route_to=route_to)


@app.route('/deleteuser/<int:users_id>', methods=['POST'])
@admin_permissions
def delete_user(users_id):
    user = db.session.query(User).get(users_id)
    is_deleted = user.delete()
    db.session.commit()
    msg = "User deleted" if is_deleted else "Impossible to delete user"
    flash(msg)
    return redirect(url_for('user_page'))


@app.route('/restoreuser/<int:users_id>', methods=['POST'])
@admin_permissions
def restore_user(users_id):
    user = db.session.query(User).get(users_id)
    user.restore()
    db.session.commit()
    flash("User restored")
    return redirect(url_for('user_page'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if form.validate_on_submit():
        user = db.session.query(User).filter(
            User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            session['user_id'] = user.id
            session['auth'] = True
            session['role_id'] = user.role_id
            flash('Welcome %s' % user.name)
            return redirect(url_for('index'))
        else:
            flash('Incorrect login/password data...')
            return render_template('login_page.html', form=form)
    else:
        return render_template('login_page.html', form=form)

    return render_template('login_page.html', form=form)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('role_id', None)
    session['auth'] = False
    flash("Successful logout")
    return redirect(url_for('index'))
