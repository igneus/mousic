from setuptools import setup

requirements = [f.strip() for f in file('requirements.txt')]

setup(name='mousic',
      version='0.1',
      url='http://github.com/igneus/mousic',
      description='translates mouse events to MIDI music notes',
      keywords='mouse music MIDI',
      author='Jakub Pavlik',
      author_email='jkb.pavlik@gmail.com',
      license='GNU/GPL 3',

      packages=['mousic'],
      install_requires=requirements,
      scripts=['bin/mousic_play.py'],)
