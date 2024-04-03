from flask import Flask
import logging


# create app instance
logging.info('starting server...')
app = Flask(__name__)
logging.info('server started')

# add routes
from server import routes
