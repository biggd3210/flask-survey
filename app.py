from flask import Flask, request, redirect, render_template, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey, surveys

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

debug = DebugToolbarExtension(app)

responses = []
survey = surveys['satisfaction']
surveyData = surveys['satisfaction'].questions

@app.route('/')
def show_homepage():
    instructions = survey.instructions
    survey_title = survey.title
    return render_template('home.html', instructions=instructions, survey_title=survey_title)

# @app.route('/')
# def show_homepage():
#     # survey_list = []
#     # for survey_ind in surveys.keys():
#     #     survey_list.append(survey_ind)
#     return render_template("home.html", survey_list=survey_list)

@app.route('/question/<int:qid>')
def show_question(qid):
    """display proper question and choices"""

    if (responses is None):
        #arrived at question page too soon
        return redirect('/')
    
    if (len(responses) == len(survey.questions)):
        #they've completed the survey
        return redirect('/end')
    
    if (len(responses) != qid):
        #accessing questions out of order
        flash("Oops. You accidentally got off course. Let's help.")
        return redirect(f'/question/{len(responses)}')
    
    
    question = surveyData[qid]
    return render_template('question.html', qid=qid, question=question)

    
@app.route('/answer', methods=["POST"])
def post_answer():
    response = request.form['answer']
    responses.append(response)
   
    if (len(responses) == len(surveyData)):
        return redirect('/end')
    else:
        return redirect(f'/question/{len(responses)}')
    
@app.route('/end')
def show_thank_you():
    """survey is finished. Show the thank you page"""
    return render_template('end.html', responses=responses)