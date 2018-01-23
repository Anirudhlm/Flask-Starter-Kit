import json
import socket
import time

from healthcheck import HealthCheck

from app.mongo.client_provider import MongoClientProvider

HEALTHCHECK_PATH = "/api/v1/version"

# global final result messages
SUCCESS_MESSAGE = "happy server is happy"
FAILURE_MESSAGE = "sad server is sad"
VERISON_INDEX = 0
OUTPUT_KEY = 'output'

# individual check results
SUCCESS_STATUS = "success"
FAILURE_STATUS = "failure"

# individual check messages
MONGO_SUCCESS = "mongo: success"
MONGO_FAILURE = "mongo: fail to connect"
ENABLED_SUCCESS = "enabling file is happy"
ENABLED_FAILURE = "enabling file is sad"

def handle_success(results):
    """Process results into a machine and human readable format."""
    data = {
        'version': results[VERISON_INDEX][OUTPUT_KEY],
        'hostname': socket.gethostname(),
        'status': SUCCESS_STATUS,
        'timestamp': time.time(),
        'details': results,
    }
    details = json.dumps(data, indent=2)
    return "{}\n{}".format(SUCCESS_MESSAGE, details)

def handle_failure(results):
    """Process results into a machine and human readable format."""
    data = {
        'hostname': socket.gethostname(),
        'status': FAILURE_STATUS,
        'timestamp': time.time(),
        'results': results,
    }
    details = json.dumps(data, indent=2)
    return "{}\n{}".format(FAILURE_MESSAGE, details)

def check_mongo():
    """Verify access to mongo database

    This check relies on ClientProvider automatically connecting to the database
    """
    try:
        client = MongoClientProvider().get_client()
        return True, MONGO_SUCCESS
    except Exception as e:
        return False, "{} ... {}".format(MONGO_FAILURE, e)

def check_version():
    """Verify a file version is present in the root folder

    This check allows us to manually make a server unhealthy and pull it out
    of load balancing by renaming the file.
    """
    try:
        with open('version', 'r') as f:
            version = open('version', 'r')
            version = version.read().strip('\n')
            return True, version
    except IOError as e:
        return False, "{} ... {}".format(ENABLED_FAILURE, e)

def initalize_healthcheck(app):
    """Inject routing and route handling into the flask app"""
    # wrap the flask app and give a heathcheck url
    health = HealthCheck(app, HEALTHCHECK_PATH,
        success_ttl=None,
        success_handler=handle_success,
        failed_ttl=None,
        failed_handler=handle_failure,
    )

    health.add_check(check_version)
    # Mongo Health check 
    #health.add_check(check_mongo)
    return health