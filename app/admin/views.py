# app/admin/views.py
from flask import abort, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from . import admin
from .. import db, foods_img, steps_img, users_img
from database import do_query_fetchall, do_query_fetchone

def check_user(food_id):
    """
    Check user's right to commit change
    """
    if food_id != current_user.id:
        abort(403)

@admin.route('/search', methods=['POST', 'GET'])
def search():
    if (request.args.get('search') is None):
        abort(404)

    searchfood = '%' + request.args.get('search') + '%'
    food = do_query_fetchall('find_food_by_name', {'name': searchfood})
    top_users = do_query_fetchall('get_top_users', {})

    return render_template('admin/foods/foods.html',
                           foods=food,
                           users=top_users,
                           title="Search_food")

@admin.route('/upload', methods=['POST', 'GET'])
@login_required
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        # filename = foods_img.save(request.files['photo'], name=secure_filename(request.filename))
        img = request.files['photo']
        filename = foods_img.save(request.files['photo'], name=secure_filename(img.filename))
        return filename

    return "Failed"