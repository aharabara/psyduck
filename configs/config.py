import logging
import os
from datetime import datetime

import yaml
from event_bus import EventBus

from orator import DatabaseManager, Model

config = yaml.load(open('./orator.yml'))
db = DatabaseManager(config['databases'])
Model.set_connection_resolver(db)

bus = EventBus()

# logger
path = 'logs/chat.log'
os.makedirs(path, exist_ok=True)
logging.basicConfig(filename=path + '/' + str(datetime.now()) + '.log', level=logging.DEBUG)
