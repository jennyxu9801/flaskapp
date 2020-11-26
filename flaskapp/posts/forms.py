
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit =   SubmitField('Post')

class SearchForm(FlaskForm):
    category = SelectField('Category', validators=[DataRequired()],choices=[(1, 'Book'), (2, 'Author')])
    content = TextAreaField('Content', validators=[DataRequired()])
    search =   SubmitField('Search')

class ReviewForm(FlaskForm):
    bookTitle = StringField('Book Title', validators=[DataRequired()])
    rating = SelectField('Rating',validators=[DataRequired()],choices=[(1, '1'), (2, '2'),(3,'3'),(4,'4'),(5,'5')])
    content = StringField('Summary', validators=[DataRequired()])
    content = TextAreaField('Review', validators=[DataRequired()])
    submit =   SubmitField('Post Review')
    

















