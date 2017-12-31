from flask import abort, flash, redirect, render_template, url_for, request, jsonify
from flask_login import current_user, login_required

from . import step
from .. import db, steps_img
from ..models import Food, Step, Upvote, Post
from ..admin.forms import ImageForm, StepForm, PostForm
from ..admin.views import check_user

from database import do_query_fetchall, do_query_fetchone

@step.route('/<int:food_id>')
def list_all_steps(food_id):
    food = do_query_fetchone('get_food_from_food_id', {'food_id':food_id})

    if (food is None):
        abort(404)

    steps = do_query_fetchall('get_all_steps_from_food_id', {'food_id':food_id})

    commands = do_query_fetchall('get_all_commands_from_food_id', {'food_id':food_id})

    top_user = do_query_fetchall('get_top_users', {})

    if (current_user.is_authenticated):
        user_authenticated = (current_user.id == food.user_id)
    else:
        user_authenticated = False

    # return jsonify([dict(food)])
    # return jsonify([dict(row) for row in food])
    return render_template('admin/steps/steps.html',
                           food=food,
                           food_id = food_id,
                           steps=steps,
                           users=top_user,
                           commands=commands,
                           user_authenticated=user_authenticated,
                           title="Steps")


@step.route('/<int:food_id>/add', methods=['GET', 'POST'])
@login_required
def add_step(food_id):
    food = Food.query.get_or_404(food_id)
    check_user(food.user_id)

    form = StepForm()
    image = ImageForm()
    if (form.validate_on_submit()):
        step = Step(desc=form.desc.data,
                    food_id=food_id)

        if (request.files['image'].filename):
            filename = steps_img.save(request.files['image'])
            step.step_img_url = filename

        try:
            # add step to database
            db.session.add(step)
            db.session.commit()
            flash('You have successfully added a new step')
        except:
            flash('Error: failed to add a new Step')

        # redirect to the food Page
        return redirect(url_for('step.list_all_steps', food_id=food_id))
    # load step template
    return render_template('admin/steps/step.html',
                           add_step=True,
                           form=form,
                           image=image,
                           title='Add step')

@step.route('/<int:food_id>/edit/<int:step_id>', methods=['GET', 'POST'])
@login_required
def edit_step(food_id, step_id):
    food = Food.query.get_or_404(food_id)
    check_user(food.user_id)
    add_step = False
    step = Step.query.get_or_404(step_id)
    form = StepForm(obj=step)
    if form.validate_on_submit():
        step.desc = form.desc.data

        if (request.files['image'].filename):
            filename = steps_img.save(request.files['image'])
            step.step_img_url = filename

        db.session.add(step)
        db.session.commit()
        flash('You have successfully edited a step')

        # redirect to the list step page
        return redirect(url_for('step.list_all_steps', food_id=food_id))

    form.desc = step.desc
    return render_template('admin/steps/step.html',
                           add_step=add_step,
                           form=form,
                           title="Edit Step")

@step.route('/<int:food_id>/delete/<int:step_id>', methods=['GET', 'POST'])
@login_required
def delete_step(food_id, step_id):
    food = Food.query.get_or_404(food_id)
    check_user(food.user_id)
    step = Step.query.get_or_404(step_id)
    db.session.delete(step)
    db.session.commit()
    flash('You have successfully deleted one step')

    # redirect to list step page
    return redirect(url_for('step.list_all_steps', food_id=food_id))

@step.route('/<int:food_id>/upvote')
@login_required
def upvote(food_id):
    user_id=current_user.id
    upvote = do_query_fetchone('get_upvote', {'food_id':food_id,
                                              'user_id':user_id})

    if upvote is None:
        upvote = Upvote(food_id=food_id,user_id=user_id)
        try:
            db.session.add(upvote)
            db.session.commit()
            flash('Upvote success')
        except:
            flash('Upvote fail')
    else:
        flash('Upvoted')

    return redirect(url_for('step.list_all_steps', food_id=food_id))

@step.route('/<int:food_id>/post', methods=['GET', 'POST'])
@login_required
def post(food_id):
    food = Food.query.get_or_404(food_id)

    form = PostForm()

    if (form.validate_on_submit()):
        post = Post(user_id=current_user.id,
                    desc=form.desc.data,
                    food_id=food_id)

        try:
            db.session.add(post)
            db.session.commit()
            flash('You have successfully posted a command')
        except:
            flash('Error: failed to post a command')

        return redirect(url_for('step.list_all_steps', food_id=food_id))

    return render_template('admin/steps/post.html',
                           form=form
                           )