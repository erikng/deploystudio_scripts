#!/usr/bin/python
import plistlib
import subprocess
import sys
import os

"""
             Name:  Automated_DS_Workflows.py
      Description:  Allows user input to trigger hidden workflows.
           Thanks:  Michael Lynn for being the nicest guy on the planet.
                    Per Olofsson for original PyObjC trigger script. http://www.deploystudio.com/Forums/viewtopic.php?pid=11522#p11522
                    Nate Felton for telling me about DS triggers.
           Author:  Erik Gomez <e@eriknicolasgomez.com>
          Created:  2015-07-03
    Last Modified:  2015-08-03
          Version:  1.03
"""

def trigger(arg):
    # Method for calling Per's PyObjC script.
	# Environmental DS Variable (Thanks Tim Sutton!)
    triggerpy = os.path.join(os.environ['DS_REPOSITORY_PATH'], 'Scripts', 'trigger.py')
    # triggerpy = sys.path[0] + '/trigger.py' # Useful for local testing - Comment out line above.
    cmd = ['python', triggerpy] + arg
    proc = subprocess.Popen(cmd, shell=False, bufsize=-1,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    output, err = proc.communicate()
    return output

# User Variables
# Couple of notes here.
# 1. The variables are ordered from left to right, however they are displayed in reverse.
# 2. Variable outputs start at 1000 and increase. Left to right.
# 3. It's probably best practice to leave the abort variable.
# 4. Aborts are fun if you have a short "reboot after x seconds" so make sure you select another workflow
# 5. Be mindful of screen space. 6 variables and an abort are probably the max you should use.
# 6. RuntimeSelectWorkflow can reference DS UUID's but they become difficult to track. Use names that you don't plan to change.

arg = ['-b', 'Abort', '-b', 'El Capitan', '-b', 'Yosemite', '-b', 'Mavericks', '-i', 'Please select the image type. Note: El Capitan is currently in BETA.', 'Machine Detected']

buttonPressed = trigger(arg)

if "1000" in buttonPressed:
	# Abort
	print "RuntimeAbortWorkflow: User Aborted!"
	exit()
elif "1001" in buttonPressed:
	# Abort
	print "RuntimeSelectWorkflow: El_Capitan"
elif "1002" in buttonPressed:
	# Abort
	print "RuntimeSelectWorkflow: Yosemite"
elif "1003" in buttonPressed:
	# Abort
	print "RuntimeSelectWorkflow: Mavericks"
