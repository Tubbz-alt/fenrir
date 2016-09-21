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
        return 'exits review mode'        
    
    def run(self):
        if not (self.env['screenData']['oldCursorReview']) and \
          (self.env['screenData']['newCursorReview']):
            self.env['runtime']['outputManager'].presentText("Not in review mode", interrupt=True)
            return  

        self.env['screenData']['oldCursorReview'] = None
        self.env['screenData']['newCursorReview'] = None
        self.env['runtime']['outputManager'].presentText("leve review mode", interrupt=True)
   
    def setCallback(self, callback):
        pass
