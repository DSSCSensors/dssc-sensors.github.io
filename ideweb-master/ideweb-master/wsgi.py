# -*- coding: utf-8 -*-
"""
ideweb.wsgi
~~~~~~~~~~

wsgi script.

"""

import sys


# Ensure the main project directory is on the path
sys.path.insert(0, '/var/www/apps/ideweb')

from ideweb import app as application
