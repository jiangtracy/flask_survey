from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
# from surveys import satisfaction_survey as survey
from surveys import surveys


app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)
RESPONSE_KEY = 'responses'


@app.route('/')
def display_survey_select():
    """ Renders the page to select the survey to take """
    print(surveys)
    # breakpoint()
    # survey_code, survey_info = surveys.items()
    return render_template('survey_select.html', surveys=surveys)


@app.route('/start')
def display_survey_info():
    """Renders the survey start root page"""
    session[RESPONSE_KEY] = []

    survey_code = request.args.get('survey-select')
    survey = surveys.get(survey_code)

    return render_template('survey_start.html',
                           survey=survey, survey_code=survey_code)


@app.route('/<survey_code>/questions/<int:question_idx>',
           methods=['GET', 'POST'])
def display_survey_question(survey_code, question_idx):
    """Renders the next survey question"""

    survey = surveys.get(survey_code)

    # prevent user from answering the quesitions if 
    # survey is already completed.
    if len(session[RESPONSE_KEY]) == len(survey.questions):
        flash("The survey has already been completed!")
        return redirect(f'/{survey_code}/complete')

    # protect questions and redirect user to the correct 
    # questions if necessary
    if question_idx != len(session[RESPONSE_KEY]):
        question_idx = len(session[RESPONSE_KEY])
        flash("Please complete the survey in sequence.")
        return redirect(f'/{survey_code}/questions/{question_idx}')

    question = survey.questions[question_idx]
    return render_template('question.html',
                           survey_code=survey_code, question=question)


@app.route('/<survey_code>/answer', methods=['POST'])
def save_answer(survey_code):
    """Saves the survey question answer and either redirects
    to next page or renders the completion page"""
    survey = surveys.get(survey_code)
    answer = request.form.get('answer')

    responses = session[RESPONSE_KEY]
    responses.append(answer)
    session[RESPONSE_KEY] = responses

    next_idx = len(session[RESPONSE_KEY])

    if next_idx < len(survey.questions):
        return redirect(f'/{survey_code}/questions/{next_idx}')
    else:
        return redirect(f'/{survey_code}/complete')


@app.route('/<survey_code>/complete')
def display_completion(survey_code):
    """ Renders the Completion page when survey is completed """

    return render_template('completion.html')
