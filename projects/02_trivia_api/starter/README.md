# Full Stack API Final Project

## Full Stack Trivia

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a  webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out. 

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others. 

## Tasks

There are `TODO` comments throughout project. Start by reading the READMEs in:

1. [`./frontend/`](./frontend/README.md)
2. [`./backend/`](./backend/README.md)

We recommend following the instructions in those files in order. This order will look familiar from our prior work in the course.

## Starting and Submitting the Project

[Fork](https://help.github.com/en/articles/fork-a-repo) the [project repository]() and [Clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository before submitting the link to your repository in the Classroom. 

## About the Stack

We started the full stack application for you. It is desiged with some key functional areas:

### Backend

The `./backend` directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in app.py to define your endpoints and can reference models.py for DB and SQLAlchemy setup. 

### Frontend

The `./frontend` directory contains a complete React frontend to consume the data from the Flask server. You will need to update the endpoints after you define them in the backend. Those areas are marked with TODO and can be searched for expediency. 

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API. 

[View the README.md within ./frontend for more details.](./frontend/README.md)
## API Reference
### Before we start
we need first to set up the environment and dependencies.

1- setting up the Database:
* go to backend folder
* open the terminal there
* run this command to import the db to our machine `psql -U your_db_username -d existed_db_name -f trivia.psql`

2- setting up the backend:
* go to backend folder
* open the terminal there
* run this command `pip install -r requirements.txt` to install depentncies
* run this commands to run the backend server
    `export FLASK_APP=flaskr
    export FLASK_ENV=development
    flask run`

3- setting up the frontend:
* go to frontend folder
* open the terminal there
* run this command `npm install` to install depentncies
* run this command to run the frontend server `npm start`

### Testing
In order to run tests navigate to the backend folder and run the following commands:

`dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py`

The first time you run the tests, omit the dropdb command.
All tests are kept in that file and should be maintained as updates are made to app functionality.

### Basics

* Base URL: `http://127.0.0.1:5000/`
and there is no auth for this APIs

### Handling erros

Errors are returned as JSON like:

    {
        "success": False,
        "error": 404,
        "message": "resource not found"
    }

and there are three error handelrs:-
* 400: bad request
* 404: resource not found
* 422: unprocessable

### Endpoints

#### GET `/categories`
* This endpoint is to list categories
* CURL: `curl http://127.0.0.1:5000/categories`
* Result:

        {
            "categories": {
                "1": "Science", 
                "2": "Art", 
                "3": "Geography", 
                "4": "History", 
                "5": "Entertainment", 
                "6": "Sports"
            }, 
            "success": true
        }


#### GET `/questions`

* This endpoint is to list questions in pages, each page contain 10 questions.
it return also a list of categories and number of questions
* Params:
    * page=int: to specify the page you want to go to. e.g. `curl http://127.0.0.1:5000/questions?page=23`
* CURL: `curl http://127.0.0.1:5000/questions`
* Result:

        {
            "categories": {
                "1": "Science",
                "2": "Art",
                "3": "Geography",
                "4": "History",
                "5": "Entertainment",
                "6": "Sports"
            },
            "questions": [
                {
                    "answer": "Apollo 13",
                    "category": 5,
                    "difficulty": 4,
                    "id": 2,
                    "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
                },
                {
                    "answer": "Tom Cruise",
                    "category": 5,
                    "difficulty": 4,
                    "id": 4,
                    "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
                },
                {
                    "answer": "Maya Angelou",
                    "category": 4,
                    "difficulty": 2,
                    "id": 5,
                    "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
                },
                {
                    "answer": "Edward Scissorhands",
                    "category": 5,
                    "difficulty": 3,
                    "id": 6,
                    "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
                },
                {
                    "answer": "Muhammad Ali",
                    "category": 4,
                    "difficulty": 1,
                    "id": 9,
                    "question": "What boxer's original name is Cassius Clay?"
                },
                {
                    "answer": "Brazil",
                    "category": 6,
                    "difficulty": 3,
                    "id": 10,
                    "question": "Which is the only team to play in every soccer World Cup tournament?"
                },
                {
                    "answer": "Uruguay",
                    "category": 6,
                    "difficulty": 4,
                    "id": 11,
                    "question": "Which country won the first ever soccer World Cup in 1930?"
                },
                {
                    "answer": "George Washington Carver",
                    "category": 4,
                    "difficulty": 2,
                    "id": 12,
                    "question": "Who invented Peanut Butter?"
                },
                {
                    "answer": "Lake Victoria",
                    "category": 3,
                    "difficulty": 2,
                    "id": 13,
                    "question": "What is the largest lake in Africa?"
                },
                {
                    "answer": "The Palace of Versailles",
                    "category": 3,
                    "difficulty": 3,
                    "id": 14,
                    "question": "In which royal palace would you find the Hall of Mirrors?"
                }
            ],
            "success": true,
            "total_questions": 25
        }

#### DELETE `/questions/\<int:question_id\>`

* This endpoint is to delete a question by its ID.
* Params:
    * int:question_id: to specify the question id you want to delete. e.g. `curl http://127.0.0.1:5000/questions/98546496`
* CURL: `curl http://127.0.0.1:5000/questions/25`
* Result:

        {
            "deleted": 25,
            "success": true,
            "total": 24
        }
        
#### POST /questions

* This endpoint have two functions, create a new question, or search for a question.
* <strong>Case Search</strong>

    * Params:
        * SearchTerm : pass the search term using JSON to search.
        like:
        
                {   
                    "searchTerm": "to"
                }
   
    * CURL: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "to"}'`
    * Result:
    
            {
                "questions": [
                    {
                        "answer": "Apollo 13",
                        "category": 5,
                        "difficulty": 4,
                        "id": 2,
                        "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
                    },
                    {
                        "answer": "Tom Cruise",
                        "category": 5,
                        "difficulty": 4,
                        "id": 4,
                        "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
                    },
                    {
                        "answer": "Maya Angelou",
                        "category": 4,
                        "difficulty": 2,
                        "id": 5,
                        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
                    },
                    {
                        "answer": "Edward Scissorhands",
                        "category": 5,
                        "difficulty": 3,
                        "id": 6,
                        "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
                    },
                    {
                        "answer": "Brazil",
                        "category": 6,
                        "difficulty": 3,
                        "id": 10,
                        "question": "Which is the only team to play in every soccer World Cup tournament?"
                    },
                    {
                        "answer": "Escher",
                        "category": 2,
                        "difficulty": 1,
                        "id": 16,
                        "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
                    }
                ],
                "success": true,
                "total_questions": 6
            }

* <strong>Case Create</strong>

    * Params:
        * question : the question you want to ask.
        * answer : the answer of the question.
        * category : the category id.
        * difficulty : the difficulty in int.
        
        all the params are passed on JSON like:
        
                {
                        "question": "what is the capital of saudi arabia?",
                        "answer": "Riyadh",
                        "category": 3,
                        "difficulty": 1
                }
        
    * CURL: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{
                "question": 'what is the capital of saudi arabia?',
                "answer": 'Riyadh',
                "category": 3,
                "difficulty": 1
                }'`
    * Result: r
    
            {
                "created": 36,
                "success": true,
                "total": 25
            }
        
<strong>Note: if searchTerm is present then IT WILL OVERWRITE and you can't create a question</strong>


#### GET `/categories/\<int:category_id\>/questions`
* This endpoint is to get the quiestion of the category given the category id in pagination.
* Params:
    * category_id: the id of the category
* CURL: `curl http://127.0.0.1:5000/categories/3/questions`
* Result:

        {
            "questions": [
                {
                    "answer": "Lake Victoria",
                    "category": 3,
                    "difficulty": 2,
                    "id": 13,
                    "question": "What is the largest lake in Africa?"
                },
                {
                    "answer": "The Palace of Versailles",
                    "category": 3,
                    "difficulty": 3,
                    "id": 14,
                    "question": "In which royal palace would you find the Hall of Mirrors?"
                },
                {
                    "answer": "Agra",
                    "category": 3,
                    "difficulty": 2,
                    "id": 15,
                    "question": "The Taj Mahal is located in which Indian city?"
                },
                {
                    "answer": "Riyadh",
                    "category": 3,
                    "difficulty": 1,
                    "id": 37,
                    "question": "what is the capital of saudi arabia?"
                }
            ],
            "success": true,
            "total_questions": 4
        }

#### POST /quizzes
* This endpoint will allow the user to play the quiz game, the requst params are category and previous questions.
* Params:
    * previous_questions: ids of the previous questions
    * quiz_category: the category type and id for the questions
    like:

        {
            "previous_questions": [13, 14],
            "quiz_category": {"type": "Geography", "id": "3"}
        }
        
* CURL: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [13, 14],
                                            "quiz_category": {"type": "Geography", "id": "3"}}'`
* Result:

        {
            "question": {
                "answer": "Riyadh", 
                "category": 3, 
                "difficulty": 1, 
                "id": 37, 
                "question": "what is the capital of saudi arabia?"
            }, 
            "success": true
        }
