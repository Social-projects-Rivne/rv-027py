"""This module generates routes for admin panel"""
from functools import wraps
from urllib import urlencode
from flask_mail import Mail, Message

from flask import (current_app, flash, redirect, request, render_template,
                   send_from_directory, session, url_for)
from sqlalchemy import and_

from backend.app import app, db, mail
from backend.forms.forms import (IssueForm, LoginForm, SearchUserForm,
                                 SearchIssuesForm, UserForm, UserAddForm)
from backend.models.issues import Attachment, Category, get_all_issue_history, Issue
from backend.models.users import Role, User, user_search


ROLE_ADMIN = 1
ROLE_MODERATOR = 2
ROLE_USER = 3

MIN_SEARCH_STR = 2

PAGINATE_PAGE = 8


def admin_permissions(function):
    """Decorator to check admin rights to access some route."""

    @wraps(function)
    def wrapper(*args, **kwargs):
        """Wrapper for routes."""
        if 'user_id' not in session or session['role_id'] != ROLE_ADMIN:
            flash("No access", category="danger")
            return redirect(url_for('login'))
        return function(*args, **kwargs)

    return wrapper


@app.route('/')
@admin_permissions
def admin():
    """Admin page route."""
    return redirect(url_for('issues_page'))


@app.route('/userpage', methods=['GET', 'POST'])
@app.route('/userpage/<int:num_page>', methods=['GET', 'POST'])
@admin_permissions
def user_page(num_page=1):
    """Page with list of users route."""
    form = SearchUserForm(request.args, meta={'csrf': False})
    msg = False
    if form.validate():
        search_by = int(request.args.get('search_by'))
        order_by = int(request.args.get('order_by'))
        search_string = str(request.args.get('search'))
        if len(search_string) >= MIN_SEARCH_STR:
            condition = user_search(search_string, search_by)
        else:
            condition = ""
            if search_string != "":
                msg = True

        order_list = [User.id, User.role_id, User.delete_date]
        order = order_list[order_by]

        search_users = db.session.query(User, Role).filter(and_(
            User.role_id == Role.id, condition)).order_by(order).paginate(
                per_page=PAGINATE_PAGE, page=num_page, error_out=True)

        if msg:
            flash("Search string is too small", category="danger")
        return render_template('user_page.html', form=form, users=search_users,
                               get="?" + urlencode(request.args))
    else:
        users = db.session.query(User, Role).filter(
            User.role_id == Role.id).order_by(User.id).paginate(
                per_page=PAGINATE_PAGE, page=num_page, error_out=True)
        return render_template('user_page.html', form=form, users=users,
                               get="?" + urlencode(request.args))


@app.route('/useradd', methods=['GET', 'POST'])
@admin_permissions
def user_add():
    """Page with user add route."""
    route_to = url_for('user_add')
    form = UserAddForm(request.form)

    if form.validate_on_submit():
        newuser = User()
        newuser.name = form.name.data
        newuser.alias = form.alias.data
        newuser.role_id = form.role_id.data
        newuser.email = form.email.data
        newuser.password = form.password.data
        db.session.add(newuser)
        db.session.commit()
        password = form.password.data
        subject = "Add User"
        msg = Message(app.config['ADMIN_MAIL_SUBJECT_PREFIX'] + ' ' + subject, sender=app.config['ADMIN_MAIL_SENDER'],
                      recipients=[newuser.email])
        msg.body = """
                              From: %s to <%s>
                              Email: %s
                              Name: %s
                              Alias: %s
                              Password: %s
                              """ % (
            app.config['ADMIN_MAIL_SUBJECT_PREFIX'], newuser.email, newuser.email, newuser.name,
            newuser.alias, password)
        mail.send(msg)
        flash("User added and notification", category="success")
        return redirect(url_for('user_page'))

    return render_template('user_add.html', form=form, route_to=route_to)


@app.route('/usermodify/<int:users_id>', methods=['GET', 'POST'])
@admin_permissions
def user_modify(users_id):
    """Page with user edit route."""
    route_to = url_for('user_modify', users_id=users_id)
    user = db.session.query(User).get(users_id)
    form = UserForm(request.form, obj=user)
    remove_role_change = (users_id != session['user_id'])

    if user.delete_date:
        flash("You can't edit the user who was deleted.", category="danger")
    elif form.validate_on_submit():
        if (users_id == session['user_id']) and (int(request.form.get('role_id')) != ROLE_ADMIN):
            flash("You can't change admin role for yourself.", category="danger")
        else:
            form.populate_obj(user)
            db.session.commit()
            flash("User modified")
            return redirect(url_for('user_page'))

    return render_template(
        'user_modify.html',
        form=form,
        route_to=route_to,
        remove_role_change=remove_role_change)


@app.route('/deleteuser/<int:users_id>', methods=['POST'])
@admin_permissions
def delete_user(users_id):
    """Route for deleting user."""
    user = db.session.query(User).get(users_id)
    is_deleted = user.delete()
    db.session.commit()
    if not is_deleted:
        flash("The last admin can't be deleted!", category="danger")
    else:
        flash("User delete", category="success")
    return redirect(url_for('user_page'))


@app.route('/restoreuser/<int:users_id>', methods=['POST'])
@admin_permissions
def restore_user(users_id):
    """Route for restore user."""
    user = db.session.query(User).get(users_id)
    user.restore()
    db.session.commit()
    flash("User restore", category="success")
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
            flash('Welcome %s' % user.name, category="success")
            return redirect(url_for('admin'))
        else:
            flash('Incorrect login/password data...', category="danger")
            return render_template('login_page.html', form=form)
    else:
        return render_template('login_page.html', form=form)

    return render_template('login_page.html', form=form)


@app.route('/logout')
def logout():
    """Logout route."""
    session.pop('user_id', None)
    session.pop('role_id', None)
    flash("Successful logout", category="success")
    return redirect(url_for('login'))


@app.route('/issuespage', methods=['GET', 'POST'])
@app.route('/issuespage/<int:num_page>', methods=['GET', 'POST'])
@admin_permissions
def issues_page(num_page=1):
    """Issues page route."""
    form = SearchIssuesForm(request.args, meta={'csrf': False})
    condition = None
    order = None
    if form.validate():
        search_by = int(request.args.get('search_by'))
        order_by = int(request.args.get('order_by'))
        search_string = str(request.args.get('search'))

        search_list = ['title', 'category', 'description']
        if len(search_string) >= MIN_SEARCH_STR:
            search_parameter = '%{}%'.format(search_string)
            if search_list[search_by] == 'title':
                condition = Issue.title.ilike(search_parameter)

            elif search_list[search_by] == 'description':
                condition = Issue.description.ilike(search_parameter)

            else:
                condition = Category.category.ilike(search_parameter)

        order_list = [Issue.title, Category.category]
        order = order_list[order_by]

    if order and condition is not None:
        issues = db.session.query(
            Category.category, Issue, User.alias).filter(and_(
                Issue.user_id == User.id, Issue.category_id == Category.id,
                condition)).order_by(order).paginate(
                    per_page=PAGINATE_PAGE, page=num_page, error_out=True)

    else:
        issues = db.session.query(
            Category.category, Issue, User.alias).filter(and_(
                Issue.user_id == User.id, Issue.category_id == Category.id)).order_by(
                    order).paginate(per_page=PAGINATE_PAGE, page=num_page, error_out=True)

    return render_template('issues_page.html', issues=issues, form=form,
                           get="?" + urlencode(request.args))


@app.route('/issuemodify/<int:issue_id>', methods=['GET', 'POST'])
@admin_permissions
def issue_modify(issue_id):
    """Page with issue edit route."""
    route_to = url_for('issue_modify', issue_id=issue_id)
    issue = db.session.query(Issue).get(issue_id)
    form = IssueForm(request.form, obj=issue)

    if issue.delete_date:
        flash("You can't edit the issue who was deleted.", category="danger")
    elif form.validate_on_submit():
        form.populate_obj(issue)
        db.session.commit()
        flash("Issue modified")
        return redirect(url_for('issues_page'))

    return render_template('issue_modify.html', form=form, route_to=route_to)


@app.route('/deleteissue/<int:issue_id>', methods=['POST'])
@admin_permissions
def delete_issue(issue_id):
    """Route for deleting issue."""
    issue = db.session.query(Issue).get(issue_id)
    issue.delete()
    db.session.commit()
    flash("Issue delete", category="success")
    return redirect(url_for('issues_page'))


@app.route('/restoreissue/<int:issue_id>', methods=['POST'])
@admin_permissions
def restore_issue(issue_id):
    """Route for restore issue."""
    issue = db.session.query(Issue).get(issue_id)
    issue.restore()
    db.session.commit()
    flash("Issue restore", category="success")
    return redirect(url_for('issues_page'))


@app.route('/media/<path:url>')
def media_dir(url):
    return send_from_directory(current_app.config['MEDIA_FOLDER'], url)


@app.route('/issue/<int:issue_id>', methods=['GET'])
@admin_permissions
def issue_info(issue_id):
    """Route for issue page"""
    issue = db.session.query(Issue).get(issue_id)
    list_history = get_all_issue_history(issue_id)
    attachments = db.session.query(Attachment).filter(Attachment.issue_id == issue_id).all()
    return render_template('issue.html', issue=issue, list_history=list_history,
                           attachments=attachments)


@app.route('/deleteimage', methods=['POST'])
@admin_permissions
def delete_image():
    """Route for deleting attachment."""
    attachment_id = request.form['attachment-id']
    attachment = db.session.query(Attachment).get(attachment_id)
    issue_id = attachment.issue_id
    attachment.delete()
    return redirect(url_for('issue_info', issue_id=issue_id))
