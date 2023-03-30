from flask import Flask, render_template, request, redirect, url_for
from jared_bot import jared_bot

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        question = request.form.get('question').strip()
        answer = get_ai_answer(question)
        return render_template('index.html', question=question, answer=answer)
    return render_template('index.html')

def get_ai_answer(question):
    # Replace this function with your actual AI function or API call
    response = jared_bot(question)
    return response[0]

app.run(debug=True)