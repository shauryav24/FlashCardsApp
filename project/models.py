from . import db

class User(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, nullable="False") 
    username = db.Column(db.String(100), primary_key=True,nullable="False",unique=True)
    password = db.Column(db.String(100),nullable="False")

class Deck(db.Model):
    __tablename__ = 'deck'

    deck_id = db.Column(db.Integer)
    deck_name = db.Column(db.String(100),primary_key=True )
    creator = db.Column(db.String(100),db.ForeignKey('user.username'), nullable=False)
    score = db.Column(db.Float, nullable=True)
    is_public = db.Column(db.Boolean, default=False)
    last_reviewed = db.Column(db.DateTime, nullable=True)

    user = db.relationship('User')

class Card(db.Model):
    __tablename__ = 'card'
    index= db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer)
    part_of_deck = db.Column(db.ForeignKey('deck.deck_name'), nullable=False)
    front = db.Column(db.String(100), nullable=False)
    back = db.Column(db.String(100), nullable=False)
    partial = db.Column(db.Integer)

    deck = db.relationship('Deck')

