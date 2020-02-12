import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from models import setup_db, db, Party, Politician, Quotes
from auth import AuthError, requires_auth

# ------------------------------------------------------------
#  Helper Functions
# -------------------------------------------------------------

LIST_PER_PAGE = 5


def paginate_list(request, selection, LIST_PER_PAGE = 5):
    '''Creates list of 5 quotes per page'''
    page = request.args.get('page', 1, type = int)
    start = (page-1) * LIST_PER_PAGE
    end = start + LIST_PER_PAGE

    current_list = selection[start:end]

    return current_list

# ------------------------------------------------------------
#  App Configurartion
# -------------------------------------------------------------

app = Flask(__name__)
setup_db(app)
CORS(app)

# ------------------------------------------------------------
#  Controllers
# -------------------------------------------------------------

@app.route('/')
def get_home():
    return jsonify({
        'success': True,
        'message': "Welcome to an API to fecth crazy things Indian politicians have said"
        })

@app.route('/quotes')
def get_quotes():
    '''
    Get quotes in a json format
    '''
    quotes = Quotes.query.all()

    if len(quotes) == 0:
        abort(404)

    formatted_quotes = [q.styled_format() for q in quotes]

    current_quotes = paginate_list(request, formatted_quotes)

    return jsonify({
        'success': True,
        'total_quotes': len(quotes),
        'quotes': current_quotes
        })


@app.route('/parties')
def get_parties():
    '''
    Fetch details of political parties in json format
    '''
    parties = Party.query.all()

    if len(parties) == 0:
        abort(404)

    formatted_parties = [party.styled_format() for party in parties]

    current_parties = paginate_list(request, formatted_parties, 2)

    return jsonify({
        'success': True,
        'parties': current_parties,
        'total_parties':len(parties)
        })


@app.route('/politicians')
def get_politicians():
    '''
    Fetch details of politicians in json format
    '''
    politicians = Politician.query.all()

    if len(politicians) == 0:
        abort(404)

    formatted_politicians = [politician.styled_format() for politician in politicians]

    current_politicians = paginate_list(request, formatted_politicians, 2)

    return jsonify({
        'success': True,
        'politicians': current_politicians,
        'total_politicians':len(politicians)
        })


@app.route('/quotes', methods=['POST'])
def create_quotes():
    '''
    Add a new quote to the repository
    '''
    body = request.get_json()

    text = body['text']
    topic = body['topic']
    party_id = body['party_id']
    politician_id = body['politician_id']


    new_quote = Quotes(
                text=text,
                topic=topic,
                party_id=party_id,
                politician_id=politician_id)

    new_quote.insert()

    return jsonify({
        'success': True,
        'quote': [new_quote.format()]
        })


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def change_detail(jwt, drink_id):
    '''
    Change details of the drink in the table
    '''
    try:
        drink = Drink.query.filter_by(id=drink_id).one_or_none()

# In case no such drink exists, then inform resource doesn't exist
        if drink is None:
            return abort(404)

        body = request.get_json()

        if 'title' in body:
            drink.title = body['title']

        if 'recipe' in body:
            drink.recipe = json.dumps(body['recipe'])

        drink.update()

        return jsonify({
            'success': True,
            'drinks': [drink.long()]
            })
    except:
        abort(422)


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(jwt, drink_id):
    '''
    Delete a drink from the tablew
    '''
    try:
        drink = Drink.query.filter_by(id=drink_id).one_or_none()

# In case no such drink exists, then inform resource doesn't exist
        if drink is None:
            return abort(404)

        drink.delete()

        return jsonify({
            'success': True,
            'delete': drink_id
            })
    except:
        abort(422)


# ---------------------------------------------------
#  Error Handler
# ----------------------------------------------------


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False,
                    "error": 422,
                    "message": "unprocessable"
                    }), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({
                    'success': False,
                    'error': 404,
                    'message': "Not found"
                    }), 404


@app.errorhandler(400)
def not_found(error):
    return jsonify({
                    'success': False,
                    'error': 400,
                    'message': "Bad request"
                    }), 400


@app.errorhandler(422)
def not_found(error):
    return jsonify({
                    'success': False,
                    'error': 422,
                    'message': "Unprocessable"
                    }), 422


@app.errorhandler(405)
def not_found(error):
    return jsonify({
                    'success': False,
                    'error': 405,
                    'message': "Method now allowed"
                    }), 405


@app.errorhandler(AuthError)
def Auth_Error(error):
    return jsonify({
                    'success': False,
                    'error': error.status_code,
                    'message': error.error['code']
                    }), error.status_code
