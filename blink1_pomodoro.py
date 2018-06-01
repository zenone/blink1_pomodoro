#!/usr/bin/env python
# coding=utf-8
#
# About: A Python Pomodoro timer using the blink(1) device as a visual cue.
#
# Requires the blink(1) device and blink1 Python library.
#  * Blink(1) Device: https://blink1.thingm.com/
#  * Blink1 Python Repo.: https://github.com/todbot/blink1-python
#  * Install Blink1 Python Library: `pip install blink1`
#
# More Info.: Wikipedia: https://en.wikipedia.org/wiki/Pomodoro_Technique


# Imports
import logging
import sys
import time
from blink1.blink1 import blink1
logging.basicConfig(level=logging.INFO, format='%(asctime)-2s %(name)-2s %(levelname)-2s %(message)s')


# Configuration
TIME_REPS = 4  # Number of "working" reps
TIME_SETS = 2  # Number of "sets" per days
TIME_WORK = 25  # Minutes
TIME_REST = 5  # Minutes
TIME_BREAK = 30  # Minutes


# The functions
def status(set, rep, msg):
    """
    This function will log a status of where we're at in the pomodoro
    session.
    :param set: int
    :param rep: int
    :param msg: str
    """
    logging.info('Set: {0}, Rep: {0}, Status: {2}'.format(
                 set + 1, rep + 1, msg))


def pomodoro():
    """
    This function handles the logic of the pomodoro timer.
    """
    for set in xrange(TIME_SETS):
        for rep in xrange(TIME_REPS):
            # Work / Focus Session
            status(set=set, rep=rep, msg='Work ({0} mins)'.format(TIME_WORK))
            use_blink(color='red', minutes=TIME_WORK)

            # Short Rest
            if set < TIME_SETS and rep + 1 < TIME_REPS:
                status(set=set, rep=rep, msg='Rest ({0} mins)'.format(TIME_REST))
                use_blink(color='yellow', minutes=TIME_REST)

        # Long(er) Break
        if set + 1 < TIME_SETS:
            status(set=set, rep=rep, msg='Break ({0} mins)'.format(TIME_BREAK))
            use_blink(color='green', minutes=TIME_BREAK)


def use_blink(color, minutes):
    """
    This function will change the color of the blink(1) device based upon
    where we're at in the pomodoro session.
    :param color: str
    :param minutes: int (or float)
    """
    try:
        with blink1() as b1:
            try:
                b1.fade_to_color(1000, color)
                time.sleep(minutes * 60)
            except KeyboardInterrupt:
                logging.info('Exiting. Control-C pressed.')
                b1.fade_to_rgb(1000, 0, 0, 0)
                b1.close()
                sys.exit(1)
    except:
        logging.info('Make sure the blink(1) device is plugged in.')
        logging.info('Exiting.')
        sys.exit(1)


def main():
    """
    Main function
    """
    # Startup
    logging.info('Starting pomodoro timer.')
    use_blink(color='blue', minutes=0.08)  # Almost 5 seconds

    # Do the pomodoro
    pomodoro()

    # Finish
    logging.info('Pomodoro timer ended.')
    use_blink(color='blue', minutes=0.08)  # Almost 5 seconds
    return 0


if __name__ == '__main__':
    sys.exit(main())
