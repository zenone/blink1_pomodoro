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
try:
    from blink1.blink1 import blink1
except ImportError:
    print('Error: blink1 library not installed.')
    print('Try `pip install blink1` and run again.')
    sys.exit(1)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')


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
            flash_blink()

            # Short Rest
            if set < TIME_SETS and rep + 1 < TIME_REPS:
                status(set=set, rep=rep, msg='Rest ({0} mins)'.format(TIME_REST))
                use_blink(color='yellow', minutes=TIME_REST)
                flash_blink()

        # Long(er) Break
        if set + 1 < TIME_SETS:
            status(set=set, rep=rep, msg='Break ({0} mins)'.format(TIME_BREAK))
            use_blink(color='green', minutes=TIME_BREAK)
            flash_blink()


def use_blink(color, minutes):
    """
    This function will change the color of the blink(1) device based upon
    where we're at in the pomodoro session.
    :param color: str
    :param minutes: int (or float)
    """
    try:
        with blink1() as b1:
            b1.fade_to_color(1000, color)
            time.sleep(minutes * 60)
    except KeyboardInterrupt:
        control_c(b1)
    except Exception as e:
        no_device_found(e)


def flash_blink():
    """
    Flash the blink(1) between blue and red.
    """
    try:
        with blink1() as b1:
            b1.fade_to_rgb(.5, 0, 0, 0)
            for i in xrange(5):
                b1.fade_to_color(100, 'blue')
                time.sleep(.1)
                b1.fade_to_color(100, 'red')
                time.sleep(.1)
            b1.fade_to_rgb(.5, 0, 0, 0)
    except KeyboardInterrupt:
        control_c(b1)
    except Exception as e:
        no_device_found(e)


def control_c(b1):
    """
    Turn off blink(1) when contrl-c is pressed.
    :param b1: blink1 function
    """
    logging.info('Exiting. Control-C pressed.')
    b1.fade_to_rgb(1000, 0, 0, 0)
    b1.close()
    sys.exit(1)


def no_device_found(e):
    """
    Inform user if blink(1) device is not found.
    """
    logging.info('Error: {0}'.format(e))
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
