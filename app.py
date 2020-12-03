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
    """Renders the survey start root page"""

    return render_template('survey_start.html', survey=survey)


@app.route('/questions/<int:question_idx>', methods=['GET', 'POST'])
def display_survey_question(question_idx):
    """Renders the next survey question"""

    question = survey.questions[question_idx]
    return render_template('question.html', question=question)


@app.route('/answer', methods=['POST'])
def save_answer():
    """Saves the survey question answer and either redirects
    to next page or renders the completion page"""
    
    answer = request.form.get('answer')
    responses.append(answer)
    
    next_idx = len(responses)

    if next_idx < len(survey.questions):
        return redirect(f'/questions/{next_idx}')
    else:
        return render_template('completion.html')
