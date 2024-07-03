# this file is called when we *import* chiller_api.  This is so we can have
# an app object created for using the CLI

import os
import connexion

from chiller_api import encoder
from chiller_api.db import db


def create_app():
    conapp = initialize_application('./swagger/')
    return conapp.app

class ConfigurationException(Exception):
    """Raised when configuration is not complete"""

def config_from_env(config, key, default):
    # check if key is set.  If not, check for environment variable.
    # If still not found, set as a default.
    # If we get to the point where we are trying to set a default, and it
    # is set to None, then that is a fatal error

    d = { }
    if key not in config:
        if key in os.environ:
            d[key] = os.environ[key]
        elif default is not None:
            d[key] = default
        else:
            raise ConfigurationException(
                    f"environment variable {key} must be set")
    return d


def initialize_application(spec_dir, local_config=None):

    conapp = connexion.App(__name__, specification_dir=spec_dir)
    conapp.app.json_encoder = encoder.JSONEncoder
    conapp.add_api('swagger.yaml')

    if local_config is not None:
        conapp.app.config.from_mapping(local_config)

    c = {}
    c.update(config_from_env(conapp.app.config, 'SECRET_KEY', 'dev'))
    c.update(config_from_env(conapp.app.config, 'CHILLER_DB_NAME', 'chiller'))
    c.update(config_from_env(conapp.app.config, "CHILLER_DB_HOST", "localhost"))
    c.update(config_from_env(conapp.app.config, "CHILLER_DB_USER", "postgres"))
    c.update(config_from_env(conapp.app.config, "CHILLER_DB_PASSWORD", None))
    c.update(config_from_env(conapp.app.config, "CHILLER_DB_PORT", '5432'))

    conapp.app.config.from_mapping(c)

    db.init_app(conapp.app)

    return conapp


