#!/usr/bin/python
import logging
import os
import subprocess

from datetime import datetime


SCRIPT_NAME = 'rfm_ecomanager_logger.py'
EXE_NAME = 'python'
FAILED_FILE = os.path.join(os.environ['HOME'], '__check_lock__')
AUDIO_WARNING = '/usr/share/sounds/speech-dispatcher/test.wav'
LOG_FILE = os.path.join(os.environ['HOME'], 'check.log')


logging.basicConfig(filename=LOG_FILE, level=logging.INFO)


def check_process_running():
    """Check for the rfm_ecomanager_logger.py process"""
    output = subprocess.check_output(['ps','-ax'])
    for line in output.splitlines():
        if SCRIPT_NAME in line and EXE_NAME in line:
            return line
    return None


def play_warning():
    logging.info("Playing warning @ %s" % datetime.now())
    subprocess.Popen(['paplay', '--volume', '65536', AUDIO_WARNING])


try:
    process_running = check_process_running()
except:
    # Unable to check the process! WARN!
    logging.exception('Failed to check processes')
    play_warning()
else:
    if process_running:
        if os.path.exists(FAILED_FILE):
            os.remove(FAILED_FILE)
    if not process_running:
        # Attempt to restart ...
        cmd = '/usr/bin/python {Home}/rfm_ecomanager_logger/rfm_ecomanager_logger/rfm_ecomanager_logger.py --data-directory {Home}/Desktop/Data'.format(Home=os.environ['HOME'])
        subprocess.Popen(cmd.split(), cwd=os.path.join(os.environ['HOME'],
                                                       'rfm_ecomanager_logger'))
        if os.path.exists(FAILED_FILE):
            play_warning()
        with open(FAILED_FILE, 'w') as f:
            f.write('FAILED AT %s' % datetime.now())
