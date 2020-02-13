import os
import unittest
import json
import random
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Quotes, Party, Politician


class QuoteTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "quote_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()


    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_quotes(self):
        res = self.client().get('/quotes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_paginated_quotes(self):
        res = self.client().get('/quotes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['total_quotes'])

    def test_parties(self):
        res = self.client().get('/parties')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['total_parties'])

    def test_politician(self):
        res = self.client().get('/politicians')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['total_politicians'])

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/quotes?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_question(self):
        new_question = Question(
                                question = "What is the capital of India",
                                answer = "New Delhi",
                                difficulty = 3,
                                category = "5"
                                )
        new_question.insert()
        res = self.client().delete('/questions/'+str(new_question.id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], new_question.id)

    def test_delete_question_fail(self):
        res = self.client().delete('/questions/10000')
        #Large question_id, which doesn't exist
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_new_question(self):
        post_data = {
                    "question": "What's the best achaar in the world?",
                    "answer": "aam ka achaar",
                    "difficulty": 2,
                    "category": "5"
                    }

        res = self.client().post('/questions', json=post_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question_id'])

    def test_new_question_fail(self):
        post_data = {
                    "question": "",
                    "answer": "",
                    "difficulty": 2,
                    "category": "5"
                    }

        res = self.client().post('/questions', json=post_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_search_question(self):
        new_question = Question(
                                question = "What is the capital of Assam",
                                answer = "Itanagar",
                                difficulty = 3,
                                category = "3"
                                )
        new_question.insert()
        post_data = {
                    "searchTerm": "What",
                    }

        res = self.client().post('/questions/search', json=post_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_search_question_fail(self):
        post_data = {"a": "b"}

        res = self.client().post('/questions/search', json=post_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_category_wise_question(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_category_wise_question_fail(self):
        #testing for category id that doesn't exist
        res = self.client().get('/categories/8/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_start_quiz(self):
        question_repo = [question.format() for question in Question.query.all()]
        question = random.choice(question_repo)

        previous_questions = [question["id"],]
        quiz_category = question["category"]

        post_data = {
                    "previous_questions": previous_questions,
                    "quiz_category": {"id": quiz_category}
                    }

        res = self.client().post('/quizzes', json=post_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])

    def test_start_quiz_fail(self):
        question_repo = [question.format() for question in Question.query.all()]
        question = random.choice(question_repo)

        previous_questions = [question["id"],]
        quiz_category = question["category"]

        post_data = {
                    "quiz_category": {"id": quiz_category}
                    }
        #Testing with invlalid json

        res = self.client().post('/quizzes', json=post_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertTrue(data['message'])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
