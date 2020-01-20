# -*- coding: utf-8 -*-
"""
ideweb.forms
~~~~~~~~~~~~



:copyright: Copyright 2016 by Matt Swain.
:license: MIT, see LICENSE file for more details.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging

from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email


log = logging.getLogger(__name__)


class RegisterForm(Form):
    """Form to register and download."""
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    name = StringField('Full Name', validators=[DataRequired()])
    affiliation = StringField('Affiliation')
    submit = SubmitField('Register & Download')
