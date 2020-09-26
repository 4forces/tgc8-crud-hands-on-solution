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


@app.route('/foods/<int:food_id>/edit')
def show_edit_food(food_id):

    # 1. find the food record to edit
    food_to_edit = None
    for each_food in database:
        if each_food["id"] == food_id:
            food_to_edit = each_food
            break

    if food_to_edit:
        return render_template('edit_food.template.html', food=food_to_edit)
    else:
        return f"The food record with the id of {food_id} is not found!"


@app.route('/foods/<int:food_id>/edit', methods=["POST"])
def process_edit_food(food_id):
    # 1. find the food record to edit
    food_to_edit = None
    for each_food in database:
        if each_food["id"] == food_id:
            food_to_edit = each_food
            break

    if food_to_edit:
        food_to_edit['name'] = request.form.get('food_name')
        food_to_edit["calories"] = request.form.get('calories')
        food_to_edit['date'] = request.form.get('date')
        food_to_edit['meal'] = request.form.get('meal')

        with open('food.json', 'w') as fp:
            json.dump(database, fp)

        return redirect(url_for('show_food'))

    else:
         return f"The food record with the id of {food_id} is not found!"




# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
