#!/usr/bin/env python
from flask import Flask, make_response, jsonify
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException
from app.health_check import initalize_healthcheck

def create_flask_app(config_module=None):
    """
    Args:

    - config_file (str)

    """

    app = Flask(__name__)
    app.config.from_object('config.config_default')
    if config_module:
        app.config.from_object(config_module) #overrides defaults

    initalize_healthcheck(app)

    from app import routes
    app.register_blueprint(routes.api)

    # handle all Werkzerg errors not explicitly handled in the routes
    # modified from: http://flask.pocoo.org/snippets/83/
    def make_json_error(ex):
        status_code = (ex.code
                        if isinstance(ex, HTTPException)
                        else 500)
        response = jsonify(status_code=status_code, status_message=str(ex))
        response.status_code = status_code
        return response

    for code in default_exceptions.iterkeys():
        app.error_handler_spec[None][code] = make_json_error

    return app

app = create_flask_app()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0') # host controls who can access the API.
