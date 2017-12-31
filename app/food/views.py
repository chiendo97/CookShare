from flask import abort, flash, redirect, render_template, url_for, request, jsonify
from flask_login import current_user, login_required

from . import food
from .. import db, foods_img, steps_img, users_img
from ..models import Food, User, Upvote, Step
from ..admin.forms import FoodForm, ImageForm, StepForm

from database import do_query_fetchall

@food.route('/')
def list_all_food():
    foods = do_query_fetchall('get_all_food', {})
    top_users = do_query_fetchall('get_top_users', {})

    # return jsonify([dict(row) for row in foods]);
    return render_template('admin/foods/foods.html',
                           foods = foods,
                           users = top_users
                           )

@food.route('/add', methods=['GET', 'POST'])
@login_required
def add_food():
    form = FoodForm()
    image = ImageForm()
    if form.validate_on_submit():
        food = Food(name=form.name.data,
                    desc=form.desc.data,
                    user_id=current_user.id)

        if (request.files['photo'].filename):
            filename = foods_img.save(request.files['photo'])
            food.food_img_url = filename

        try:
            db.session.add(food)
            db.session.commit()
            flash('You have successfully added a new Food')
        except:
            flash('Error: food name already exists.')

        return redirect(url_for('food.list_all_food'))

    return render_template('admin/foods/food.html',
                           action="Add",
                           user_id=current_user.id,
                           add_food=True,
                           form=form,
                           image=image,
                           title="Add food")

@food.route('/edit/<int:food_id>', methods=['GET', 'POST'])
@login_required
def edit_food(food_id):
    food = Food.query.get_or_404(food_id)

    check_user(food.user_id)

    form = FoodForm(obj=food)
    if form.validate_on_submit():
        food.name = form.name.data
        food.desc = form.desc.data

        if (request.files['photo'].filename):
            filename = foods_img.save(request.files['photo'])
            food.food_img_url = filename

        db.session.commit()
        flash("You have successfully edited the Food")

        return redirect(url_for('food.list_all_food'))

    form.desc.data = food.desc
    form.name.data = food.name
    return render_template('admin/foods/food.html',
                           action="Edit",
                           add_food=False,
                           form=form,
                           food=food, title="Edit Food")

@food.route('/delete/<int:food_id>')
@login_required
def delete_food(food_id):
    food = Food.query.get_or_404(food_id)

    check_user(food.user_id)

    db.session.delete(food)
    db.session.commit()
    flash('You have successfully deleted food.')

    return redirect(url_for('food.list_all_food'))

def check_user(food_id):
    if food_id != current_user.id:
        abort(403)
