import time

from schematic.code_runner import my_message_queue


def get(channel: int):
    if channel not in my_message_queue:
        my_message_queue[channel] = []
    while len(my_message_queue[channel]) == 0:
        time.sleep(999999999)
    return my_message_queue[channel].pop(0)


def aget(channel: int):
    if channel not in my_message_queue:
        my_message_queue[channel] = []
    if len(my_message_queue[channel]) == 0:
        return None
    return my_message_queue[channel].pop(0)
