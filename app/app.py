from flask import Flask, render_template, request, session, redirect, url_for
from database import insert_person
import jwt
import datetime
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

SECRET_JWT = os.getenv('SECRET_JWT')

@app.route('/')
def home():
    if 'submitted' in session and session['submitted']:
        return redirect(url_for('kiosk'))
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

        user_id = insert_person(age, gender, education, city_size, income, dining_freq)

        token = jwt.encode({
            'user_id': user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=0.5)
        }, SECRET_JWT, algorithm='HS256')

        session['submitted'] = True
        session['token'] = token
        session['user_id'] = user_id

        return redirect(url_for('kiosk'))
    
@app.route('/kiosk')
def kiosk():
    if 'submitted' in session and session['submitted']:
        return render_template('kiosk.html', token=session['token'], user_id=session['user_id'])
    else:
        return redirect(url_for('home'))

# for testing purposes
@app.route('/reset', methods=['POST'])
def reset():
    session.pop('submitted', None)
    session.pop('token', None)
    session.pop('user_id', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)