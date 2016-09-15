#!/bin/python
import fcntl
import sys
import termios


class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        return environment
    def shutdown(self, environment):
        return environment 
    def getDescription(self):
        return 'selects the previous clipboard'        
    def run(self, environment):
        if len(environment['commandBuffer']['clipboard']) == 0:
            environment['runtime']['outputManager'].presentText(environment, 'clipboard empty', interrupt=True)
            return environment 
        environment['commandBuffer']['currClipboard'] -= 1
        if environment['commandBuffer']['currClipboard'] < 0:
            environment['commandBuffer']['currClipboard'] = len(environment['commandBuffer']['clipboard']) -1
            environment['runtime']['outputManager'].presentText(environment, 'Last clipboard ', interrupt=True)            
            environment['runtime']['outputManager'].presentText(environment, environment['commandBuffer']['clipboard'][environment['commandBuffer']['currClipboard']], interrupt=False)            
        else:
            environment['runtime']['outputManager'].presentText(environment, environment['commandBuffer']['clipboard'][environment['commandBuffer']['currClipboard']], interrupt=True)
        return environment                
    def setCallback(self, callback):
        pass
