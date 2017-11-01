from datetime import datetime
from flask import flash, render_template, redirect, request, session, url_for
from manage import app, db
from forms.forms import LoginForm, UserForm
from models.users import Role, User


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/admin')
def admin():
    if 'user_id' in session and session['role_id'] == 1:
        return render_template('admin_page.html')
    else:
        flash('Dont have access ...')
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

        if (form.validate_on_submit() and
                User(**User().clear_form_data(form.data)).data_validataion()):
            if form.id.data:
                user = db.session.query(User).get(form.id.data)
                user.name = form.name.data
                user.alias = form.alias.data
                user.email = form.email.data
                user.role_id = form.role_id.data
                user.delete_date = form.delete_date.data

                db.session.commit()
                flash("user modified")
            else:
                newuser = User(**User().clear_form_data(form.data))
                db.session.add(newuser)
                db.session.commit()
                flash("user added")
            return redirect(url_for('user_page'))
        else:
            flash("wrong data")
            return render_template('user_modify.html', form=form)


@app.route('/delete_user')
def delete_user():
    msg = "cannot delete user"
    if 'id' in request.args:
        today = datetime.today().strftime('%Y-%m-%d')
        user = db.session.query(User).get(request.args.get('id'))
        if not is_last_admin(user):
            user.delete_date = today
            db.session.commit()
            msg = "user deleted"
        flash(msg)

    return redirect(url_for('user_page'))


def is_last_admin(user):
    admins = User.query.filter_by(role_id='1')
    count = admins.count()
    if count > 1:
        return False
    else:
        admin = admins.first()
        if user.id != admin.id:
            return False
        return True


@app.route('/restore_user')
def restore_user():
    if 'id' in request.args:
        user = db.session.query(User).get(request.args.get('id'))
        user.delete_date = None
        db.session.commit()
        flash("user restored")

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
