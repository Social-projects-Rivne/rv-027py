"""This module generates routes for admin panel"""
from functools import wraps

from flask import flash, redirect, request, render_template, session, url_for
from sqlalchemy import and_, func, or_

from backend.app import app, db
from backend.forms.forms import LoginForm, SearchUserForm, UserForm
from backend.models.issues import (Attachment, Category, IssueHistory,
                                   Issue, Status)
from backend.models.users import Role, User

ROLE_ADMIN = 1
ROLE_MODERATOR = 2
ROLE_USER = 3


MIN_SEARCH_STR = 2


def admin_permissions(function):
    """Decorator to check admin rights to access some route."""

    @wraps(function)
    def wrapper(*args, **kwargs):
        """Wrapper for routes."""
        if 'user_id' not in session or session['role_id'] != ROLE_ADMIN:
            flash("No access")
            return redirect(url_for('login'))
        return function(*args, **kwargs)

    return wrapper


@app.route('/')
@admin_permissions
def admin():
    """Admin page route."""
    return render_template('admin_page.html')


@app.route('/userpage', methods=['GET', 'POST'])
@admin_permissions
def user_page():
    """Page with list of users route."""
    form = SearchUserForm(request.args, meta={'csrf': False})
    msg = False
    if form.validate():
        search_by = int(request.args.get('search_by'))
        order_by = int(request.args.get('order_by'))
        search_string = str(request.args.get('search'))
        if len(search_string) >= MIN_SEARCH_STR:
            condition_list = []
            for one_string in search_string.split():
                if len(one_string) < MIN_SEARCH_STR:
                    continue
                search_parameter = '%{}%'.format(one_string)
                search_list = []
                search_list.append(User.name.ilike(search_parameter))
                search_list.append(User.alias.ilike(search_parameter))
                search_list.append(User.email.ilike(search_parameter))
                conditions = [
                    search_list[0],
                    search_list[1],
                    search_list[2],
                    or_(search_list[0], search_list[1]),
                    or_(search_list[1], search_list[2]),
                    or_(search_list[2], search_list[0]),
                    or_(search_list[0], search_list[1], search_list[2])
                ]
                condition_list.append(conditions[search_by])
            condition = or_(*condition_list)
        else:
            condition = ""
            if search_string != "":
                msg = True

        order_list = [User.id, User.role_id, User.delete_date]
        order = order_list[order_by]

        search_users = db.session.query(User, Role).filter(and_(
            User.role_id == Role.id, condition)).order_by(order).all()

        if msg:
            flash("Search string is too small")
        return render_template('user_page.html', form=form, users=search_users)
    else:
        users = db.session.query(User, Role).filter(
            User.role_id == Role.id).order_by(User.id).all()
        return render_template('user_page.html', form=form, users=users)


@app.route('/useradd', methods=['GET', 'POST'])
@admin_permissions
def user_add():
    """Page with user add route."""
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
    """Page with user edit route."""
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
    """Route for deleting user."""
    user = db.session.query(User).get(users_id)
    is_deleted = user.delete()
    db.session.commit()
    msg = "User deleted" if is_deleted else "Impossible to delete user"
    flash(msg)
    return redirect(url_for('user_page'))


@app.route('/restoreuser/<int:users_id>', methods=['POST'])
@admin_permissions
def restore_user(users_id):
    """Route for restore user."""
    user = db.session.query(User).get(users_id)
    user.restore()
    db.session.commit()
    flash("User restored")
    return redirect(url_for('user_page'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page route."""
    form = LoginForm(request.form)

    if form.validate_on_submit():
        user = db.session.query(User).filter(
            User.email == form.email.data).first()
        if user and not user.delete_date and \
                user.check_password(form.password.data):
            session['user_id'] = user.id
            session['role_id'] = user.role_id
            flash('Welcome %s' % user.name)
            return redirect(url_for('admin'))
        else:
            flash('Incorrect login/password data...')
            return render_template('login_page.html', form=form)
    else:
        return render_template('login_page.html', form=form)

    return render_template('login_page.html', form=form)


@app.route('/logout')
def logout():
    """Logout route."""
    session.pop('user_id', None)
    session.pop('role_id', None)
    flash("Successful logout")
    return redirect(url_for('admin'))


@app.route('/issuespage')
@admin_permissions
def issues_page():
    """Issues page route."""
    count_att = db.session.query(Issue.id, func.count(Attachment.id).label(
        'count')).filter(Issue.id == Attachment.issue_id).group_by(
            Issue.id).subquery('count_att')
    issues = db.session.query(
        Category.category, Issue, User.alias, count_att.c.count).filter(and_(
            Issue.user_id == User.id, Issue.category_id == Category.id,
            Issue.id == count_att.c.id)).order_by(
                Issue.id).all()
    return render_template('issues_page.html', issues=issues)


@app.route('/issuehistory/<int:issue_id>')
@admin_permissions
def issue_history(issue_id):
    """Issue history page route."""
    history = db.session.query(
        IssueHistory, Status.status, User.alias, Issue.name).filter(and_(
            IssueHistory.user_id == User.id,
            IssueHistory.status_id == Status.id,
            IssueHistory.issue_id == Issue.id,
            IssueHistory.issue_id == issue_id)).all()
    return render_template('issue_history.html', issue_history=history)


@app.route('/attachments/<int:issue_id>')
@admin_permissions
def attachments(issue_id):
    """Attachments page route."""
    attach = db.session.query(Attachment, Issue.name).filter(and_(
        Attachment.issue_id == issue_id,
        Issue.id == Attachment.issue_id)).all()
    return render_template('attachments.html', attachments=attach)
