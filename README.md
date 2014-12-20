# mousic

Experimenting with translation of low-level mouse events to MIDI events.

Intended for use on a headless Raspberry Pi working as a "music instrument".

# how to run

1. install requirements

    $ pip install -r requirements.txt

3. start mousic; on most systems root privileges will be required, as regular users aren't allowed to read the devices in /dev/input

    $ python mousic.py

4. connect mousic to some midi synthesizer. I use Jack to connect mousic to QSynth.

5. enjoy the noise on every mouse movement

# license

GNU/GPL v. 3 or later
