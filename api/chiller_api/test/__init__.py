import logging
import os, tempfile

import connexion
from flask_testing import TestCase

from chiller_api import initialize_application
from chiller_api.db import db

import uuid


class BaseTestCase(TestCase):

    def create_app(self):
        # this creates an app per method call within the class
        # can't find a place where I can set this up in class variables 
        # per class - need to get to know pytest better to do this
        logging.getLogger('connexion.operation').setLevel('ERROR')
        db_name = "a%s" % uuid.uuid4().hex
        print(db_name)
        conapp = initialize_application('./swagger/', {
            'TESTING': True,
            'CHILLER_DB_NAME': db_name,
        })
        with conapp.app.app_context():
            db.create_db(db_name)
            db.init_db()

        return conapp.app
