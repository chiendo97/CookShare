# app/admin/views.py

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from forms import FoodForm, StepForm
from .. import db
from ..models import Food, Step

# def check_admin():
#     """
#
#     """
#     if not current_user.is_admin:
#         abort(403)

# Food Views

@admin.route('/foods', methods=['GET', 'POST'])
@login_required
def list_food():
    """
    List all departments
    """
    # check_admin()

    foods = Food.query.all()

    return render_template('admin/foods/foods.html',
                           foods=foods, title="Food")

@admin.route('/foods/add', methods=['GET', 'POST'])
def add_food():
    """
    List all food
    """
    # check_admin()

    add_food = True

    form = FoodForm()
    if form.validate_on_submit():
        food = Food(name=form.name.data,
                    desc=form.desc.data,
                    steps=form.steps.data)
        try:
            # add food to database
            db.session.add(food)
            db.session.commit()
            flash('You have successfully added a new Food')
        except:
            flash('Error: food name already exists.')

        # redirect to the food page
        return redirect(url_for('admin.list_food'))

    # load food template
    return render_template('admin/foods/food.html', action="Add",
                           add_food=add_food, form=form,
                           title="Add food")

@admin.route('/foods/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_food(id):
    """
    Edit food
    """
    # check_admin()

    add_food = False

    food = Food.query.get_or_404(id)
    form = FoodForm(obj=food)
    if form.validate_on_submit():
        food.name = form.name.data
        food.desc = form.desc.data
        food.steps = form.steps.data
        db.session.commit()
        flash("You have successfully edited the Food")

        # redirect to the Food page
        return redirect(url_for('admin.list_food'))

    form.desc.data = food.desc
    form.name.data = food.name
    return render_template('admin/foods/food.html', action="Edit",
                           add_food=add_food, form=form,
                           food=food, title="Edit Food")

@admin.route('/foods/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_food(id):
    """
    Delete Food from database
    """
    # check_admin()

    food = Food.query.get_or_404(id)
    db.session.delete(food)
    db.session.commit()
    flash('You have successfully deleted food.')

    # redirect to the Food page
    return redirect(url_for('admin.list_food'))

@admin.route('/foods/<int:food_id>')
@login_required
def list_step(food_id):
    """
    List all Step of one Food
    """
    food = Food.query.get_or_404(food_id)
    steps = Step.query.filter_by(food_id = food_id).all()

    return render_template('admin/steps/steps.html',
                           food=food,
                           food_id = food_id,
                           steps =steps,
                           title="Steps")

@admin.route('/foods/<int:food_id>/add_step/<int:food_order>', methods=['POST', 'GET'])
@login_required
def add_step(food_id, food_order):
    food = Food.query.get_or_404(food_id)

    add_step = True

    form = StepForm()
    if (form.validate_on_submit()):
        step = Step(order=food_order,
                    desc=form.desc.data,
                    food_id=food_id)
        try:
            # add step to database
            db.session.add(step)
            db.session.commit()
            flash('You have successfully added a new step')
        except:
            flash('Error: failed to add new Step')

        # redirect to the food Page
        return redirect(url_for('admin.list_step', food_id=food_id))
    # load step template
    return render_template('admin/steps/step.html',
                           add_step=add_step,
                           form=form,
                           title='Add step')

@admin.route('/foods/<int:food_id>/edit_step/<int:step_id>', methods=['POST', 'GET'])
@login_required
def edit_step(food_id, step_id):
    """

    """

    add_step = False
    step = Step.query.get_or_404(step_id)
    form = StepForm(obj=step)
    if form.validate_on_submit():
        step.desc = form.desc.data
        db.session.add(step)
        db.session.commit()
        flash('You have successfully edited a step')

        # redirect to the list step page
        return redirect(url_for('admin.list_step', food_id=food_id))

    form.desc = step.desc
    return render_template('admin/steps/step.html',
                           add_step=add_step,
                           form=form,
                           title="Edit Step")

@admin.route('/foods/<int:food_id>/delete_step/<int:step_id>')
@login_required
def delete_step(food_id, step_id):
    """

    """

    step = Step.query.get_or_404(step_id)
    db.session.delete(step)
    db.session.commit()
    flash('You have successfully deleted one step')

    # redirect to list step page
    return redirect(url_for('admin.list_step', food_id=food_id))