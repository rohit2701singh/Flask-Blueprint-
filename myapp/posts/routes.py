from flask import Blueprint, request, redirect, render_template, url_for, flash, abort
from myapp.posts.forms import PostForm
from myapp.models import Post
from flask_login import login_required, current_user
from myapp import db

posts = Blueprint('posts', __name__)

@posts.route("/all_post")
def all_posts():
    # posts = db.session.execute(db.select(Post).order_by(Post.id.desc())).scalars()
    # return render_template('all_posts.html', title='All Post', posts=posts, image_file=show_image_in_web())

    page = request.args.get('page', 1, type=int)  # page number from query params, default page=1
    per_page = 4  # Number of posts per page

    posts = db.paginate(db.select(Post).order_by(Post.date_posted.desc()), page=page, per_page=per_page, error_out=False)
    return render_template('all_posts.html', title='All Post', posts=posts)


@posts.route("/post/new" , methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()

        flash(message="Your post has been created!", category='success')
        return redirect(url_for('posts.all_posts'))
    return render_template('create_post.html', title='New Post', form=form, legend='Create New Post')


@posts.route("/post/<int:post_id>")
def post_details(post_id):
    post = db.get_or_404(Post, post_id)

    return render_template('post.html', title=post.title, post=post)



@posts.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = db.get_or_404(Post, post_id)

    if post.author != current_user: 
        abort(403)
    
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash(message="Your post has been updated!", category='success')
        return redirect(url_for('posts.post_details', post_id=post.id))
    
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content

    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = db.get_or_404(Post, post_id)

    if post.author != current_user: 
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash(message="Your post has been deleted", category="success")
    
    return redirect(url_for('posts.all_posts'))
