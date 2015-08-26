#!/usr/bin/python
import plistlib
import subprocess
import sys
import os

"""
             Name:  Automated_DS_Workflows-Fusion_No_Trigger.py
      Description:  Determines machine model and starts embedded
                    workflow automatically via print. Use case is for
                    proper formatting/image of Fusion Drives without
                    end user needing to understand underlying platform.
           Thanks:  Michael Lynn for being the nicest guy on the planet.
                    Greg Neagle for showing me I'm still working too hard. - "Why system_profiler?"
                    Nate Felton for telling me about DS triggers.
           Author:  Erik Gomez <e@eriknicolasgomez.com>
          Created:  2015-08-26
    Last Modified:  2015-08-26
          Version:  1.0
"""

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

if 'iMac' in get_model_identifier():
    print "iMac detected"
    if 'ssd' in get_medium_type_disk(0):
        print "SSD detected on disk0 - continuing check"
        if 'rotational' in get_medium_type_disk(1):
			print "HDD detected on disk1. Assuming Fusion Drive"
			isfusion = "1"
        else:
			print "No HDD detected on disk1. iMac is not a Fusion Drive."
			isfusion = "0"
    elif 'ssd' in get_medium_type_cs_disk(0):
		print "SSD detected on disk0 (Core Storage) - continuing check"
		if 'rotational' in get_medium_type_cs_disk(1):
			# print "HDD detected on disk1 (Core Storage). Assuming Fusion Drive (Core Storage)"
			isfusion = "1"
		else:
			print "No HDD detected on disk1. iMac is not a Fusion Drive, but does contain a Core Storage"
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
