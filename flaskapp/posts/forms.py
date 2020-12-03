
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit =   SubmitField('Post')

class SearchForm(FlaskForm):
    category = SelectField('Category', validators=[DataRequired()],choices=[(1, 'Book'), (2, 'Author')])
    content = StringField('Content', validators=[DataRequired()])
    search =   SubmitField('Search')

class OrderByForm(FlaskForm):
    orderby = SelectField('Order By',choices=[(1, 'Rating(desc)'), (2, 'Rating(asc)')])
    gernes = SelectField('Gernes',choices=[(1, 'All'), (2, 'Title')])
    search =   SubmitField('Search')

class NewReviewForm(FlaskForm):
    bookTitle = StringField('Book Title', validators=[DataRequired()])
    rating = SelectField('Rating',validators=[DataRequired()],choices=[(1, '1'), (2, '2'),(3,'3'),(4,'4'),(5,'5')])
    summary = StringField('Summary', validators=[DataRequired()])
    review = TextAreaField('Review', validators=[DataRequired()])
    submit =   SubmitField('Post Review')

class NewBookForm(FlaskForm):
    title = StringField('Book Title', validators=[DataRequired()])
    asin = StringField('asin', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
    brand = StringField('Brand')
    description = TextAreaField('Description', validators=[DataRequired()])
    submit =   SubmitField('Add Book')
    

















