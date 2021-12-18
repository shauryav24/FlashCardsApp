from flask import Blueprint, render_template, redirect, request, flash
from . import db
from .models import Deck, Card
from datetime import datetime

views = Blueprint('views', __name__)


@views.route('/')
def index():
    return render_template('index.html')


@views.route('/dashboard/<username>')
def dashboard(username):
    decks = Deck.query.filter_by(creator=username).all()
    return render_template('dashboard.html', username=username, decks=decks)


@views.route('/begin/<deck_name>')
def begin(deck_name):
    t = datetime.now()
    deck = Deck.query.filter_by(deck_name=deck_name).first()
    deck.last_reviewed = t
    db.session.commit()

    return redirect('/review/' + deck_name)


@views.route('/review/<deck_name>')
def review(deck_name):
    card = Card.query.filter_by(part_of_deck=deck_name, card_id=1).first()
    if card == None:
        flash('Please create a card to review it.')
        return render_template('create_card.html', deck_name=deck_name)

    deck = Deck.query.filter_by(deck_name=deck_name).first()
    username = deck.creator
    return render_template('review.html',
                           card=card,
                           deck_name=deck_name,
                           username=username)


@views.route('/review/<deck_name>/<card_id>', methods=["GET", "POST"])
def review_next(deck_name, card_id):
    if request.method == "POST":
        partialscore = request.values.get('partialscore')

        c = Card.query.filter_by(part_of_deck=deck_name,
                                 card_id=card_id).first()
        c.partial = int(partialscore)
        

        db.session.commit()

        cards = Card.query.filter_by(part_of_deck=deck_name).all()
        total = 0
        for cd in cards:
            total = total + cd.partial

        count = Card.query.filter_by(part_of_deck=deck_name).count()
        new_score = int(total / count)

        deck = Deck.query.filter_by(deck_name=deck_name).first()

        username = deck.creator
        deck.score = new_score
        db.session.commit()

        card_id = int(card_id) + 1
        card = Card.query.filter_by(part_of_deck=deck_name,
                                    card_id=card_id).first()
        if card == None:
            return redirect('/dashboard/' + username)

        return render_template('review.html',
                               card=card,
                               deck_name=deck_name,
                               username=username)
    else:
        card = Card.query.filter_by(part_of_deck=deck_name,
                                    card_id=card_id).first()
        return render_template('review.html', card=card, deck_name=deck_name)


@views.route('/about')
def about():
    return render_template('about.html')


@views.route('/all_cards/<deck_name>')
def all_cards(deck_name):
    cards = Card.query.filter_by(part_of_deck=deck_name).all()
    deck = Deck.query.filter_by(deck_name=deck_name).first()
    print(deck)
    username = deck.creator
    return render_template('all_cards.html',
                           cards=cards,
                           deck_name=deck_name,
                           username=username)


@views.route('/create_card/<deck_name>')
def create_card(deck_name):
    return render_template('create_card.html', deck_name=deck_name)


@views.route('/create_card/<deck_name>', methods=["POST"])
def created_card(deck_name):
    front = request.form.get('front')
    back = request.form.get('back')

    if front == "" or back == "":
        flash('Card cannot be empty. Please try again.')
        return redirect('/create_card/' + deck_name)

    count = Card.query.filter_by(part_of_deck=deck_name).count()
    count = count + 1
    card = Card.query.filter_by(front=front, back=back,part_of_deck=deck_name).first()
    if card:
        flash('Card already exists')
        return redirect('/create_card/' + deck_name)

    new_card = Card(card_id=count,
                    part_of_deck=deck_name,
                    front=front,
                    back=back)

    db.session.add(new_card)
    db.session.commit()

    cards = Card.query.filter_by(part_of_deck=deck_name).all()
    return render_template('all_cards.html', cards=cards, deck_name=deck_name)


@views.route('/create_deck/<username>')
def create_deck(username):
    return render_template('create_deck.html', username=username)


@views.route('/create_deck/<username>', methods=["POST"])
def created_deck(username):
    deck_name = request.form.get('deck_name')

    count = Deck.query.count()
    count = count + 1
    deck = Deck.query.filter_by(deck_name=deck_name).first()
  
    if deck_name == "":
        flash('Deck name cannot be empty. Please try again.')
        return redirect('/create_deck/' + username)

    if deck:
        flash('Deck already exists')
        return redirect('/create_deck/' + username)
    


    new_deck = Deck(deck_id=count,
                    deck_name=deck_name,
                    creator=username,
                    score=None,
                    is_public=True)

    db.session.add(new_deck)
    db.session.commit()

    return redirect('/dashboard/' + username)


@views.route('/edit_card/<deck_name>/<card_id>')
def edit_card(deck_name, card_id):
    card = Card.query.filter_by(part_of_deck=deck_name,
                                card_id=card_id).first()

    return render_template('edit_card.html', card=card)


@views.route('/edit_card/<deck_name>/<card_id>', methods=["POST"])
def edited_card(deck_name, card_id):
    front = request.form.get('front')
    back = request.form.get('back')

    if front == "" or back == "":
        flash('Card cannot be empty. Please try again.')
        return redirect('/edit_card/' + deck_name + '/' + card_id)

    card = Card.query.filter_by(front=front, back=back,part_of_deck=deck_name).first()
    if card:
        flash('Card already exists')
        return redirect('/create_card/' + deck_name)

    Card.query.filter_by(card_id=card_id,
                         part_of_deck=deck_name).update(dict(front=front))
    Card.query.filter_by(card_id=card_id,
                         part_of_deck=deck_name).update(dict(back=back))
    db.session.commit()

    cards = Card.query.filter_by(part_of_deck=deck_name).all()
    return render_template('all_cards.html', cards=cards, deck_name=deck_name)


@views.route('/delete_card/<deck_name>/<card_id>')
def delete_card(deck_name, card_id):
    card = Card.query.filter_by(part_of_deck=deck_name,
                                card_id=card_id).first()

    db.session.delete(card)
    db.session.commit()

    return redirect('/all_cards/' + deck_name)


@views.route('/delete_deck/<deck_name>')
def delete_deck(deck_name):
    cards = Card.query.filter_by(part_of_deck=deck_name).all()
    for card in cards:
        db.session.delete(card)
    db.session.commit()

    deck = Deck.query.filter_by(deck_name=deck_name).first()
    username = deck.creator
    db.session.delete(deck)
    db.session.commit()

    return redirect('/dashboard/' + username)


@views.route('/edit_deck/<username>/<deck_name>')
def edit_deck(deck_name,username):
    deck = Deck.query.filter_by(deck_name=deck_name).first()
    return render_template('edit_deck.html', deck=deck,username=username)


@views.route('/edit_deck/<username>/<deck_name>', methods=["POST"])
def edited_deck(deck_name,username):
    new_deck_name = request.form.get('deck_name')

    deck = Deck.query.filter_by(deck_name=new_deck_name,creator=username).first()

    if deck:
        flash('Deck already exists')
        return redirect('/edit_deck/'+username+'/' + deck_name)

    Card.query.filter_by(part_of_deck=deck_name).update(dict(part_of_deck=new_deck_name))

    Deck.query.filter_by(deck_name=deck_name).update(
        dict(deck_name=new_deck_name))
    deck = Deck.query.filter_by(deck_name=new_deck_name).first()
    username = deck.creator
    db.session.commit()

    return redirect('/dashboard/' + username)
