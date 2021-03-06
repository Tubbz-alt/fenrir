#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass
    def getDescription(self):
        return 'No Description found'   

    def run(self):
        return
        if not self.env['runtime']['settingsManager'].getSettingAsBool('review', 'leaveReviewOnKeypress'):
            return
        if not self.env['runtime']['inputManager'].noKeyPressed():
            return
        if self.env['runtime']['screenManager'].isScreenChange():
            return
        if len(self.env['input']['prevDeepestInput']) > len(self.env['input']['currInput']):
            return
        self.env['runtime']['cursorManager'].clearReviewCursor()

    def setCallback(self, callback):
        pass

