#!/usr/bin/python

# mousic

# reads low-level mouse events,
# produces MIDI events

import evdev
import rtmidi
import rtmidi.midiconstants
import time

MIDDLE_C = 60 # midi value of middle c

def main():
    mouse_dev = evdev.InputDevice('/dev/input/event1')

    midiout = rtmidi.MidiOut()
    available_ports = midiout.get_ports()
    if available_ports:
        midiout.open_port(0)
    else:
        midiout.open_virtual_port("mousic virtual output")

    for event in mouse_dev.read_loop():
        if event.type != evdev.ecodes.EV_REL:
            continue

        code = evdev.ecodes.REL[event.code]
        #print '%s %i' % (code, event.value)

        if code == 'REL_X':
            channel = 4
        elif code == 'REL_Y':
            channel = 8
        elif code == 'REL_WHEEL':
            channel = 11
        else:
            raise RuntimeError('unexpected code %s' % code)

        note = MIDDLE_C + event.value # value may be negative
        note_on = [channel | rtmidi.midiconstants.NOTE_ON, note, 112]
        note_off = [channel | rtmidi.midiconstants.NOTE_OFF, note, 0]
        midiout.send_message(note_on)
        time.sleep(0.05)
        midiout.send_message(note_off)

    del midiout

main()
