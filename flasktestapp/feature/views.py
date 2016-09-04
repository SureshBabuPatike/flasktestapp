# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template
from flask_login import login_required

from . import models

blueprint = Blueprint('feature', __name__, url_prefix='/features', static_folder='../static')


@blueprint.route('/')
@login_required
def members():
    """List feature."""
    ctxt = {}
    query = models.Feature.query
    # # TODO: client_filter, pagination, tables
    # if user.clients:
    #     query = query.filter(client_id in user.clients)
    ctxt['features'] = query.all()

    return render_template('features/feature_list.html', **ctxt)
