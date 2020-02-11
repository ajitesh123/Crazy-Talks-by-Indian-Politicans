import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from models import setup_db, db, Party, Politician, Quotes
from auth import AuthError, requires_auth

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

    data = []
    new_dict = {}

    for quote in quotes:
        new_dict["text"] = quote.text
        new_dict["Politican"] = Politician.query.filter_by(id=quote.politician_id).all()[0].name
        new_dict["Party"] = Party.query.filter_by(id=quote.party_id).all()[0].name
        data.append(new_dict)
        new_dict = {}

    return jsonify({
        'success': True,
        'quotes': data
        })


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drink_detail(jwt):
    '''
    Fetch the long form representation of the drinks
    '''
    drinks = Drink.query.all()

    if len(drinks) == 0:
        abort(404)

    formatted_drinks = [drink.format() for drink in drinks]

    return jsonify({
        'success': True,
        'drinks': formatted_drinks
        })


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_detail(jwt):
    '''
    Add a new drink in the drinks table
    '''
    body = request.get_json()
    new_title = body['title']
    recipe_json = body['recipe']

    new_drink = Drink(
                title=new_title,
                recipe=json.dumps(recipe_json))

    new_drink.insert()

    return jsonify({
        'success': True,
        'drinks': [new_drink.long()]
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
