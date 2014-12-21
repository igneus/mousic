# players.py

# generators interpreting mouse input as midi events

import evdev
import rtmidi.midiconstants
import time

MIDI_NOTE_MIN = 21
MIDI_NOTE_MAX = 107

def normalize_midi_note_value(value, _min=MIDI_NOTE_MIN, _max=MIDI_NOTE_MAX):
    """
    returns value or the nearest valied MIDI note value
    """

    if value < _min:
        return _min
    elif value > _max:
        return _max

    return value

def naive(mouse_dev, base_note=60, sleep_interval=0.1, channel_x=1, channel_y=2, channel_wheel=3):
    """
    translates each and every mouse event to a MIDI event
    """

    for event in mouse_dev.read_loop():
        if event.type != evdev.ecodes.EV_REL:
            continue

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
        note_on = [channel | rtmidi.midiconstants.NOTE_ON, note, 112]
        note_off = [channel | rtmidi.midiconstants.NOTE_OFF, note, 0]

        yield note_on
        time.sleep(sleep_interval)
        yield note_off

def forgetting(mouse_dev, base_note=60, sleep_interval=0.1, channel_x=1, channel_y=2, channel_wheel=3):
    """
    reads several events at once and only translates the first of them
    to a MIDI event
    """

    while True:
        try:
            events = mouse_dev.read()
            event = events.next()
        except IOError as e:
            # resource unavailable
            time.sleep(sleep_interval)
            continue

        if event.type != evdev.ecodes.EV_REL:
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
        note_on = [channel | rtmidi.midiconstants.NOTE_ON, note, 112]
        note_off = [channel | rtmidi.midiconstants.NOTE_OFF, note, 0]

        yield note_on
        time.sleep(sleep_interval)
        yield note_off

def concatenating(mouse_dev, base_note=60, sleep_interval=0.1, channel_x=1, channel_y=2, channel_wheel=3):
    """
    reads several events at once and concatenates them to 1-3 larger ones
    """

    while True:
        buff = {}

        try:
            events = mouse_dev.read()

            for event in events:
                if event.type != evdev.ecodes.EV_REL:
                    continue

                code = evdev.ecodes.REL[event.code]
                # 'REL_X' -> 'x'
                add_to = code.split('_')[1].lower()

                if add_to not in buff:
                    buff[add_to] = 0
                buff[add_to] += event.value
        except IOError as e:
            # resource unavailable
            time.sleep(sleep_interval)
            continue

        channels = (
            ('x', channel_x),
            ('y', channel_y),
            ('wheel', channel_wheel))
        for axis, channel in channels:
            if axis not in buff:
                continue

            note = base_note + buff[axis] # value may be negative
            note = normalize_midi_note_value(note)

            note_on = [channel | rtmidi.midiconstants.NOTE_ON, note, 112]
            note_off = [channel | rtmidi.midiconstants.NOTE_OFF, note, 0]

            yield note_on
            time.sleep(sleep_interval)
            yield note_off

