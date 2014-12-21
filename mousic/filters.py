# filters.py

# (input) event filters that either consume some of the events
# without yielding them
# or yield modified events

import evdev

import midiutils

def type_only(queue, _type):
    """
    only yields events of the specified type
    """

    for event in queue:
        if event.type != _type:
            continue

        yield event

def rel_only(queue):
    """
    only yields rel (mouse relative movement) events
    """

    return type_only(queue, evdev.ecodes.EV_REL)

def merge(queue):
    """
    consumes all events and produces 0..3 events merging
    values of events of each type
    """

    buff = {}

    for event in queue:
        code = event.code
        if code not in buff:
            buff[code] = event
        else:
            new_val = buff[code].value + event.value
            buff[code].value = midiutils.normalize_note_value(new_val)

    for event in buff.values():
        yield event
