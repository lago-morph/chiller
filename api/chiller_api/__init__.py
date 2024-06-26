# this file is called when we *import* chiller_api.  This is so we can have
# an app object created for using the CLI

import os
import connexion

from chiller_api import encoder
from chiller_api.db import db


def create_app():
    conapp = initialize_application('./swagger/')
    return conapp.app


def initialize_application(spec_dir, local_config=None):

    conapp = connexion.App(__name__, specification_dir=spec_dir)
    conapp.app.json_encoder = encoder.JSONEncoder
    conapp.add_api('swagger.yaml')

    if local_config is not None:
        conapp.app.config.from_mapping(local_config)

    if 'SECRET_KEY' not in conapp.app.config:
        conapp.app.config['SECRET_KEY'] = 'dev'
    if 'DATABASE' not in conapp.app.config:
        database = os.path.join(conapp.app.instance_path, 
                                        'chiller_api.sqlite')
        conapp.app.config['DATABASE'] = database

    # make sure the instance folder exists
        try:
            os.makedirs(conapp.app.instance_path)
        except OSError:
            pass

    db.init_app(conapp.app)

    return conapp


