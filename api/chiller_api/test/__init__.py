import logging
import os, tempfile

import connexion
from flask_testing import TestCase

from chiller_api import initialize_application
from chiller_api.db import db


class BaseTestCase(TestCase):

    def _pre_setup(self):
        self._db_fd, self._db_path = tempfile.mkstemp()
        super()._pre_setup()

    def _post_teardown(self):
        super()._post_teardown()
        os.close(self._db_fd)
        os.unlink(self._db_path)

    def create_app(self):
        # this creates an app per method call within the class
        # can't find a place where I can set this up in class variables 
        # per class - need to get to know pytest better to do this
        logging.getLogger('connexion.operation').setLevel('ERROR')
        conapp = initialize_application('./swagger/', {
            'TESTING': True,
            'DATABASE': self._db_path,
        })
        with conapp.app.app_context():
            db.init_db()

        return conapp.app
