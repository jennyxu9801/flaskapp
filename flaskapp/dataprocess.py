import pandas as pd
import datetime

datapath = 'C:\\Users\\x5021\\Downloads\\archive\\kindle_reviews.csv'

#%%
colnames=['id', 'asin', 'helpful', 'overall','reviewText','reviewTime','reviewerID','reviewerName','summary','unixReviewTime'] 

data = pd.read_csv(datapath,names=colnames, header=None)
data = data.drop(index =0)

print(data.head())

#%%

from sqlalchemy import create_engine
engine = create_engine('sqlite:///site.db')

print(engine.table_names())

#%%
    
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Book(Base):
    __tablename__  ='book'
    asin = Column(String(100), primary_key = True)
    description = Column(Text, default = 'No text.')
    title = Column(String(100))
    price = Column(Integer, default = 0)
    imUrl = Column(String(100))
    brand = Column(String(100))
    reviews = relationship('Review',backref='book',lazy=True)

    def __repr__(self):
        return f"Book('{self.title}','{self.asin}')"

class Review(Base):
    __tablename__  ='review'
    id = Column(Integer, primary_key = True)
    asin = Column(String(100), ForeignKey('book.asin'),nullable=False)
    helpful = Column(String(10) )
    overall = Column(Integer,  default = 0)
    reviewText = Column(Text, default = 'No text.')
    reviewTime = Column(DateTime,  nullable=False, default = datetime.datetime.utcnow() + datetime.timedelta(hours=8))
    reviewerID = Column(String(100), ForeignKey('reviewer.id'),nullable=False)
    summary = Column(String(100))
    unixReviewTime = Column(String(100),nullable=False, default = int(datetime.datetime.now().timestamp()) )
   
    def __repr__(self):
        return f"Review('{self.reviewerID}','{self.reviewText}')"

class Reviewer(Base):
    __tablename__  ='reviewer'
    id = Column(String(100), primary_key = True)
    name = Column(String(100), default = ' ')
    reviews = relationship('Review',backref='reviewer',lazy=True)

    def __repr__(self):
        return f"Reviewer('{self.id}','{self.name}')"

Base.metadata.create_all(engine)
    
    

#%%
from sqlalchemy.orm import sessionmaker
import re

# create a configured "Session" class
Session = sessionmaker(bind=engine)

# create a Session
session = Session()
counter=0
big_counter=0
reviewer_ls =[]

for index,review in data.iterrows():
    s = review['reviewTime']
    s = re.sub(r'[^\w\s]','',s)
    
    reviewer=review['reviewerID']
    
    newdateTime = datetime.datetime.strptime(s, '%m %d %Y')
    
    newreview = Review(id= review['id'],asin = review['asin'],helpful = review['helpful'],
                       overall = review['overall'],reviewText = review['reviewText'],reviewTime = newdateTime,
                       reviewerID = review['reviewerID'],summary = review['summary'],unixReviewTime = review['unixReviewTime'])
    newreviewer = Reviewer(id = review['reviewerID'], name = review['reviewerName'])
    session.add(newreview)
    
    if reviewer not in reviewer_ls:
        newreviewer = Reviewer(id = review['reviewerID'], name = review['reviewerName'])
        session.add(newreviewer)
        reviewer_ls.append(reviewer)
    
    
    counter+=1
    if counter==10:
        
        print(f'commiting {big_counter}')
        session.commit()
        big_counter+=1
        counter=0

session.commit()

#%%
session.rollback()

newBook1 = Book(asin = '1B000JMKQ0',title ='book1',price=1,imUrl ='sdfa', brand='apple')
newBook2 = Book(asin = '2B000JMNQ0',title ='book2',price=2,imUrl ='gfdsag', brand='tree')
newBook3 = Book(asin = '3B000JMKQ0',title ='book3',price=3,imUrl ='gsawet', brand='lemon')
newBook4 = Book(asin = '4B00JMKNQ0',title ='book4',price=4,imUrl ='jtyk', brand='grass')
newBook5 = Book(asin = '5B000MKNQ0',title ='book5',price=5,imUrl ='hrtsj', brand='hopper')
newBook6 = Book(asin = '6B000JMKNQ',title ='book6',price=6,imUrl ='ejyt', brand='jump')

session.add(newBook1)
session.add(newBook2)
session.add(newBook3)
session.add(newBook4)
session.add(newBook5)
session.add(newBook6)
session.commit()
#%%
session.rollback()
newBook1 = Book(asin = 'B000JMKX4W',title ='book7',price=7,imUrl ='sdfa', brand='apple')
session.add(newBook1)
session.commit()
#%%
import json
import ast

fr=open('C:\\Users\\x5021\\Downloads\\meta_kindle_store\\meta_Kindle_Store.json'
)
fw=open('C:\\Users\\x5021\\Downloads\\meta_kindle_store\\new_meta_Kindle_Store.json'
, "w")

for line in fr:
    json_dat = json.dumps(ast.literal_eval(line))
    dict_dat = json.loads(json_dat)
    json.dump(dict_dat, fw)
    fw.write("\n")

fw.close()
fr.close()

#%%

import pandas as pd
df = pd.read_json (r'C:\\Users\\x5021\\Downloads\\meta_kindle_store\\new_meta_Kindle_Store.json',lines=True)
print (df.head(5))

#%%
session.rollback()
counter=0
big_counter=0
book_ls =[]

for index,book in df.iterrows():
   
    bookasin=book['asin']

    newbook = Book(asin = book['asin'],description = book['description'],
                       price = book['price'],imUrl = book['imUrl'],
                       title = book['title'],brand = book['brand'])
    

    
    if bookasin not in book_ls:
        
        session.add(newbook)
        book_ls.append(bookasin)
    
    
    counter+=1
    if counter==10:
        
        print(f'commiting {big_counter}')
        session.commit()
        big_counter+=1
        counter=0

session.commit()



#%%

Book.__table__.drop(engine)




