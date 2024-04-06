from flask import Flask, render_template, request, url_for, redirect
import re, os
import csv
from functions import get_survey_response, craft_question, export

app = Flask(__name__)


'''
Pseudo-code for final solution
1. Present Question 1 on the screen for user
2. 
    a. Read user's submitted answer and call ChatGPT API to read it
    b. Count 1 question asked on counter module
    c. Output question and question response 'somewhere'
3. ChatGPT API to craft another question based on response of user and internal rules applied
4. Present Question 2 on the screen for user
5. 
    a. Read user's submitted answer and call ChatGPT API to read it
    b. Count 2 questions asked on counter module
    c. Output question and question response 'somewhere'
6. ChatGPT API to craft another question based on response of user and internal rules applied
7. Present Question 3 on the screen for user
8. 
    a. Read user's submitted answer and call ChatGPT API to read it
    b. Count 3 questions asked on counter module
    c. Output question and question response 'somewhere'
'''

'''
More thoughts
1. Use Flask to delineate survey from survey parameters
2. Load up survey within JavaScript page, call ChatGPT API within JavaScript to dynamically run the survey on the page
3. Load survey results to other Flask page
'''

responses = []
questions = [
        "How often do you read/watch educational things online like articles, videos, or social media posts?",
        "What makes you want to click on something you see online?",
        "If something you're reading or watching online lets you interact with it (like taking quizzes, voting in polls, or moving things around), are you more likely to keep reading or watching?"
]

@app.route("/")
def index():

    return render_template("index.html")


@app.route("/1", methods=('GET', 'POST'))
def question_one():
    if request.method == 'POST':
        responses.append(get_survey_response())

        return redirect("/2")
    else:
        question_number = 1
        question_text = questions[0]

        return render_template("question-layout.html", question_number=question_number, question_text=question_text)


@app.route("/2", methods=('GET', 'POST'))
def question_two():
    if request.method == 'POST':
        responses.append(get_survey_response())
        
        return redirect("/3")
    
    else:
        question_number = 2
        questions[1] = craft_question(questions, responses)
        question_text = questions[1]

        return render_template("question-layout.html", question_number=question_number, question_text=question_text)


@app.route("/3", methods=('GET', 'POST'))
def question_three():
    if request.method == 'POST':
        responses.append(get_survey_response())
        
        return redirect("/")
    
    else:
        question_number = 3
        questions[2] = craft_question(questions, responses)
        question_text = questions[2]

        return render_template("question-layout.html", question_number=question_number, question_text=question_text)
    

@app.route("/responses", methods=('GET', 'POST'))
def responses_page():
    if request.method == 'POST':
        export(questions, responses)
        
        return redirect("/")
    
    else:

        return render_template("responses.html", questions=questions, responses=responses)