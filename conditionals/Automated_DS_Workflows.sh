#!/bin/bash

#             Name:  Automated_DS_Workflows.sh
#      Description:  Allows user input to trigger hidden workflows.
#           Thanks:  Per Olofsson for original PyObjC trigger script. http://www.deploystudio.com/Forums/viewtopic.php?pid=11522#p11522
#                    Nate Felton for telling me about DS triggers.
#           Author:  Erik Gomez <e@eriknicolasgomez.com>
#          Created:  2015-07-30
#    Last Modified:  2015-07-30
#          Version:  1.0

# Tool to display a popup message with buttons.
POPUP=`dirname "$0"`/trigger.py

# retval
# Couple of notes here.
# 1. The variables are ordered from left to right, however they are displayed in reverse.
# 2. Variable outputs start at 1000 and increase. Left to right.
# 3. It's probably best practice to leave the abort variable.
# 4. Aborts are fun if you have a short "reboot after x seconds" so make sure you select another workflow
# 5. Be mindful of screen space. 6 variables and an abort are probably the max you should use.
# 6. RuntimeSelectWorkflow can reference DS UUID's but they become difficult to track. Use names that you don't plan to change.

retval=`$POPUP -b 'Abort' -b 'El Capitan' -b 'Yosemite' -b 'Mavericks' -i "Please note that El Capitan is currently in beta." "Please select the image type"`
case $retval in
	1000) # Abort
		echo "RuntimeAbortWorkflow: User Aborted!"
		exit 1
		;;
	1001) # El Capitan
		echo "RuntimeSelectWorkflow: El_Capitan"
		;;
	1002) # Yosemite
		echo "RuntimeSelectWorkflow: Yosemite"
		;;
	1003) # Mavericks
		echo "RuntimeSelectWorkflow: Mavericks"
		;;
esac