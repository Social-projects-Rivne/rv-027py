from datetime import datetime
from functools import wraps

from flask import flash, redirect, request, render_template, session, url_for
from sqlalchemy import and_, or_

from app import app, db
from forms.forms import LoginForm, SearchForm, UserForm
from models.users import Role, User

ROLE_ADMIN = 1
ROLE_MODERATOR = 2
ROLE_USER = 3
MIN_SEARCH_STR = 2

def admin_permissions(func):
    """Decorator to check admin rights to access some route."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not 'user_id' in session or session['role_id'] != ROLE_ADMIN:
            flash("Don't have access")
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


@app.route('/userpage', methods=['GET'])
@admin_permissions
def user_page():
    form = SearchForm(request.form)
    users = db.session.query(User, Role).filter(
        User.role_id == Role.id).order_by(User.id).all()
    if request.args.get('search') != "" and request.args.get('search') >= MIN_SEARCH_STR:
    # if form.validate_on_submit():
        key = int(request.args.get('field_by'))
        search_string = str(request.args.get('search'))
        search_paremeters = []
        search_users = []
        for one_string in search_string.split(' '):
            if len(one_string) >= MIN_SEARCH_STR:
                search_paremeters.append(''.join(["%", one_string, "%"]))
        for search_paremeter in search_paremeters:
            conditions = {1:"users.name LIKE  '%s'" %(search_paremeter),
                          2:"users.alias LIKE  '%s'" %(search_paremeter),
                          3:"users.email LIKE  '%s'" %(search_paremeter)}
            conditions[4] = ' '.join([conditions[1], "OR", conditions[2]])
            conditions[5] = ' '.join([conditions[2], "OR", conditions[3]])
            conditions[6] = ' '.join([conditions[1], "OR", conditions[3]])
            conditions[7] = ' '.join([conditions[1], "OR", conditions[2], "OR", conditions[3]])
            condition = conditions.get(key)
            results = db.session.query(User, Role).filter(and_(
                User.role_id == Role.id, str(condition))).distinct(User.id).order_by(User.id).all()
            for user in results:
                if not user in search_users:
                    search_users.append(user)
        search_users.sort(key=lambda user: user[0].id)
        if search_users == []:
            flash("Search didn`t give result")
            return redirect(url_for('user_page'))
        flash("Search results")
        return render_template('user_page.html', form=form, users=search_users)
    else:
        return render_template('user_page.html', form=form, users=users)


@app.route('/useradd', methods=['GET', 'POST'])
@admin_permissions
def user_add():
    route_to = url_for('user_add')
    form = UserForm(request.form)

    if request.method == "GET":
        return render_template('user_modify.html', form=form, route_to=route_to)

    if form.validate_on_submit():
        newuser = User()
        newuser.name = form.name.data
        newuser.alias = form.alias.data
        newuser.role_id = form.role_id.data
        newuser.email = form.email.data
        db.session.add(newuser)
        db.session.commit()
        flash("user added")
        return redirect(url_for('user_page'))
    else:
        flash("wrong data")
        return render_template('user_modify.html', form=form, route_to=route_to)


@app.route('/usermodify/<int:users_id>', methods=['GET', 'POST'])
@admin_permissions
def user_modify(users_id):
    route_to = url_for('user_modify', users_id=users_id)
    user = db.session.query(User).get(users_id)
    form = UserForm(obj=user)

    if request.method == "GET":
        return render_template('user_modify.html', form=form, route_to=route_to)

    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        flash("user modified")
        return redirect(url_for('user_page'))
    else:
        flash("wrong data")
        return render_template('user_modify.html', form=form, route_to=route_to)


@app.route('/deleteuser/<int:users_id>')
def delete_user(users_id):
    current_moment = datetime.now()
    user = db.session.query(User).get(users_id)
    user.delete_date = current_moment
    db.session.commit()
    flash("user deleted")
    return redirect(url_for('user_page'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'GET':
        return render_template('login_page.html', form=form)

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
