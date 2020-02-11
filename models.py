import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()
# We would change the ENV variable during development and production
ENV = 'prod'


def setup_db(app, ENV=ENV):
    '''Binds a flask application and a SQLAlchemy service'''
    if ENV == 'dev':
        app.debug = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ajitesh@localhost:5432/mockdb'
    else:
        app.debug = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://bsmfjjpvmspejy:8037411620a3fed176d4f8843eb2a308fac61d07863277e73d45dacc7df96a97@ec2-35-168-54-239.compute-1.amazonaws.com:5432/d3d5h5hckmgn9d'

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app

    db.init_app(app)
#No create all will be required, as we're using flask_migrate

class Party(db.Model):
    __tablename__ = 'Party'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    part_symbol =  db.Column(db.String(180))


    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'part_symbol': self.part_symbol
        }


    def insert(self):
        db.session.add(self)
        db.session.commit()


    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class Politician(db.Model):
    __tablename__ = 'Politician'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    image_link =  db.Column(db.String(180))
    famous_posts = db.Column(db.String(500))
    party_id = db.Column(db.Integer, db.ForeignKey('Party.id'), nullable=False)
    party = db.relationship('Party', backref=db.backref('politicians', lazy=True))
# plural (politicians) used in backref as party could have multiple politicians


    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'image_link': self.image_link,
            'famous_posts': self.famous_posts,
            'party_id': self.party_id
        }


    def insert(self):
        db.session.add(self)
        db.session.commit()


    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class Quotes(db.Model):
    __tablename__ = 'Quotes'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500))
    topic = db.Column(db.String(180))
    party_id = db.Column(db.Integer, db.ForeignKey('Party.id'), nullable=False)
    party = db.relationship('Party', backref=db.backref('quotes', lazy=True))
    politician_id = db.Column(db.Integer, db.ForeignKey('Politician.id'), nullable=False)
    politician = db.relationship('Politician', backref=db.backref('quotes', lazy=True))


    def format(self):
        return {
            'id': self.id,
            'text': self.text,
            'topic': self.topic,
            'party_id': self.party_id,
            'politician_id': self.politician_id
        }


    def insert(self):
        db.session.add(self)
        db.session.commit()


    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
