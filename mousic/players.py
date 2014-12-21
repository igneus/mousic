# players.py

# generators interpreting mouse input as midi events

import evdev
import time

import midiutils
import filters

def naive(mouse_dev, base_note=60, sleep_interval=0.1, channel_x=1, channel_y=2, channel_wheel=3):
    """
    translates each and every mouse event to a MIDI event
    """

    for event in filters.rel_only(mouse_dev.read_loop()):
        code = evdev.ecodes.REL[event.code]
        # print '%s %i' % (code, event.value)

        if code == 'REL_X':
            channel = channel_x
        elif code == 'REL_Y':
            channel = channel_y
        elif code == 'REL_WHEEL':
            channel = channel_wheel
        else:
            raise RuntimeError('unexpected code %s' % code)

        note = base_note + event.value # value may be negative

        yield midiutils.note_on(channel, note)
        time.sleep(sleep_interval)
        yield midiutils.note_off(channel, note)

def forgetting(mouse_dev, base_note=60, sleep_interval=0.1, channel_x=1, channel_y=2, channel_wheel=3):
    """
    reads several events at once and only translates the first of them
    to a MIDI event
    """

    while True:
        try:
            events = mouse_dev.read()
            event = filters.rel_only(events).next()
        except IOError as e:
            # resource unavailable
            time.sleep(sleep_interval)
            continue

        code = evdev.ecodes.REL[event.code]

        if code == 'REL_X':
            channel = channel_x
        elif code == 'REL_Y':
            channel = channel_y
        elif code == 'REL_WHEEL':
            channel = channel_wheel
        else:
            raise RuntimeError('unexpected code %s' % code)

        note = base_note + event.value # value may be negative

        yield midiutils.note_on(channel, note)
        time.sleep(sleep_interval)
        yield midiutils.note_off(channel, note)

def merging(mouse_dev, base_note=60, sleep_interval=0.1, channel_x=1, channel_y=2, channel_wheel=3):
    """
    reads several events at once and concatenates them to 1-3 larger ones
    """

    while True:
        buff = {}

        try:
            events = mouse_dev.read()

            for event in filters.merge(filters.rel_only(events)):
                code = evdev.ecodes.REL[event.code]
                if code == 'REL_X':
                    channel = channel_x
                elif code == 'REL_Y':
                    channel = channel_y
                elif code == 'REL_WHEEL':
                    channel = channel_wheel
                else:
                    raise RuntimeError('unexpected code %s' % code)

                note = base_note + event.value # value may be negative

                yield midiutils.note_on(channel, note)
                time.sleep(sleep_interval)
                yield midiutils.note_off(channel, note)
        except IOError:
            # resource unavailable
            time.sleep(sleep_interval)
            continue

def xdynamic_ypitch(mouse_dev, base_note=60, sleep_interval=0.1, channel_x=3, channel_y=2, channel_wheel=3):
    """
    keeps internally absolute pitch;
    y movements change pitch,
    x movements are translated to note events with dynamic corresponding
    to the mouse event value.

    channel_y and channel_wheel are not used.
    """

    note = base_note
    channel = channel_x

    for event in filters.rel_only(mouse_dev.read_loop()):
        code = evdev.ecodes.REL[event.code]

        if code in ('REL_Y', 'REL_WHEEL'):
            note = midiutils.normalize_note_value(note + event.value / 5.0)

        elif code == 'REL_X':
            dynamic = 80 + abs(event.value)

            yield midiutils.note_on(channel, note, dynamic)
            time.sleep(sleep_interval)
            yield midiutils.note_off(channel, note)
