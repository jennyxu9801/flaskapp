#%% Setting the data path

import pandas as pd
import datetime

datapath = 'C:\\Users\\x5021\\Downloads\\archive\\kindle_reviews.csv'

#%% Read the csv file into pandas dataframe

colnames=['id', 'asin', 'helpful', 'overall','reviewText','reviewTime','reviewerID','reviewerName','summary','unixReviewTime'] 

data = pd.read_csv(datapath,names=colnames, header=None)
data = data.drop(index =0)

print(data.head())

#%% Connect to the database

from sqlalchemy import create_engine
engine = create_engine('sqlite:///site.db')

import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mongo"]

#%% Create table from base models
    
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
    genre = Column(String(100))
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
    
    

#%% Create session and process review info from kaggle
from sqlalchemy.orm import sessionmaker
import re

# create a configured "Session" class
Session = sessionmaker(bind=engine)

# create a Session
session = Session()

#%% Process review info from kaggle

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
    if counter==100:
        
        print(f'commiting {big_counter}00')
        session.commit()
        big_counter+=1
        counter=0

session.commit()
print('Finish writing reviews to sqlite database')

#%% Clean the unstandard json file and save as new one
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

#%% Read the metadata into pandas dataframe

import pandas as pd
df = pd.read_json (r'C:\\Users\\x5021\\Downloads\\meta_kindle_store\\new_meta_Kindle_Store.json',lines=True)
print (df['categories'])


#%%  Create session and process books info 

session.rollback()
counter=0
big_counter=0
book_ls =[]
genre_ls = []

for index,book in df.iterrows():
   
    bookasin=book['asin']
    genre = book['categories']
    

    newbook = Book(asin = book['asin'],description = book['description'],
                       price = book['price'],imUrl = book['imUrl'],
                       title = book['title'],brand = book['brand'],genre = str(genre))
    
    #keeping a distinct book list for creating the relational db for books
    if bookasin not in book_ls:
        session.add(newbook)
        book_ls.append(bookasin)          
    counter+=1
    
    if counter==100:
        
        print(f'commiting {big_counter}00')
        session.commit()
        big_counter+=1
        counter=0
    
    '''if big_counter == 10:  # for testing purpose, we dont need full data to test 
        break'''
        
session.commit()
print('Finish writing metadata to sqlite database')


#%% Processing metadata and store into mongodb
  
import json
collection_books = mydb['book']

data = [json.loads(line) for line in open('C:\\Users\\x5021\\Downloads\\meta_kindle_store\\new_meta_Kindle_Store.json', 'r')]
collection_books.insert_many(data)

#%%
import re
# This function will return a dictionary of all the categories with subcategories
def build_dic_cat(ls,totaldic):
    dicutil={}
    #ls is a list of list
    for sublst in ls:   #['Books', 'Literature & Fiction']
        
        i=0
        dicfor1 ={}
        element1=re.sub(r"\.+", "", sublst[i])  #'Books'
        if element1 not in totaldic.keys():
            totaldic[element1]=dicfor1 
            

        i+=1
        
        if len(sublst)==i:
            continue
        
        dicfor2={}
        dicutil= totaldic[element1]
        element2=re.sub(r"\.+", "", sublst[i]) #lit and fic
        if element2 not in dicutil.keys():
            dicutil[element2]=dicfor2
            
            
        i+=1
        if len(sublst)==i:
            continue
        
        dicfor3={}
        dicutil=dicutil[element2]
        element3=re.sub(r"\.+", "", sublst[i])
        if element3 not in dicutil.keys():
            dicutil[element3]=dicfor3
            
        i+=1
        if len(sublst)==i:
            continue
        
        dicfor4={}
        dicutil=dicutil[element3]
        element4=re.sub(r"\.+", "", sublst[i])
        if element4 not in dicutil.keys():
            dicutil[element4]=dicfor4
            
        i+=1
        if len(sublst)==i:
            continue
        
        dicfor5={}
        dicutil=dicutil[element4]
        element5=re.sub(r"\.+", "", sublst[i])
        if element5 not in dicutil.keys():
            dicutil[element5]=dicfor5
            
        i+=1
        if len(sublst)==i:
            continue
        
        
    
    return totaldic
    




#%%

cat_dic={}
for book in collection_books.find():
    genre = book["categories"]
    cat_dic = build_dic_cat(genre,cat_dic)

with open('categories.json', 'w') as fp:
    json.dump(cat_dic, fp)
    
# back up the categories in mongodb
collection_categories = mydb['categories']
collection_categories.insert_one(cat_dic)

#%% Drop table in case that need to reset the table

Book.__table__.drop(engine)




