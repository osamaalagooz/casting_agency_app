import os
from sqlalchemy import Column, String, Integer,DateTime, create_engine, ForeignKey,Date
from flask_sqlalchemy import SQLAlchemy
import json
from flask_migrate import Migrate
# database_name = 'casting'
# datebase_path = "postgres://{}:{}@{}/{}".format('postgres', 'robot9000','localhost:5432', database_name)
datebase_path = "postgres://sdguovfclpgcna:f7a43ac36efaed20c7a467dd55388f7ba6c07a703e88ede7efa65ea44832689e@ec2-52-71-85-210.compute-1.amazonaws.com:5432/d5ics59q8du01e"
db = SQLAlchemy()
migrate = Migrate()
'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, datebase_path=datebase_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = datebase_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate.init_app(app, db)
    #db.create_all()



class Movie(db.Model):
    __tablename = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)   
    release_date = Column(Date)
    image_url = Column(String)
    stuff = db.relationship('Actor', backref='show' )

    def __init__(self, title,release_date, image_url):
        self.title = title
        self.release_date = release_date
        self.image_url = image_url
       
    

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
        'id': self.id,
        'title': self.title,
        'release_date': self.release_date,
        'image_url': self.image_url
        }

class Actor(db.Model):
    __tablename = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    age = Column(Integer)
    gender = Column(String)
    image_url = Column(String)
    movie_id = Column(Integer, ForeignKey('movie.id'), nullable=True)

      
    def __init__(self, name,age,gender, movie_id, image_url):
        self.name = name
        self.age = age
        self.gender = gender
        self.movie_id = movie_id
        self.image_url = image_url
        
    

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
        'id': self.id,
        'name': self.name,
        'age': self.age,
        'gender': self.gender,
        'movie_id': self.movie_id,
        'image_url': self.image_url
        
        }

