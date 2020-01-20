# -*- coding: utf-8 -*-
"""
ideweb.models
~~~~~~~~~~~~~

Data models.

:copyright: Copyright 2016 by Matt Swain.
:license: MIT, see LICENSE file for more details.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging
from datetime import datetime

from sqlalchemy.dialects.postgresql import JSONB

from . import db


log = logging.getLogger(__name__)


class IdeJob(db.Model):
    """An ImageDataExtractor job."""
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    file = db.Column(db.String, nullable=True)
    url = db.Column(db.String, nullable=True)
    result = db.Column(JSONB, nullable=True)

    @property
    def status(self):
        from .tasks import celery
        return celery.AsyncResult(self.job_id).status


class CdeJob(db.Model):
    """A ChemDataExtractor job."""
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    file = db.Column(db.String, nullable=True)
    url = db.Column(db.String, nullable=True)
    result = db.Column(JSONB, nullable=True)

    @property
    def status(self):
        from .tasks import celery
        return celery.AsyncResult(self.job_id).status


class ChemDict(db.Model):
    """A chemical name with associated SMILES."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    smiles = db.Column(db.String, nullable=True)


class User(db.Model):
    """Registered user."""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=True)
    affiliation = db.Column(db.String, nullable=True)
