import logging
import os
from datetime import datetime

from event_bus import EventBus

from psy.client.message import Message

bus = EventBus()

# logger
path = 'logs/chat.log'
os.makedirs(path, exist_ok=True)
logging.basicConfig(filename=path + '/' + str(datetime.now()) + '.log', level=logging.DEBUG)


@bus.on('client:messages:sent')
@bus.on('client:messages:received')
def log(message: Message):
    logging.info(message)

####
