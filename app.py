from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

# session['responses'] = []

@app.route('/')
def display_survey_info():
    """Renders the survey start root page"""
    session['responses'] = []
    return render_template('survey_start.html', survey=survey)


@app.route('/questions/<int:question_idx>', methods=['GET', 'POST'])
def display_survey_question(question_idx):
    """Renders the next survey question"""

    #prevent user from answering the quesitions if survey is already completed.

    if len(session['responses']) == len(survey.questions):
        return redirect('/complete')

    # protect questions and redirect user to the correct questions if necessary
    if question_idx != len(session['responses']):
        question_idx = len(session['responses'])
        return redirect(f'/questions/{question_idx}')
    

    question = survey.questions[question_idx]
    return render_template('question.html', question=question)


@app.route('/answer', methods=['POST'])
def save_answer():
    """Saves the survey question answer and either redirects
    to next page or renders the completion page"""

    answer = request.form.get('answer')
    print(answer)

    responses = session['responses']
    responses.append(answer)
    session['responses'] = responses

    print(session['responses'])

    next_idx = len(session['responses'])

    if next_idx < len(survey.questions):
        return redirect(f'/questions/{next_idx}')
    else:
        return redirect('/complete')


@app.route('/complete')
def display_completion():
    """ Renders the Completion page when survey is completed """

    return render_template('completion.html')
