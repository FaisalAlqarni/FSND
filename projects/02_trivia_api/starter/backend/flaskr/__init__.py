import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  @app.route('/')
  def index():
    return "Hello !!"
  '''
  @TODOx: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  # inspired from Udacity classroom videos
  CORS(app)
  cors = CORS(app, resources={r"/*": {"origins": "*"}})

  '''
  @TODOx: Use the after_request decorator to set Access-Control-Allow
  '''
  # inspired from Udacity classroom videos
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
      return response
    
  '''
  @TODOx: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def get_categories():
    categories = Category.query.order_by(Category.type).all()
    if len(categories) == 0:
      abort(404)

    try:
      formated_categories = []
      for category in categories:
        formated_categories.append(category.format())

      return jsonify({
        'success': True,
        'categories': formated_categories
      }), 200
    except:
      abort(422)

  '''
  @TODOx: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  def questions_pagination(request, collection):
    page = request.args.get('page', 1, type=int)
    
    start =  (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in collection]
    paginated_questions = questions[start:end]
    
    return paginated_questions

  @app.route('/questions', methods=['GET'])
  def get_questions():
    questions = Question.query.order_by(Question.id).all()
    categories = Category.query.order_by(Category.type).all()

    if len(questions) == 0:
      abort(404)
    
    try:
      paginated_questions = questions_pagination(request, questions)
      formated_categories = []
      for category in categories:
        formated_categories.append(category.format())
        
      return jsonify({
        'success': True,
        'questions': paginated_questions, 
        'number of total questions': len(questions),
        'categories': formated_categories,
        'current_category': None,
      }), 200
    except:
      abort(422)

  '''
  @TODOx: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    question = Question.query.filter(Question.id == question_id).one_or_none()

    if question is None:
      abort(404)
      
    try:
      question.delete()
      questions = Question.query.all()

      return jsonify({
        'success': True,
        'deleted': question_id,
        'total': len(questions),
      }), 200
      
    except:
      abort(422)

  '''
  @TODOx: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def create_question():
    body = request.get_json()
    # the attributes are from FormView.js
    question = body.get('question', None)
    answer = body.get('answer', None)
    difficulty = body.get('difficulty', None)
    category = body.get('category', None)
    searchTerm = body.get('searchTerm', None)

    try:
      if searchTerm:
        questions_collection = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(searchTerm)))
        paginated_questions = questions_pagination(request, questions_collection)
        
        answers_collection = Question.query.order_by(Question.id).filter(Question.answer.ilike('%{}%'.format(searchTerm)))
        paginated_answers = questions_pagination(request, answers_collection)

        if (len(questions_collection.all()) == 0) and (len(answers_collection.all()) == 0):
          abort(404)
          
        return jsonify({
          'success': True,
          'by_questions': paginated_questions,
          'total_questions': len(questions_collection.all()),
          'by_answers': paginated_answers,
          'total_answers': len(answers_collection.all()),
        }), 200
        
      else:
        if (question is None) or (answer is None) or (difficulty is None) or (category is None):
          abort(400)
          
        created_question = Question(
          question=question,
          answer=answer,
          difficulty=difficulty,
          category=category)

        created_question.insert()
        questions = Question.query.all()

        return jsonify({
          'success': True,
          'created': created_question.id,
          'total': len(questions),
        }), 200
      
    except:
      abort(422)

  '''
  @TODOx: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  
  # i created a serchterm in teh previous endpoint because i am not sure if you want to extend the leangth of this route
  @app.route('/questions/search', methods=['POST'])
  def search_question():
    body = request.get_json()
    # the attributes are from FormView.js
    searchTerm = body.get('searchTerm', None)

    if searchTerm is None:
      abort(400)
    questions_collection = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(searchTerm)))
    answers_collection = Question.query.order_by(Question.id).filter(Question.answer.ilike('%{}%'.format(searchTerm)))

    if (len(questions_collection.all()) == 0) and (len(answers_collection.all()) == 0):
      abort(404)
      
    try:  
      paginated_questions = questions_pagination(request, questions_collection)
      paginated_answers = questions_pagination(request, answers_collection)
          
      return jsonify({
        'success': True,
        'by_questions': paginated_questions,
        'total_questions': len(questions_collection.all()),
        'by_answers': paginated_answers,
        'total_answers': len(answers_collection.all()),
      }), 200  
    except:
      abort(422)

  '''
  @TODOx: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/category/<int:category_id>/questions')
  def get_questions_on_category(category_id):
    questions = Question.query.join(Category, Question.category == Category.id).filter(Category.id == category_id).order_by(Question.id).all()
    
    if len(questions) == 0:
      abort(404)
      
    try:
      formated_questions = []
      for question in questions:
        formated_questions.append(question.format())


      return jsonify({
        'success': True,
        'category': category_id,
        'questions': formated_questions,
        'total': len(questions),
      }), 200
    
    except:
      abort(422)

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def get_quiz_with_random_questions():
    body = request.get_json()
    # from QuizView.js
    previous_questions = body.get('previous_questions')
    quiz_category = body.get('quiz_category')

    if quiz_category is None or previous_questions is None:
      abort(400)

    try:        
      if quiz_category['id'] == 0:
        questions = Question.query.all()
      else:
        questions = Question.query.join(Category, Question.category == Category.id).filter(Category.id == quiz_category['id']).all()

      quiz_questions = [question.format() for question in questions if question.id not in previous_questions]

      if len(quiz_questions) == 0:
          next_question = None
      else:
          next_question = random.choice(quiz_questions)

      return jsonify({
          'success': True,
          'question': next_question
      }), 200

    except:
      abort(422)
  '''
  @TODOx: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": "bad request"
      }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "resource not found"
      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "unprocessable"
      }), 422

  return app

    