from flask import Blueprint, request, render_template, redirect, url_for, flash
from myapp.users.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flask_login import current_user, login_required, login_user, logout_user
from myapp import bcrypt, db
from myapp.models import User, Post
from myapp.users.utils import save_picture
import os   # move this to users/utils.py and some part of remove_img function
from flask import current_app



users = Blueprint('users', __name__)


@users.route("/registration", methods=["GET", "POST"])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    registration_form = RegistrationForm()

    if registration_form.validate_on_submit():
        username = registration_form.username.data
        email = registration_form.email.data
        password = registration_form.password.data
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash(f"Account created successfully for {username}! You can now login", category="success")
        return redirect(url_for('users.login'))

    return render_template('registration.html', form=registration_form, title='register')


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    login_form = LoginForm()

    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data
        remember_me = login_form.remember.data

        get_user = db.session.execute(db.select(User).where(User.email == email)).scalar()
        # print(get_user_data)

        if get_user and bcrypt.check_password_hash(get_user.password, password):
            login_user(get_user, remember=remember_me)
            next_page = request.args.get('next')

            flash(f"successfully logged in user {get_user.username}!", category="success")
            return redirect(next_page or url_for('main.home'))
        else:
            flash("please enter the correct details", category="danger")

    return render_template('login.html', form=login_form, title='login')


@users.route("/logout")
def logout():
    if not current_user.is_authenticated:
        flash("You are already logged out!", category="warning")
        return redirect(url_for("users.login"))

    logout_user()
    flash("User logged out successfully", category="info")
    return redirect(url_for("main.home"))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        if form.picture.data:
            picture_filename = save_picture(form.picture.data)
            current_user.image_file = picture_filename

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()

        flash(message="Your account has been updated!", category='success')
        return redirect(url_for('users.account'))
    
    elif request.method == 'GET':   # prefilled user details in form
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename=f'profile_pics/{current_user.image_file}')

    return render_template('account.html', image_file=image_file, form=form, title='account')



@users.route('/remove_img', methods=['GET', 'POST'])
@login_required
def remove_profile_image():

    if current_user.image_file != 'default.jpg':
        
        previous_img_path = os.path.join(current_app.root_path, 'static/profile_pics', current_user.image_file)

        if os.path.isfile(previous_img_path):
            os.remove(previous_img_path)    # remove previous image then set it to default

        current_user.image_file = 'default.jpg'
        db.session.commit()

        flash('Your profile picture has been removed.', 'warning')
    else:
        flash("Can't remove. Image is already the default one.", 'warning')

    return redirect(url_for('users.account'))  # Redirect to the profile page or where necessary


@users.route("/user/<string:username>")
def user_posts(username):
    user = db.first_or_404(db.select(User).where(User.username == username))
    page = request.args.get('page', 1, type=int)
    per_page = 2

    posts = db.paginate(
        db.select(Post).where(Post.author == user).order_by(Post.date_posted.desc()),
        page=page,
        per_page=per_page,
        error_out=False
    )

    return render_template('user_posts.html', title='User Posts', user=user, posts=posts)

