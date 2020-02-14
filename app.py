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
def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

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
    @requires_auth('post:quotes')
    def create_quotes(jwt):
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
            'quote': [new_quote.styled_format()]
            })


    @app.route('/quick/quotes', methods=['POST'])
    @requires_auth('post:quotes')
    def create_quotes_easy(jwt):
        '''
        Add a new quote to the repository in easy way
        '''
        body = request.get_json()

        text = body['text']
        topic = body['topic']

        party_search = body['party']
        selection = Party.search_by_name(party_search)
        if len(selection)!=1:
            abort(400)
        else:
            party_id = selection[0].id

        politician_search = body['politician']
        selection = Politician.search_by_name(politician_search)
        if len(selection)!=1:
            abort(400)
        else:
            politician_id = selection[0].id

        new_quote = Quotes(
                    text=text,
                    topic=topic,
                    party_id=party_id,
                    politician_id=politician_id)

        new_quote.insert()

        return jsonify({
            'success': True,
            'quote': [new_quote.styled_format()]
            })


    @app.route('/quotes/search', methods=['POST'])
    def search_quotes():
        '''Get questions based on match with the search term'''
        body = request.get_json()

        search = body.get('searchTerm', None)

        if search is None:
            abort(400)

        try:
            selection = Quotes.query.filter(Quotes.text.ilike("%{}%".format(search))).all()

            if len(selection) == 0:
                abort(404)

            formated_selection = [q.styled_format() for q in selection]
            current_selection = paginate_list(request, formated_selection)

            return jsonify({
                'success': True,
                'total_quotes': len(selection),
                'current_quotes': current_selection
                })
        except:
            abort(404)


    @app.route('/quotes/<int:quote_id>', methods=['PATCH'])
    @requires_auth('patch:quotes')
    def change_detail(jwt, quote_id):
        '''
        Change details of the quotes in the table
        '''
        try:
            quote = Quotes.query.filter_by(id=quote_id).one_or_none()

    # In case no such quote exists, then inform resource doesn't exist
            if quote is None:
                abort(404)

            body = request.get_json()

            if 'text' in body:
                quote.text = body['text']

            if 'topic' in body:
                quote.topic = body['topic']

            if 'party_id' in body:
                quote.party_id = int(body['party_id'])

            if 'politician_id' in body:
                quote.politician_id = int(body['politician_id'])

            quote.update()

            return jsonify({
                'success': True,
                'quote': [quote.styled_format()]
                })

        except:
            abort(422)


    @app.route('/quotes/<int:quote_id>', methods=['DELETE'])
    @requires_auth('delete:quotes')
    def delete_drink(jwt, quote_id):
        '''
        Delete a quote from the table
        '''
        try:
            quote = Quotes.query.filter_by(id=quote_id).one_or_none()

    # In case no such quotes exists, then inform resource doesn't exist
            if quote is None:
                return abort(404)

            quote.delete()

            return jsonify({
                'success': True,
                'delete': quote_id
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
# ----------------------------------------------
    return app
