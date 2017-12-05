# app/admin/views.py

import logging

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from forms import FoodForm, StepForm
from .. import db
from ..models import Food, Step, User, Upvote, Upvote_user


def check_user(food_id):
    """
    Check user's right to commit change
    """
    logging.warn(str(food_id) + " " + str(current_user.id))
    if food_id != current_user.id:
        abort(403)

@admin.route('/vote/<int:user_id>/<int:food_id>', methods=['POST', 'GET'])
@login_required
def vote(user_id, food_id):
    upvote = Upvote.query.filter_by(food_id=food_id).filter_by(user_id=user_id).first()
    if upvote is not None:
        try:
            db.session.delete(upvote)
            db.session.commit()
            flash("You have successfuly downvote this Food")

        except:
            flash("Failed to downvote this Food")
    else:
        new_upvote = Upvote(food_id=food_id,
                            user_id=user_id)
        try:
            db.session.add(new_upvote)
            db.session.commit()
            flash("You have successfully upvote this Food")

            food = Food.query.filter_by(id=food_id).first()
            upvote_user = Upvote_user.query.filter_by(user1_id=food.user_id).filter_by(user2_id=user_id).first()
            if (upvote_user is None):
                new_upvote_user = Upvote_user(user1_id=food.user_id,
                                              user2_id=user_id)
                db.session.add(new_upvote_user)
                db.session.commit()
                flash("You have successfuly upvote for this User")

        except:
            flash("Failed to upvote this Food")


    return redirect(url_for('admin.list_food'))

@admin.route('/users/<int:user_id>')
@login_required
def user_info(user_id):
    """
    Show infomation of user
    """
    user = User.query.get_or_404(user_id)
    return render_template('admin/users/user.html',
                           user=user)


@admin.route('/users/<int:user_id>/foods')
@login_required
def list_user_food(user_id):
    """
    List all user's food
    """
    foods = Food.query.filter_by(user_id=user_id).all()
    return render_template('admin/foods/foods.html',
                           foods=foods,
                           user_id=current_user.id,
                           title="User_food")

# Food Views
@admin.route('/foods', methods=['GET', 'POST'])
def list_food():
    """
    List all food
    """

    foods = Food.query.all()

    return render_template('admin/foods/foods.html',
                           foods=foods,
                           title="All_food")

@admin.route('/foods/add', methods=['GET', 'POST'])
@login_required
def add_food():
    """
    Add food by user
    """
    # check_admin()

    add_food = True

    form = FoodForm()
    if form.validate_on_submit():
        food = Food(name=form.name.data,
                    desc=form.desc.data,
                    user_id=current_user.id)
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
    return render_template('admin/foods/food.html',
                           action="Add",
                           user_id=current_user.id,
                           add_food=add_food,
                           form=form,
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

    check_user(food.user_id)

    form = FoodForm(obj=food)
    if form.validate_on_submit():
        food.name = form.name.data
        food.desc = form.desc.data
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
    food = Food.query.get_or_404(id)

    check_user(food.user_id)

    db.session.delete(food)
    db.session.commit()
    flash('You have successfully deleted food.')

    # redirect to the Food page
    return redirect(url_for('admin.list_food'))

@admin.route('/foods/<int:food_id>')
def list_step(food_id):
    """
    List all Step of one Food
    """
    food = Food.query.get_or_404(food_id)

    return render_template('admin/steps/steps.html',
                           food=food,
                           food_id = food_id,
                           title="Steps")

@admin.route('/foods/<int:food_id>/add_step', methods=['POST', 'GET'])
@login_required
def add_step(food_id):
    """
    Add more step
    """

    food = Food.query.get_or_404(food_id)
    check_user(food.user_id)

    add_step = True

    form = StepForm()
    if (form.validate_on_submit()):
        step = Step(desc=form.desc.data,
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
    Edit one step
    """
    food = Food.query.get_or_404(food_id)
    check_user(food.user_id)
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
    Delete step
    """
    food = Food.query.get_or_404(food_id)
    check_user(food.user_id)
    step = Step.query.get_or_404(step_id)
    db.session.delete(step)
    db.session.commit()
    flash('You have successfully deleted one step')

    # redirect to list step page
    return redirect(url_for('admin.list_step', food_id=food_id))