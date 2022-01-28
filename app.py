from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

RESPONSES_KEY = "responses"

@app.get('/')
def show_survey():
    """Shows the start survey page"""

    session['responses'] = []

    return render_template(
        "survey_start.html",
        title=survey.title,
        instructions=survey.instructions
    )

@app.get("/question/<int:question_number>")
def show_question(question_number):
    """Show page with the next question"""

    if len(session[RESPONSES_KEY]) == len(survey.questions):
        flash("You have answered all the questions")
        return redirect("/completion")

    if question_number >= len(survey.questions) or question_number > len(session[RESPONSES_KEY]):
        question_number = len(session[RESPONSES_KEY])
        flash("Stop trying to skip my questions")
        return redirect(f"/question/{question_number}")

    question_number = len(session[RESPONSES_KEY])

    question = survey.questions[question_number]

    return render_template(
        "question.html",
        question=question
        # question_number = question_number + 1
    )

 
@app.post("/answer")
def collect_answers():
    """Adds selected answers to global response variable list
    Redirects to next question, if there are no more questions,
    redirects to thank you page.
    """
    answer = request.form["answer"]
    responses = session[RESPONSES_KEY]
    responses.append(answer)
    session[RESPONSES_KEY] = responses

    if len(responses) == len(survey.questions):
        return redirect("/completion")
    else:
        # question_number = request.form["question_number"]
        question_number = len(responses)
        return redirect(f"/question/{question_number}")


@app.get("/completion")
def finish_survey():
    """Shows thank you message for completing the survey"""

    return render_template("completion.html")

"""
    can't directly append data to session[RESPONSES_KEY], as the list inside can't
    update automatically, so we need to rebind to it, like line 56-58

"""  