# midiutils.py

# utilities knowing about the MIDI internals

import rtmidi.midiconstants

MIDI_NOTE_MIN = 21
MIDI_NOTE_MAX = 107

def normalize_note_value(value, _min=MIDI_NOTE_MIN, _max=MIDI_NOTE_MAX):
    """
    returns value or the nearest valied MIDI note value
    """

    if value < _min:
        return _min
    elif value > _max:
        return _max

    return value

def note_on(channel, note, dynamic=112):
    """
    construct 'note on' message for rtmidi
    """

    return [channel | rtmidi.midiconstants.NOTE_ON, note, dynamic]

def note_off(channel, note, dynamic=0):
    """
    construct 'note off' message for rtmidi
    """

    return [channel | rtmidi.midiconstants.NOTE_OFF, note, dynamic]
