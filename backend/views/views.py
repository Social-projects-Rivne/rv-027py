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


@app.route('/userpage', methods=['GET', 'POST'])
@admin_permissions
def user_page():
    users = None

    form = SearchForm(request.args, csrf_enabled=False)
    if form.validate():
        key = int(request.args.get('field_by'))
        search_string = str(request.args.get('search'))
        condition_list = []
        for one_string in search_string.split():
            if len(one_string) < MIN_SEARCH_STR:
                continue
            search_parameter = '%{}%'.format(one_string)
            name_search = User.name.like(search_parameter)
            alias_search = User.alias.like(search_parameter)
            email_search = User.email.like(search_parameter)
            conditions = [
                name_search,
                alias_search,
                email_search,
                or_(name_search, alias_search),
                or_(alias_search, email_search),
                or_(email_search, name_search),
                or_(name_search, alias_search, email_search)
            ]
            condition_list.append(conditions[key])
        condition = or_(*condition_list)
        search_users = db.session.query(User, Role).filter(and_(
            User.role_id == Role.id, condition)).order_by(User.id).all()
        if search_users:
            flash("Search results")
            return render_template('user_page.html', form=form, users=search_users)
        else:
            flash("Search didn`t give result")
            return render_template('user_page.html', form=form, users=[])

    if 'delete_date_checkbox' in request.args and 'role_checkbox' in request.args:
        users = db.session.query(User, Role).filter(User.role_id == Role.id) \
            .order_by(User.role_id, User.delete_date).all()

    elif 'delete_date_checkbox' in request.args:

        users = db.session.query(User, Role).filter(User.role_id == Role.id) \
            .order_by(User.delete_date).all()

    elif 'role_checkbox' in request.args:

        users = db.session.query(User, Role).filter(User.role_id == Role.id) \
            .order_by(User.role_id).all()

    else:
        users = db.session.query(User, Role).filter(User.role_id == Role.id) \
            .order_by(User.role_id).all()
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
