#!/bin/bash

#             Name:  Automated_DS_Workflows-Fusion.sh
#      Description:  Determines machine model and allows user input
#                    to trigger hidden workflows. Use case is for
#                    proper formatting/image of Fusion Drives without
#                    end user needing to understand underlying platform.
#           Thanks:  Per Olofsson for original PyObjC trigger script. http://www.deploystudio.com/Forums/viewtopic.php?pid=11522#p11522
#                    Nate Felton for telling me about DS triggers.
#           Author:  Erik Gomez <e@eriknicolasgomez.com>
#          Created:  2015-08-03
#    Last Modified:  2015-08-03
#          Version:  1.01

# Tool to display a popup message with buttons.
POPUP=`dirname "$0"`/trigger.py

# Variables
Hardware_ID=`system_profiler SPHardwareDataType | grep "Model Identifier"`
CHECKFUSION=`system_profiler SPStorageDataType | grep "Medium Type"`

# retval
# Couple of notes here.
# 1. The variables are ordered from left to right, however they are displayed in reverse.
# 2. Variable outputs start at 1000 and increase. Left to right.
# 3. It's probably best practice to leave the abort variable.
# 4. Aborts are fun if you have a short "reboot after x seconds" so make sure you select another workflow
# 5. Be mindful of screen space. 6 variables and an abort are probably the max you should use.
# 6. RuntimeSelectWorkflow can reference DS UUID's but they become difficult to track. Use names that you don't plan to change.

# echo the workflow ID or title prefixed by "RuntimeSelectWorkflow:" according to the machine model
if [[ "$Hardware_ID" == *iMac* ]] && [[ "${CHECKFUSION}" == *"SSD"* && *"Rotational"* ]]
    then
        # Only iMacs have fusion drive.
        retval=`$POPUP -b 'Abort' -b 'El Capitan' -b 'Yosemite' -b 'Mavericks' -i "Please select the image type. Note: El Capitan is currently in BETA." "Fusion Drive Detected"`
        case $retval in
            1000) # Abort
                # Stop workflow
                echo "RuntimeAbortWorkflow: User Aborted!"
                exit 1
                ;;
            1001) # El_Capitan-Fusion_Drive
                echo "RuntimeSelectWorkflow: El_Capitan-Fusion_Drive"
                ;;
            1002) # Yosemite-Fusion_Drive
                echo "RuntimeSelectWorkflow: Yosemite-Fusion_Drive"
                ;;
            1003) # Mavericks-Fusion_Drive
                echo "RuntimeSelectWorkflow: Mavericks-Fusion_Drive"
                ;;
        esac
    else
        # All other models
        retval=`$POPUP -b 'Abort' -b 'El Capitan' -b 'Yosemite' -b 'Mavericks' -i "Please select the image type. Note: El Capitan is currently in BETA." "Machine Detected"`
        case $retval in
            1000) # Abort
                # Stop workflow
                echo "RuntimeAbortWorkflow: User Aborted!"
                exit 1
                ;;
            1001) # El_Capitan
                echo "RuntimeSelectWorkflow: El_Capitan"
                ;;
            1002) # Yosemite
                echo "RuntimeSelectWorkflow: Yosemite"
                ;;
            1003) # Mavericks
                echo "RuntimeSelectWorkflow: Mavericks"
                ;;
        esac
fi