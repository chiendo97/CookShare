# app/admin/views.py

import logging

from flask import abort, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required
from sqlalchemy import func
from werkzeug.utils import secure_filename

from . import admin
from forms import FoodForm, StepForm, ImageForm
from .. import db, foods_img, steps_img, users_img
from ..models import Food, Step, User, Upvote

def check_user(food_id):
    """
    Check user's right to commit change
    """
    if food_id != current_user.id:
        abort(403)


@admin.route('/upload', methods=['POST', 'GET'])
@login_required
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        # filename = foods_img.save(request.files['photo'], name=secure_filename(request.filename))
        img = request.files['photo']
        filename = foods_img.save(request.files['photo'], name=secure_filename(img.filename))
        return foods_img.path(filename)

    return "Failed"

@admin.route('/vote/<int:user_id>/<int:food_id>/<int:ref>', methods=['POST', 'GET'])
@login_required
def vote(user_id, food_id, ref):
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

        except:
            flash("Failed to upvote this Food")

    if ref==0:
        return redirect(url_for('admin.list_food'))
    else:
        return redirect(url_for('admin.list_user_food', user_id=ref))

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
    # foods = db.session.query(Food, Upvote, func.count(Upvote.food_id)).join(Upvote, isouter=True).group_by(Food.id)
    foods = db.session.query(Food, Upvote, func.count(Upvote.food_id)).join(Upvote, isouter=True).group_by(
        Food.id).filter(Food.user_id == user_id)

    if foods.count() == 0:
        abort(404)

    top_users = db.session.query(User, func.count(User.id).label('asdf')).join(Food, User.id == Food.user_id).group_by(
        User.id).order_by('asdf desc');

    return render_template('admin/foods/foods.html',
                           foods=foods,
                           user_id=current_user.id,
                           ref=current_user.id,
                           users=top_users,
                           title="User_food")

# Food Views
@admin.route('/foods', methods=['GET', 'POST'])
def list_food():
    """
    List all food
    """

    foods = db.session.query(Food, Upvote, func.count(Upvote.food_id)).join(Upvote, isouter=True).group_by(Food.id)

    top_users = db.session.query(User, func.count(User.id).label('asdf')).join(Food, User.id == Food.user_id).group_by(
        User.id).order_by('asdf desc');

    return render_template('admin/foods/foods.html',
                           foods=foods,
                           ref=0,
                           users=top_users,
                           title="All_food")

@admin.route('/foods/add', methods=['GET', 'POST'])
@login_required
def add_food():
    """
    Add food by user
    """

    form = FoodForm()
    image = ImageForm()
    if form.validate_on_submit():
        img_filename = request.files['photo'].filename
        if (img_filename == ''):
            food = Food(name=form.name.data,
                        desc=form.desc.data,
                        user_id=current_user.id)
        else:
            foods_img.save(request.files['photo'])
            food = Food(name=form.name.data,
                        desc=form.desc.data,
                        img_url=img_filename,
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
                           add_food=True,
                           form=form,
                           image=image,
                           title="Add food")

@admin.route('/foods/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_food(id):
    """
    Edit food
    """

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
    return render_template('admin/foods/food.html',
                           action="Edit",
                           add_food=False,
                           form=form,
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

    top_users = db.session.query(User, func.count(User.id).label('asdf')).join(Food, User.id == Food.user_id).group_by(
        User.id).order_by('asdf desc');

    return render_template('admin/steps/steps.html',
                           food=food,
                           food_id = food_id,
                           users=top_users,
                           title="Steps")

@admin.route('/foods/<int:food_id>/add_step', methods=['POST', 'GET'])
@login_required
def add_step(food_id):
    """
    Add more step
    """

    food = Food.query.get_or_404(food_id)
    check_user(food.user_id)

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
            flash('Error: failed to add a new Step')

        # redirect to the food Page
        return redirect(url_for('admin.list_step', food_id=food_id))
    # load step template
    return render_template('admin/steps/step.html',
                           add_step=True,
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