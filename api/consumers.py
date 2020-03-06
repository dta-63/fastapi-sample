import logging
from tools.kafka import Message


def items_consumer_callback(msg: Message):
    logging.info('Message receive {} {} {} {} {}'.format(
        msg.topic(),
        msg.partition(),
        msg.offset(),
        str(msg.key()),
        msg.value(),
    ))
