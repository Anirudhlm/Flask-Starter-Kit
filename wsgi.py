#!usr/bin/env python

# Create the WSGI Entry Point
from run import app
application = app # uwsgi needs the thing it runs to be called 'application'
if __name__ == "__main__":
    application.run()
