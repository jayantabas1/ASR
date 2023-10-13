"""
 Copyright Flexday Solutions LLC, Inc - All Rights Reserved
 Unauthorized copying of this file, via any medium is strictly prohibited
 Proprietary and confidential
 See file LICENSE.txt for full license details.
 
"""

# app/__init__.py

from flask import Flask

app = Flask(__name__)

# Import routes here
from app import routes
