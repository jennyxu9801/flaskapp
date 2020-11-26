from flask import render_template, request, Blueprint
from flaskapp.models import Post, Book, Review
from flaskapp.posts.forms import SearchForm
from flask import (render_template, url_for, flash,
                   redirect)
main = Blueprint('main',__name__)

@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=2)

    return render_template('home.html', posts=posts)


@main.route("/about")
def about():
    return render_template('about.html', title='About')

@main.route("/search", methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        
        if form.category.data =='1':
            book = Book.query.filter_by(title=form.content.data).first_or_404()
        '''elif form.category == 'Author':
            book = Book.query.filter_by(author=form.content.data).first_or_404()
'''
        return redirect(url_for('posts.book',asin=book.asin, book=book))
    
    return render_template('search.html', title='Search',
                           form=form)

@main.route("/reviews")
def review():
    page = request.args.get('page', 1, type=int)
    reviews = Review.query.order_by(
        Review.reviewTime.desc()).paginate(page=page, per_page=15)

    return render_template('review.html', reviews=reviews)




















