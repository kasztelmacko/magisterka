from flask import Flask, render_template, request, session, redirect, url_for, render_template_string
from database import insert_person, select_items
import datetime
from dotenv import load_dotenv
import os
import jwt

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

SECRET_JWT = os.getenv('SECRET_JWT')

@app.route('/')
def home():
    if 'submitted' in session and session['submitted']:
        return redirect(url_for('direct'))
    else:
        return render_template('index.html', submitted=False)

@app.route('/submit_person', methods=['POST'])
def submit_characteristic():
    if request.method == 'POST':
        age = request.form['age']
        gender = request.form['gender']
        education = request.form['education']
        city_size = request.form['city']
        income = request.form['income']
        dining_freq = request.form['dining']

        person_id = insert_person(age, gender, education, city_size, income, dining_freq)

        token = jwt.encode({
            'person_id': person_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=0.5)
        }, SECRET_JWT, algorithm='HS256')

        session['submitted'] = True
        session['token'] = token
        session['person_id'] = person_id

        return redirect(url_for('direct'))
    
@app.route('/direct')
def direct():
    if 'submitted' in session and session['submitted']:
        items = select_items([1,2,3,4,5])
        return render_template('direct.html', token=session.get('token'), person_id=session.get('person_id'), items=items)
    else:
        return redirect(url_for('home'))
    
@app.route('/updated_steps')
def updated_steps():
    step = int(request.args.get('step', 1))
    steps = [
        {'name': 'Information', 'status': 'step-success' if step >= 1 else ''},
        {'name': 'Demographics', 'status': 'step-success' if step >= 2 else ''},
        {'name': 'Direct', 'status': 'step-success' if step >= 3 else ''},
        {'name': 'Indirect', 'status': 'step-success' if step >= 4 else ''},
        {'name': 'End', 'status': 'step-success' if step >= 5 else ''},
    ]
    
    updated_steps_html = '<ul class="steps mt-auto py-10">'
    for step in steps:
        updated_steps_html += f'<li class="step {step["status"]}">{step["name"]}</li>'
    updated_steps_html += '</ul>'
    
    return render_template_string(updated_steps_html)

# for testing purposes
@app.route('/reset', methods=['POST'])
def reset():
    session.pop('submitted', None)
    session.pop('token', None)
    session.pop('person_id', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)