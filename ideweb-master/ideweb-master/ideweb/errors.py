# -*- coding: utf-8 -*-
"""
ideweb.errors
~~~~~~~~~~~~~

Error views.

:copyright: Copyright 2016 by Matt Swain.
:license: MIT, see LICENSE file for more details.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging

from flask import render_template, request, jsonify

from . import app


log = logging.getLogger(__name__)


def get_message(e):
    if hasattr(e, 'data') and 'messages' in e.data:
        return e.data['messages']
    if hasattr(e, 'description'):
        return e.description
    elif hasattr(e, 'msg'):
        return e.msg
    elif hasattr(e, 'message'):
        return e.message
    else:
        return repr(e)


@app.errorhandler(400)
def forbidden(e):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'bad request', 'message': get_message(e)})
        response.status_code = 400
        return response
    return render_template('400.html', description=get_message(e)), 400


@app.errorhandler(403)
def forbidden(e):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'forbidden', 'message': get_message(e)})
        response.status_code = 403
        return response
    return render_template('403.html', description=get_message(e)), 403


@app.errorhandler(404)
def page_not_found(e):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'not found', 'message': get_message(e)})
        response.status_code = 404
        return response
    return render_template('404.html', description=get_message(e)), 404


@app.errorhandler(422)
def unprocessable_entity(e):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'unprocessable entity', 'message': get_message(e)})
        response.status_code = 422
        return response
    return render_template('422.html', description=get_message(e)), 422


@app.errorhandler(500)
def internal_server_error(e):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'internal server error', 'message': get_message(e)})
        response.status_code = 500
        return response
    return render_template('500.html', description=get_message(e)), 500


@app.errorhandler(503)
def internal_server_error(e):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'service unavailable', 'message': get_message(e)})
        response.status_code = 503
        return response
    return render_template('503.html', description=get_message(e)), 503
