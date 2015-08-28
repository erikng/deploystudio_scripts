#!/usr/bin/python
import plistlib
import subprocess
import sys
import os

"""
             Name:  Automated_DS_Workflows-DUFusion_No_Trigger.py
      Description:  Determines machine model and starts embedded
                    workflow automatically via print. Use case is for
                    proper formatting/image of Fusion Drives without
                    end user needing to understand underlying platform..
           Author:  Erik Gomez <e@eriknicolasgomez.com>
          Created:  2015-08-28
    Last Modified:  2015-08-28
          Version:  1.0
"""

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
        sp_model_identifier = plist[0]['_items'][0]['machine_model']
        return sp_model_identifier
    except Exception:
        return {}

def get_medium_type_disk(disk_id):
    # Uses diskutil to process whether a physical disk is a SolidState or not.
    disk = 'disk' + str(disk_id)
    cmd = ['/usr/sbin/diskutil', 'info', '-plist', disk]
    proc = subprocess.Popen(cmd, shell=False, bufsize=-1,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    output, err = proc.communicate()
    try:
        plist = plistlib.readPlistFromString(output)
        sp_medium_type = plist['SolidState']
        return sp_medium_type
    except Exception:
        return {}

if 'iMac' in get_model_identifier():
    print "iMac detected"
    if get_medium_type_disk(0) is True:
        print "SSD detected on disk0 - continuing check"
        if get_medium_type_disk(1) is False:
			print "HDD detected on disk1. Assuming Fusion Drive"
			isfusion = "1"
        else:
			print "No HDD detected on disk1. iMac is not a Fusion Drive."
			isfusion = "0"
    else:
        print "This iMac is not a Fusion Drive."
        isfusion = "0"
else:
	print "This machine is not an iMac"
	isfusion = "0"

if "0" in isfusion:
	print "RuntimeSelectWorkflow: Yosemite"
if "1" in isfusion:
	print "RuntimeSelectWorkflow: Yosemite-Fusion_Drive"