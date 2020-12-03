from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def display_survey_info():
    return render_template('survey_start.html', survey=survey)


@app.route('/questions/<int:question_idx>', methods=['POST'])
def display_survey_question(question_idx):
    question = survey.questions[question_idx]
    return render_template('question.html', question=question)