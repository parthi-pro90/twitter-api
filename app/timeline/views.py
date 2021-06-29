from flask import Blueprint, redirect, request, render_template, url_for
from app import app
from app.timeline.controller import get_timeline_data

timeline_blueprint = Blueprint(
    'timeline_blueprint',
    __name__,
    url_prefix='/user',
    template_folder='templates'
)

@timeline_blueprint.route('/timeline', methods=['GET', 'POST'])
def timeline():
    data = get_timeline_data(request)
    return render_template('timeline.html', data=data) 