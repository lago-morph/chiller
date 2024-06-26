import logging

import connexion
from flask_testing import TestCase

from chiller_api.encoder import JSONEncoder
from chiller_api.common import common_init


class BaseTestCase(TestCase):

    def create_app(self):
        logging.getLogger('connexion.operation').setLevel('ERROR')
        app = connexion.App(__name__, specification_dir='../swagger/')
        app.app.json_encoder = JSONEncoder
        app.add_api('swagger.yaml')
        common_init(app)
        return app.app
