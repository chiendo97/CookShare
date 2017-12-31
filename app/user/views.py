from flask import abort, flash, redirect, render_template, url_for, request, jsonify
from flask_login import current_user, login_required

from . import user
from .. import db, foods_img, steps_img, users_img
from ..models import Food, Step, User, Upvote
from ..admin.forms import FoodForm, ImageForm, StepForm
from ..admin.views import check_user

from database import do_query_fetchall, do_query_fetchone

@user.route('/<int:user_id>')
def user_info(user_id):
    # user = User.query.get_or_404(user_id)
    user = do_query_fetchone('get_user_by_user_id', {'user_id':user_id})
    if (user is None):
        abort(404)
    foods = do_query_fetchall('get_all_food_from_user_id',{'user_id':user_id})

    return render_template('admin/users/user.html',
                           foods=foods,
                           user=user
                           )