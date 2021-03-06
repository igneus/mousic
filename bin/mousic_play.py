#!/usr/bin/python

# mousic_play.py

# mousic's commandline interface

import sys
import evdev
import rtmidi

import mousic.players as players

MIDDLE_C = 60 # midi value of middle c

def main():
    mouse_dev = evdev.InputDevice('/dev/input/event1')

    midiout = rtmidi.MidiOut()
    available_ports = midiout.get_ports()
    if available_ports:
        midiout.open_port(0)
    else:
        midiout.open_virtual_port("mousic virtual output")

    player = 'xdynamic_ypitch'
    if len(sys.argv) >= 2:
        player = sys.argv[1]

    try:
        for msg in getattr(players, player)(mouse_dev, MIDDLE_C, 0.05):

            try:
                midiout.send_message(msg)
            except OverflowError as e:
                sys.stderr.write('%s: %s\n' % (e.message, str(msg)))

    except KeyboardInterrupt:
        # the program usually runs endlessly until killed
        del midiout

main()
