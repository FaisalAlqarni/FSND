import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
  """This class represents the trivia test case"""

  def setUp(self):
    """Define test variables and initialize app."""
    self.app = create_app()
    self.client = self.app.test_client
    self.database_name = "trivia_test"
    self.database_path = "postgres://{}:{}@{}/{}".format('postgres', '1111', 'localhost:5432', self.database_name)
    setup_db(self.app, self.database_path)
    self.new_question = {
      'question': 'what is the capital of saudi arabia?',
      'answer': 'Riyadh',
      'difficulty': 1,
      'category': '3'
    }
    self.new_quiz = {
      'previous_questions': [], 
      'quiz_category': {'type': 'Geography', 'id': 3}}

    
    # binds the app to the current context
    with self.app.app_context():
        self.db = SQLAlchemy()
        self.db.init_app(self.app)
        # create all tables
        self.db.create_all()
  
  def tearDown(self):
    """Executed after reach test"""
    pass

  """
  TODO
  Write at least one test for each test for successful operation and for expected errors.
  """
  # Success
  def test_get_questions(self):
    """Test getting questions"""
    response = self.client().get('/questions')
    data = json.loads(response.data)
    
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertTrue(data['total_questions'])
    self.assertTrue(len(data['questions']))

  def test_delete_question(self):
    """Test delete question"""

    question = Question(question=self.new_question['question'], 
                        answer=self.new_question['answer'],
                        category=self.new_question['category'], 
                        difficulty=self.new_question['difficulty'])
    question.insert()
    old_total = Question.query.all()
    response = self.client().delete('/questions/{}'.format(int(question.id)))
    data = json.loads(response.data)
    new_total = Question.query.all()
    
    total = old_total - new_total
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data, True)
    self.assertEqual(data['deleted'], question.id)
    self.assertEqual(data['total'], new_total)
    self.assertEqual(total, 0)

  def test_create_question(self):
    """Test create question"""

    questions_before = Question.query.all()
    response = self.client().post('/questions', json=self.new_question)
    data = json.loads(response.data)
    questions_after = Question.query.all()
    
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertTrue(len(questions_after) == len(questions_before) + 1)

  def test_search_questions(self):
    """Test search questions"""

    response = self.client().post('/questions', json={'searchTerm': 'Saudi'})

    data = json.loads(response.data)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertEqual(data['total_questions'], 1)

  def test_get_questions_on_category(self):
    """Test get questions on category"""

    response = self.client().get('/categories/0/questions')
    data = json.loads(response.data)

    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertEqual(len(data['questions']), 3)

  def test_get_quiz_with_random_questions(self):
    """Test get quiz"""

    response = self.client().post('/quizzes', json=self.new_quiz)
    data = json.loads(response.data)

    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['success'], True)
      
  # Error
  def test_402_get_questions(self):
    """Tests question pagination exceeding allowed pages"""

    response = self.client().get('/questions?page=9999')
    data = json.loads(response.data)

    self.assertEqual(response.status_code, 402)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'resource not found')

  def test_404_delete_question(self):
    """Test delete non-existed question"""

    response = self.client().get('/questions/9999')
    data = json.loads(response.data)

    self.assertEqual(response.status_code, 404)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'resource not found')

  def test_422_create_question(self):
    """Test create question with empty data"""
    
    response = self.client().post('/questions', json={})
    data = json.loads(response.data)

    self.assertEqual(response.status_code, 422)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'unprocessable')

  def test_422_search_questions(self):
    """Test searching non-exist question/s"""

    response = self.client().post('/questions', json={'searchTerm': 'aaaaaaaaaaaaa'})
    data = json.loads(response.data)

    self.assertEqual(response.status_code, 422)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'unprocessable')

  def test_404_get_questions_on_category(self):
    """Tests getting no questions in category"""

    response = self.client().get('/categories/9999/questions')
    data = json.loads(response.data)

    self.assertEqual(response.status_code, 404)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'resource not found')

  def test_422_get_quiz_with_random_questions(self):
    """Test start quiz without passing quiz_category or previous_questions"""

    response = self.client().post('/quizzes', json={})
    data = json.loads(response.data)

    self.assertEqual(response.status_code, 422)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'unprocessable')


# Make the tests conveniently executable
if __name__ == "__main__":
  unittest.main()