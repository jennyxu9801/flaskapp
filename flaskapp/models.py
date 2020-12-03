from flaskapp import db,login_manager
import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from flask import current_app,url_for

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable = False, default ='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post',backref='author',lazy=True)

    def get_reset_token(self,expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'],expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def veryfy_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try: 
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime,  nullable=False, default = datetime.datetime.utcnow() + datetime.timedelta(hours=8))
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"

class Book(db.Model):
    asin = db.Column(db.String(100), primary_key = True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    imUrl = db.Column(db.String(100), nullable=False, default ='def_book_cover/defbookcover.jpg')
    brand = db.Column(db.String(100), nullable=False)
    reviews = db.relationship('Review',backref='book',lazy=True)
    description = db.Column(db.Text, default = 'No text')
    def __repr__(self):
        return f"Book('{self.title}','{self.asin}')"

class Review(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    asin = db.Column(db.String(100), db.ForeignKey('book.asin'),nullable=False)
    helpful = db.Column(db.String(10))
    overall = db.Column(db.Integer,  default = 0)
    reviewText = db.Column(db.Text, default = 'No text')
    reviewTime = db.Column(db.DateTime,  nullable=False, default = datetime.datetime.utcnow() + datetime.timedelta(hours=8))
    reviewerID = db.Column(db.String(100), db.ForeignKey('reviewer.id'),nullable=False)
    summary = db.Column(db.String(100) )
    unixReviewTime = db.Column(db.String(100), default = int(datetime.datetime.now().timestamp()) )

    def __repr__(self):
        return f"Review('{self.reviewerID}','{self.reviewText}')"

class Reviewer(db.Model):
    id = db.Column(db.String(100), primary_key = True)
    name = db.Column(db.String(100), nullable=False)
    reviews = db.relationship('Review',backref='reviewer',lazy=True)

    def __repr__(self):
        return f"Reviewer('{self.id}','{self.name}')"

