# filters.py

# (input) event filters that either consume some of the events
# without yielding them
# or yield modified events

import evdev

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


