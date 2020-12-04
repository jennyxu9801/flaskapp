from flask import render_template, request, Blueprint
from flaskapp.models import Post, Book, Review
from flaskapp.posts.forms import SearchForm, OrderByForm
from flask import (render_template, url_for, flash,
                   redirect)
from flaskapp import db
from sqlalchemy.sql import func,desc,asc
import json,sqlalchemy

main = Blueprint('main',__name__)
f = open('C:\\Users\\x5021\\OneDrive\\桌面\\flask_app\\flaskapp\\categories.json') 
categorydata = json.load(f)
categorykey=categorydata.keys()




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
    #print(categorydata,flush=True)
    return render_template('search.html', title='Search',
                           form=form,categorykey =categorykey)

@main.route("/search/category/<string:category>", methods=['GET', 'POST'])
def search_cat(category):
    form = SearchForm()
    if form.validate_on_submit():
        if form.category.data =='1':
            return redirect(url_for('main.search_result',search=form.content.data))

    page = request.args.get('page', 1, type=int)
    books= Book.query.filter(Book.genre.contains(category)).paginate(page=page, per_page=5)
    try:
        categorykey= gen_dict_extract(categorydata,category).keys()
    except AttributeError:
        categorykey={}
    
    
    return render_template('search_cat.html', title='Search',
                           form=form,books=books,categorykey=categorykey)

@main.route("/search/<string:search>/result")
def search_result(search):
    page = request.args.get('page', 1, type=int)
    books= Book.query.filter(Book.title.contains(search)).paginate(page=page, per_page=5)
    return render_template('search_result.html',books=books,search=search)



@main.route("/reviews")
def review():
    page = request.args.get('page', 1, type=int)
    reviews = Review.query.order_by(
        Review.reviewTime.desc()).paginate(page=page, per_page=5)

    return render_template('review.html', reviews=reviews)

@main.route("/",methods=['GET', 'POST'])
@main.route("/books",methods=['GET', 'POST'])
def book():
    form = OrderByForm()
    try:
        if form.is_submitted():
            
            if form.orderby.data =='1': #[(1, 'Rating (desc)'), (2, 'Rating (asc)')]) 
                return redirect(url_for('main.order_by_rating_desc'))
            elif form.orderby.data =='2': 
                return redirect(url_for('main.order_by_rating_asc'))

        page = request.args.get('page', 1, type=int)
        books = Book.query.order_by(
                    Book.title.desc()).paginate(page=page, per_page=5)
        return render_template('books.html', form=form, books=books )
    except:
        return render_template('errors/unknown.html')
        
    
    


@main.route("/orderby/rating_desc")
def order_by_rating_desc():
    try:
        page = request.args.get('page', 1, type=int)

        #book = db.session.query( Review.asin, func.avg(Review.overall).label('avg_rating') ).group_by(Review.asin).order_by(desc('avg_rating')).first()
        asin_and_avg = db.session.query( Review.asin,func.avg(Review.overall).label('avg_rating')).group_by(Review.asin).subquery()
        books = db.session.query(Book.title,Book.asin,Book.brand,Book.imUrl,Book.price, asin_and_avg.c.avg_rating).outerjoin(Book,asin_and_avg.c.asin == Book.asin).order_by(desc('avg_rating')).paginate(page=page, per_page=5)

        return render_template('orderby_rating.html',books=books,order = 1)
    except :
        return render_template('errors/unknown.html')
    

@main.route("/orderby/rating_asc")
def order_by_rating_asc():
    page = request.args.get('page', 1, type=int)
    asin_and_avg = db.session.query( Review.asin,func.avg(Review.overall).label('avg_rating')).group_by(Review.asin).subquery()
    books = db.session.query(Book.title,Book.asin,Book.brand,Book.imUrl,Book.price, asin_and_avg.c.avg_rating).outerjoin(Book,asin_and_avg.c.asin == Book.asin).order_by(asc('avg_rating')).paginate(page=page, per_page=5)

    return render_template('orderby_rating.html',books=books,order= 2)
    
 
    

def gen_dict_extract(var, key):
    if type(var)!={}:
        for k, v in var.items():
            if k == key:
                return v
            if isinstance(v, dict):
                ans= gen_dict_extract(v, key)
                if ans!={} and ans!=None:
                    return ans




















