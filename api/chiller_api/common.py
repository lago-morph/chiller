import os

def common_init(conapp):
    conapp.app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(conapp.app.instance_path, 'chiller_api.sqlite'),
    )

    # make sure the instance folder exists
    try:
        os.makedirs(conapp.app.instance_path)
    except OSError:
        pass

    from chiller_api.db import db
    db.init_app(conapp.app)
