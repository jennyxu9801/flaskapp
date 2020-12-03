from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskapp import db
from flaskapp.models import Post, Book, Review
from flaskapp.posts.forms import PostForm,NewReviewForm,NewBookForm

posts = Blueprint('posts',__name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()

        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend="New Post")


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title='post.title', post=post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

    return render_template('create_post.html', title='Update post',
                           form=form, legend="Update Post")


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))

@posts.route("/book/<string:asin>")
def book(asin):
    page = request.args.get('page', 1, type=int)
    reviews = Review.query.filter_by(asin= asin).order_by(
        Review.reviewTime.desc()).paginate(page=page, per_page=5)

    book = Book.query.get_or_404(asin)
    return render_template('book.html', title='book.title', book=book, reviews= reviews)



@posts.route("/review/new", methods=['GET', 'POST'])
@login_required
def new_review():
    form = NewReviewForm()

    try:
        book = Book.query.filter_by(title=form.bookTitle.data).first()
        if form.validate_on_submit():
            review = Review(asin=book.asin,overall=form.rating.data, reviewerID=current_user.id,reviewText = form.review.data,summary=form.summary.data)
            db.session.add(review)
            db.session.commit()

            flash('Your review has been created!', 'success')
            return redirect(url_for('main.home'))
        return render_template('new_review.html', title='New Review',
                            form=form)
    except AttributeError:
        flash('The book does not exist, please add new book first!', 'warning')
        return render_template('new_review.html', title='New Review',
                            form=form)

@posts.route("/book/new", methods=['GET', 'POST'])
@login_required
def new_book():
    form = NewBookForm()
    try:
        if form.validate_on_submit():
            book = Book(asin=form.asin.data,title=form.title.data, price=form.price.data,brand = form.brand.data,description=form.description.data)
            db.session.add(book)
            db.session.commit()
            flash('New book has been added!', 'success')
            return redirect(url_for('main.home'))
        return render_template('new_book.html', title='New Book',
                            form=form)
    except AttributeError:
        flash('The book does not exist, please add new book first!', 'warning')
        return render_template('new_book.html', title='New Book',
                            form=form)












