#!/usr/bin/python

# mousic

# reads low-level mouse events,
# produces MIDI events

import evdev
import rtmidi
import players

MIDDLE_C = 60 # midi value of middle c

def main():
    mouse_dev = evdev.InputDevice('/dev/input/event1')

    midiout = rtmidi.MidiOut()
    available_ports = midiout.get_ports()
    if available_ports:
        midiout.open_port(0)
    else:
        midiout.open_virtual_port("mousic virtual output")

    for msg in players.forgetting(mouse_dev, MIDDLE_C, 0.05):
        midiout.send_message(msg)

    del midiout

main()
