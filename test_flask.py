import os
import unittest
import json
import random
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, db, Quotes, Party, Politician

# -------------------------------------------------------------------
# Set Up
# -------------------------------------------------------------------

app = create_app()
#Create an instance of app imported from app

# -------------------------------------------------------------------
# Auth Token for Testing
# -------------------------------------------------------------------

admin_auth_token = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1rUkJNekUwUVRCRlFqYzNPRGt3TjBJd1JUWkJNa1pCUlVFNFJUTXhNVFZFTXpKRE1VSTRRdyJ9.eyJpc3MiOiJodHRwczovL3h1cGxlci5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWUzNzNlOTVlMjc1ZWUwZTc5NzlmMmIxIiwiYXVkIjoicXVvdGUiLCJpYXQiOjE1ODE3MTIyODAsImV4cCI6MTU4MTcxOTQ4MCwiYXpwIjoiZTI1WkVRQ2UwZHJ2ZXlNU3N2OTZvanFFS0w0RzJRNmYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpxdW90ZXMiLCJwYXRjaDpxdW90ZXMiLCJwb3N0OnF1b3RlcyJdfQ.Xaqet37JqvZOo57N8dolCTrz0jXxYWIdqPLWZjn9mxvr3n6NoWZaJfDGj9Gx8Q87Zg_J-HjZPwsOl2Ai9MHt2Tci1eBAYSlZE2buFtOC60g5gDyTVQQ-9-36wF64G7VCWlThmUcw4-1utEo_WQo0kYhZ9xNCdK2-cZ0C187AsyOWe9ZklsNtKMgNUvTmwpKIoUJer5bS_tUwHqb5KXmSS9qtjWKChf89AWIDsbl3k-3IMeT0Fjedo64Wven6HhwQ87J5JjfREJ9OihhIA4DFzeJvHSz6a4iIZgqiQQEOFgDuF-_AOI6Q5BcguTTS5mK_SPNGSqMayKj1EcjbD-56eg'

creator_auth_token = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1rUkJNekUwUVRCRlFqYzNPRGt3TjBJd1JUWkJNa1pCUlVFNFJUTXhNVFZFTXpKRE1VSTRRdyJ9.eyJpc3MiOiJodHRwczovL3h1cGxlci5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWUzNGEyMmM3MzY3ZGEwZTc3OGE4MjZiIiwiYXVkIjoicXVvdGUiLCJpYXQiOjE1ODE3MTMyMDQsImV4cCI6MTU4MTcyMDQwNCwiYXpwIjoiZTI1WkVRQ2UwZHJ2ZXlNU3N2OTZvanFFS0w0RzJRNmYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbInBvc3Q6cXVvdGVzIl19.tuuMmjjzt9h19sYocIsUSPNwqn3bvHR3szepOzssYlsAAWWUIlbVIFEQoXLTaxxY6UFEqtELKTwHXeM8kkv7Q9BykyQKLTdevp-NXjG-eYjFhMBOxqzytrSKiVV5Dddw5y8M-MW6M94IXwm19rpx43Z-LdoOby3Zv0ieanaAQxdtnMLMn-8Fmrq0ZiqqDW8nB98kMPo1gWC-8ywvN2MI3zHKqir2njf55oW5_w0LPzP2mJoBG8-239zveSBZMit5x9Zp2sSrT128SqfnDqlQ2sPM877yjVItHoCgRu0Z5tV4_MocWNMhMoo3o5HRH4tHNykVElvmy4MgxbnNpuC5-A'

# -------------------------------------------------------------------
# General Test
# -------------------------------------------------------------------
class QuoteTestCase(unittest.TestCase):
    """This class represents the Quote test case"""

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
# New database created for testing purupose
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ajitesh@localhost:5432/quote_test'
        self.client= app.test_client

# Clear the database and create tables again at start of each test
        db.drop_all()
        db.create_all()

        new_party = Party(name="INC", party_symbol="web_link")
        new_party.insert()

        new_politician = Politician(
                                    name="Rahul Gandhi",
                                    image_link="link",
                                    famous_posts="President of Congress",
                                    party_id=1)
        new_politician.insert()

        new_quote = Quotes(
                            text="Last night I wake up in morning",
                            topic="UP Election",
                            party_id=1,
                            politician_id=1)
        new_quote.insert()

# -------------------------------------------------------------------
# Tear Down
# -------------------------------------------------------------------

    def tearDown(self):
        """Executed after reach test"""
        pass

# -------------------------------------------------------------------
# Tests
# -------------------------------------------------------------------

    def test_get_quotes(self):
        res = self.client().get('/quotes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_paginated_quotes(self):
        res = self.client().get('/quotes?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['total_quotes'])

    def paginated_quotes_fail(self):
        res = self.client().get('/quotes?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_parties(self):
        res = self.client().get('/parties')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def paginated_parties_fail(self):
        res = self.client().get('/parties?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_politician(self):
        res = self.client().get('/politicians')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['total_politicians'])

    def test_delete_quote_fail(self):
        new_quote = Quotes(
                            text="Aisa machine lagunga idhar aloo daalo udhar sona niklega",
                            topic="UP Election",
                            party_id=1,
                            politician_id=1)
        new_quote.insert()

        res = self.client().delete('/quotes/'+str(new_quote.id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_delete_quote(self):
        new_quote = Quotes(
                            text="Aisa machine idhar aloo daalo udhar sona niklega",
                            topic="UP Election",
                            party_id=1,
                            politician_id=1)
        new_quote.insert()

        res = self.client().delete('/quotes/'+str(new_quote.id), headers={'Authorization': admin_auth_token})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_new_quotes_access_fail(self):
        post_data = {
                    "text": "Aisa idhar aloo daalo udhar sona niklega",
                    "topic": "UP Election",
                    "party_id": 1,
                    "politician_id": 1
                    }

        res = self.client().post('/quotes', json=post_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_new_quotes(self):
        post_data = {
                    "text": "Aisa idhar aloo daalo udhar sona niklega",
                    "topic": "UP Election",
                    "party_id": 1,
                    "politician_id": 1
                    }

        res = self.client().post('/quotes', json=post_data, headers={'Authorization': creator_auth_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_search_quotes(self):
        new_quote = Quotes(
                            text="Dummy question is just for search",
                            topic="UP Election",
                            party_id=1,
                            politician_id=1)
        new_quote.insert()

        post_data = {
                    "searchTerm": "search",
                    }

        res = self.client().post('/quotes/search', json=post_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_search_quotes_fail(self):
        post_data = {"a": "b"}

        res = self.client().post('/quotes/search', json=post_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_edit_quotes(self):
        patch_data = {
                    "text": "changed text",
                    "topic": "UP Election",
                    "party_id": 1,
                    "politician_id": 1
                    }

        res = self.client().patch('/quotes/1', json=patch_data, headers={'Authorization': admin_auth_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_edit_quotes_access_fail(self):
        patch_data = {
                    "text": "changed text",
                    "topic": "UP Election",
                    "party_id": 1,
                    "politician_id": 1
                    }

        res = self.client().patch('/quotes/1', json=patch_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_edit_quotes_fail(self):
        patch_data = {
                    "a": "changed text",
                    "b": "UP Election",
                    "c": 1,
                    "d": 1
                    }

        res = self.client().patch('/quotes/100', json=patch_data, headers={'Authorization': admin_auth_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
