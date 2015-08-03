#!/usr/bin/python

import sys
import optparse
import objc
from AppKit import *
from Foundation import *


class AlertPopup(object):
    
    def __init__(self, messageText):
        super(AlertPopup, self).__init__()
        self.messageText = messageText
        self.informativeText = ""
        self.buttons = []
    
    def createAlert_(self, timer):
        alert = NSAlert.alloc().init()
        alert.setMessageText_(self.messageText)
        alert.setInformativeText_(self.informativeText)
        alert.setAlertStyle_(NSInformationalAlertStyle)
        for button in self.buttons:
            alert.addButtonWithTitle_(button)
        NSApp.activateIgnoringOtherApps_(True)
        buttonPressed = alert.runModal()
        print buttonPressed
        NSApp.terminate_(self)
    
    def startRunLoop(self):
        NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(1, self, 'createAlert:', "", False)
        NSApplication.sharedApplication()
        NSApp.run()
    

def main(argv):
    p = optparse.OptionParser()
    p.set_usage("""Usage: %prog [options] 'message text'""")
    p.add_option("-i", "--info", action="store",
                 dest="info", help="Informative message.")
    p.add_option("-b", "--button", action="append",
                 dest="buttons", help="Add button (one per button to add).")
    options, argv = p.parse_args(argv)
    if len(argv) != 2:
        print >>sys.stderr, p.get_usage()
        return 1
    
    messageText = argv[1]
    
    ap = AlertPopup(messageText)
    if options.info:
        ap.informativeText = options.info
    if options.buttons:
        for button in options.buttons:
            ap.buttons.append(button)
    
    ap.startRunLoop()
    
    return 0
    

if __name__ == '__main__':
    sys.exit(main(sys.argv))