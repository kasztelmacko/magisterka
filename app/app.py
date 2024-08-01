import datetime
import json
import os

from dotenv import load_dotenv
from flask import Flask, render_template, request, session, redirect, url_for, render_template_string, jsonify
import jwt

from database import insert_person, select_items, insert_direct_survey, insert_indirect_survey, select_types, insert_discrete_order
from person import Person


load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')
SECRET_JWT = os.getenv('SECRET_JWT')

with open('static/data/items.json') as f:
    item_lists = json.load(f)

@app.route('/')
def home():
    with open('static/data/fields.json') as f:
        questions = json.load(f)['questions']
    if 'submitted' in session and session['submitted']:
        return redirect(url_for('direct'))
    else:
        return render_template('index.html', questions=questions, submitted=False)

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
        person = Person(person_id, age, gender, education, city_size, income, dining_freq, None, None, None, None)

        token = jwt.encode({
            'person_id': person_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=0.5)
        }, SECRET_JWT, algorithm='HS256')

        session['submitted'] = True
        session['token'] = token
        session['person_id'] = person_id
        session['person'] = person.__dict__

        return redirect(url_for('direct'))
    
@app.route('/direct')
def direct():
    if 'submitted' in session and session['submitted']:
        items = select_items(item_lists['direct'])
        return render_template('surveys/direct.html', token=session.get('token'), person_id=session.get('person_id'), items=items)
    else:
        return redirect(url_for('home'))
    
@app.route('/submit_direct_survey', methods=['POST'])
def submit_direct_survey():
    if request.method == 'POST':
        person_id = session.get('person_id')
        low_1 = request.form.get('low_1')
        poor_1 = request.form.get('poor_1')
        high_1 = request.form.get('high_1')
        low_2 = request.form.get('low_2')
        poor_2 = request.form.get('poor_2')
        high_2 = request.form.get('high_2')
        low_7 = request.form.get('low_7')
        poor_7 = request.form.get('poor_7')
        high_7 = request.form.get('high_7')
        low_12 = request.form.get('low_12')
        poor_12 = request.form.get('poor_12')
        high_12 = request.form.get('high_12')

        insert_direct_survey(person_id, low_1, poor_1, high_1, low_2, poor_2, high_2, low_7, poor_7, high_7, low_12, poor_12, high_12)

        person_dict = session.get('person')
        if person_dict:
            person = Person(**person_dict)
            person.wtp_burger = poor_1
            person.wtp_double_burger = poor_2
            person.wtp_special_burger = poor_7
            person.wtp_fires = poor_12
            session['person'] = person.__dict__

        return redirect(url_for('indirect'))

    
@app.route('/indirect')
def indirect():
    if 'submitted' in session and session['submitted']:
        items = select_items(item_lists['indirect'])
        return render_template('surveys/indirect.html', token=session.get('token'), person_id=session.get('person_id'), items=items)
    else:
        return redirect(url_for('home'))

@app.route('/submit_indirect_survey', methods=['POST'])
def submit_indirect_survey():
    if request.method == 'POST':
        rect1 = request.form.get('rect1', '')
        rect2 = request.form.get('rect2', '')
        rect3 = request.form.get('rect3', '')
        rect4 = request.form.get('rect4', '')
        rect5 = request.form.get('rect5', '')
        wtp = request.form.get('wtp', '')
        person_id = session.get('person_id')

        insert_indirect_survey(rect1, rect2, rect3, rect4, rect5, wtp, person_id)
        return redirect(url_for('discrete', observation=1))
    

@app.route('/discrete/<int:observation>', methods=['GET'])
def discrete(observation):
    if 'submitted' in session and session['submitted']:
        discrete_key = f'discrete_{observation}'
        item_id_list = item_lists['discrete'].get(discrete_key, "*")
        
        if item_id_list == "*":
            items = select_items()
        else:
            items = select_items(item_id_list)
        types = select_types()

        custom_order = ['burger', 'fries', 'soda', 'bundle']
        types_sorted = sorted(types, key=lambda x: custom_order.index(x['item_type']))

        grouped_items = {}
        for item in items:
            item_type = item['item_type']
            if item_type not in grouped_items:
                grouped_items[item_type] = []
            grouped_items[item_type].append(item)

        grouped_items_sorted = {key: grouped_items[key] for key in custom_order if key in grouped_items}

        person_dict = session.get('person')
        person = Person(**person_dict) if person_dict else None

        for item in items:
            if item['price_type'] == 'burger':
                item['item_base_price'] = int(person.wtp_burger)
            elif item['price_type'] == 'double_burger':
                item['item_base_price'] = int(person.wtp_double_burger)
            elif item['price_type'] == 'special_burger' or item['price_type'] == 'vege_burger':
                item['item_base_price'] = int(person.wtp_special_burger)
            elif item['price_type'] == 'double_special_burger':
                item['item_base_price'] = int(person.wtp_special_burger) + 5
            elif item['price_type'] == 'medium_fries':
                item['item_base_price'] = int(person.wtp_fires)
            elif item['price_type'] == 'big_fries':
                item['item_base_price'] = round(int(person.wtp_fires) * 1.05, 1)

        simplified_items = []
        for item in items:
            simplified_item = {
                'item_name': item['item_name'],
                'item_base_price': item['item_base_price'],
                'item_type': item['item_type'],
                'price_type': item['price_type']
            }
            simplified_items.append(simplified_item)

        items_json = json.dumps(simplified_items)
        session['items_json'] = items_json

        return render_template('surveys/discrete.html', token=session.get('token'), person_id=session.get('person_id'), grouped_items=grouped_items_sorted, types=types_sorted, items_json=items_json, observation=observation)
    else:
        return redirect(url_for('home'))



    
@app.route('/submit_discrete_order', methods=['POST'])
def submit_discrete_order():
    if request.method == 'POST':
        items = []
        for key in request.form:
            if key.startswith('items'):
                item = json.loads(request.form[key])
                items.append(item)

        person_id = session.get('person_id')
        items_json = session.get('items_json')
        observation = int(request.form.get('observation', 1))
        order_status = request.form.get('order_status')
        order_json = {"items": items}
        order_price = sum(item['price'] for item in items)

        session.pop('items_json', None)

        insert_discrete_order(person_id, observation, order_json, order_price, items_json, order_status)

        if observation < item_lists["discrete"]["number_of_discrete_choices"]:
            observation += 1
            return redirect(url_for('discrete', observation=observation))
        else:
            return render_template('end.html', token=session.get('token'), person_id=session.get('person_id'))


    
@app.route('/updated_steps')
def updated_steps():
    step = int(request.args.get('step', 1))
    steps = [
        {'name': 'Information', 'status': 'step-success' if step >= 1 else ''},
        {'name': 'Demographics', 'status': 'step-success' if step >= 2 else ''},
        {'name': 'Direct', 'status': 'step-success' if step >= 3 else ''},
        {'name': 'Indirect', 'status': 'step-success' if step >= 4 else ''},
        {'name': 'Discrete', 'status': 'step-success' if step >= 5 else ''},
        {'name': 'End', 'status': 'step-success' if step >= 6 else ''},
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