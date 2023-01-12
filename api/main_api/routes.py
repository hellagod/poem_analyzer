from flask import render_template
from api.main_api import bp
from modules.handlers.cloud import get_cloud_data
from modules.handlers.poem import get_poem


@bp.route('/')
def home():
    return render_template('main.html')


@bp.route('/uploadPoem', methods=['POST'])
def upload():
    return get_cloud_data()


@bp.route('/poem', methods=['GET'])
def get_random_poem():
    return get_poem()


