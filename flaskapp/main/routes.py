from flask import render_template, request, Blueprint
from flaskapp.models import Post, Book, Review
from flaskapp.posts.forms import SearchForm, OrderByForm
from flask import (render_template, url_for, flash,
                   redirect)
from flaskapp import db
from sqlalchemy.sql import func,desc
import sys

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
        #print("entered search",flush=True)
        if form.category.data =='1':
            return redirect(url_for('main.search_result',search=form.content.data))
        
    
    return render_template('search.html', title='Search',
                           form=form)

@main.route("/search/<string:search>/result")
def search_result(search):
    page = request.args.get('page', 1, type=int)
    books = Book.query.filter(Book.title.contains(search)).paginate(page=page, per_page=5)
    return render_template('search_result.html',books=books,search=search)


@main.route("/reviews")
def review():
    page = request.args.get('page', 1, type=int)
    reviews = Review.query.order_by(
        Review.reviewTime.desc()).paginate(page=page, per_page=15)

    return render_template('review.html', reviews=reviews)

@main.route("/books",methods=['GET', 'POST'])
def book():
    form = OrderByForm()
    print(form.orderby.data,flush=True)
    if form.is_submitted():
        print("first if",flush=True)
        if form.orderby.data =='1': #[(1, 'Rating'), (2, 'Title')]) 
            print("second if",flush=True)
            flash('Your have selected rating!', 'success')
            page = request.args.get('page', 1, type=int)

            '''books = Book.query.with_entities(func.avg(Book.query.join(Review).overall.label('avg_rating'))).order_by(
                Book.avg_rating.desc()).paginate(page=page, per_page=5)
            books = Review.query.group_by(Review.asin)'''

            #book = db.session.query( Review.asin, func.avg(Review.overall).label('avg_rating') ).group_by(Review.asin).order_by(desc('avg_rating')).first()
            books = db.session.query( Review.asin,Book.query.filter_by(asin=Review.asin).first().title,func.avg(Review.overall).label('avg_rating')).group_by(Review.asin).order_by(desc('avg_rating')).paginate(page=page, per_page=5)
            #order_by(desc('avg_rating')).paginate(page=page, per_page=5)
            #print(book,flush=True)
            
        '''else:
            page = request.args.get('page', 1, type=int)     
            books = Book.query.order_by(
                Book.title.desc()).paginate(page=page, per_page=5)'''
        
    
        return render_template('orderby_result.html', books=books )

    page = request.args.get('page', 1, type=int)
    books = Book.query.order_by(
                Book.title.desc()).paginate(page=page, per_page=5)
    print("before if",flush=True)
    return render_template('books.html', form=form, books=books )
    
 
    






















