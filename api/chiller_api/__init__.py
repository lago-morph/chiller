# this file is called when we import chiller_api.  This is so we can have
# an app object created for using the CLI

import os
import connexion

from chiller_api import encoder
from chiller_api.common import common_init


def create_app():
    conapp = connexion.App(__name__, specification_dir='./swagger/')

    conapp.app.json_encoder = encoder.JSONEncoder
    conapp.add_api('swagger.yaml')

    common_init(conapp)

    return conapp.app
