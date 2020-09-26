from flask import Flask, render_template, request, redirect, url_for
import os
import json
import random

app = Flask(__name__)

database = {}
with open('food.json') as fp:
    database = json.load(fp)


@app.route('/foods')
def show_food():
    return render_template('food.template.html', all_food=database)


@app.route('/foods/add')
def show_add_food():
    return render_template('create_food.template.html')


@app.route('/foods/add', methods=["POST"])
def process_add_food():
    print(request.form)
    database.append({
        'id': random.randint(1000, 9999),
        'name': request.form.get('food_name'),
        'calories': request.form.get('calories'),
        'date': request.form.get('date'),
        'meal': request.form.get('meal')
    })

    with open('food.json', 'w') as fp:
        json.dump(database, fp)

    return redirect(url_for('show_food'))


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
