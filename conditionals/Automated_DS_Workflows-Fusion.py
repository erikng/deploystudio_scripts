#!/usr/bin/python
import plistlib
import subprocess
import sys
import os

"""
             Name:  Automated_DS_Workflows-Fusion.py
      Description:  Determines machine model and allows user input
                    to trigger hidden workflows. Use case is for
                    proper formatting/image of Fusion Drives without
                    end user needing to understand underlying platform.
           Thanks:  Michael Lynn for being the nicest guy on the planet.
                    Greg Neagle for showing me I'm still working too hard. - "Why system_profiler?"
                    Per Olofsson for original PyObjC trigger script. http://www.deploystudio.com/Forums/viewtopic.php?pid=11522#p11522
                    Nate Felton for telling me about DS triggers.
           Author:  Erik Gomez <e@eriknicolasgomez.com>
          Created:  2015-08-03
    Last Modified:  2015-08-03
          Version:  1.01
"""

# Rather than import the module like a sane person, let's just do this.
os.chdir(sys.path[0])

# eventually move to diskutil list -plist  & diskutil info -plist disk0/etc. Easier to parse.

def get_model_identifier():
    # Uses system_profiler to find the model identifier of the machine.
    cmd = ['/usr/sbin/system_profiler', '-xml', 'SPHardwareDataType']
    proc = subprocess.Popen(cmd, shell=False, bufsize=-1,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    output, err = proc.communicate()
    try:
        plist = plistlib.readPlistFromString(output)
        # Down the rabbit hole we go...
        sp_model_identifier = plist[0]['_items'][0]['machine_model']
        return sp_model_identifier
    except Exception:
        return {}

def get_medium_type_disk(disk_id):
    # Uses system_profiler to find the medium types for Physical Drives on the machine. SSD or HDD.
    # Need to check for non CS volumes just in case someone recklessly blew away the entire Fusion Drive CS volume.
    cmd = ['/usr/sbin/system_profiler', '-xml', 'SPStorageDataType']
    proc = subprocess.Popen(cmd, shell=False, bufsize=-1,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    output, err = proc.communicate()
    try:
        plist = plistlib.readPlistFromString(output)
        # Further down the rabbit hole...
        sp_medium_type = plist[0]['_items'][disk_id]['physical_drive']['medium_type']
        return sp_medium_type
    except Exception:
        return {}

def get_medium_type_cs_disk(disk_id):
    # Uses system_profiler to find the medium types for Physical Drives on the machine. SSD or HDD.
    cmd = ['/usr/sbin/system_profiler', '-xml', 'SPStorageDataType']
    proc = subprocess.Popen(cmd, shell=False, bufsize=-1,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    output, err = proc.communicate()
    try:
        plist = plistlib.readPlistFromString(output)
        # Further down the rabbit hole...
        sp_medium_type_cs = plist[0]['_items'][0]['com.apple.corestorage.pv'][disk_id]['medium_type']
        return sp_medium_type_cs
    except Exception:
        return {}

def trigger(arg):
    # Method for calling Per's PyObjC script.
    cmd = ['python', 'trigger.py'] + arg
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

normal = ['-b', 'Abort', '-b', 'El Capitan', '-b', 'Yosemite', '-b', 'Mavericks', '-i', 'Please note that El Capitan is currently in beta.', 'Please select the image type']
fusion = ['-b', 'Abort', '-b', 'El Capitan', '-b', 'Yosemite', '-b', 'Mavericks', '-i', 'Please note that El Capitan is currently in beta. Fusion Drive detected.', 'Please select the image type']

if 'iMac' in get_model_identifier():
    print "iMac detected"
    if 'ssd' in get_medium_type_disk(0):
        print "SSD detected on disk0 - continuing check"
        if 'rotational' in get_medium_type_disk(1):
			print "HDD detected on disk1. Assuming Fusion Drive"
			isfusion = "1"
			buttonPressed = trigger(fusion)
        else:
			print "No HDD detected on disk1. iMac is not a Fusion Drive."
			isfusion = "0"
			buttonPressed = trigger(normal)
    elif 'ssd' in get_medium_type_cs_disk(0):
		print "SSD detected on disk0 (Core Storage) - continuing check"
		if 'rotational' in get_medium_type_cs_disk(1):
			# print "HDD detected on disk1 (Core Storage). Assuming Fusion Drive (Core Storage)"
			isfusion = "1"
			buttonPressed = trigger(fusion)
		else:
			print "No HDD detected on disk1. iMac is not a Fusion Drive, but does contain a Core Storage"
			isfusion = "0"
			buttonPressed = trigger(normal)
else:
	print "This machine is not an iMac"
	isfusion = "0"
	buttonPressed = trigger(normal)

if "0" in isfusion:
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
if "1" in isfusion:
	if "1000" in buttonPressed:
		# Abort
		print "RuntimeAbortWorkflow: User Aborted!"
		exit()
	elif "1001" in buttonPressed:
		# Abort
		print "RuntimeSelectWorkflow: El_Capitan-Fusion_Drive"
	elif "1002" in buttonPressed:
		# Abort
		print "RuntimeSelectWorkflow: Yosemite-Fusion_Drive"
	elif "1003" in buttonPressed:
		# Abort
		print "RuntimeSelectWorkflow: Mavericks-Fusion Drive"
