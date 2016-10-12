#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

import importlib.util
import os
import __main__
from configparser import ConfigParser
from core import inputManager
from core import outputManager
from core import commandManager
from core import screenManager
from core import punctuationManager
from core import cursorManager
from core import applicationManager
from core import environment 
from core.settings import settings
from core import debug

class settingsManager():
    def __init__(self):
        self.settings = settings
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass
    def loadShortcuts(self, kbConfigPath=os.path.dirname(os.path.realpath(__main__.__file__)) + '/../../config/keyboard/desktop.conf'):
        kbConfig = open(kbConfigPath,"r")
        while(True):
            line = kbConfig.readline()
            if not line:
                break
            line = line.replace('\n','')
            if line.replace(" ","") == '':
                continue            
            if line.replace(" ","").startswith("#"):
                continue
            if line.count("=") != 1:
                continue
            sepLine = line.split('=')
            commandName = sepLine[1].upper()
            sepLine[0] = sepLine[0].replace(" ","")
            sepLine[0] = sepLine[0].replace("'","")
            sepLine[0] = sepLine[0].replace('"',"")
            keys = sepLine[0].split(',')
            shortcutKeys = []
            shortcutRepeat = 1
            shortcut = []
            for key in keys:
                try:
                    shortcutRepeat = int(key)
                except:
                    shortcutKeys.append(key.upper()) 
            shortcut.append(shortcutRepeat)
            shortcut.append(sorted(shortcutKeys))
            self.env['runtime']['debug'].writeDebugOut("Shortcut: "+ str(shortcut) + ' command:' +commandName ,debug.debugLevel.INFO)    
            self.env['bindings'][str(shortcut)] = commandName     
        kbConfig.close()

    def loadSoundIcons(self, soundIconPath):
        siConfig = open(soundIconPath + '/soundicons.conf',"r")
        while(True):
            line = siConfig.readline()
            if not line:
                break
            line = line.replace('\n','')
            if line.replace(" ","") == '':
                continue            
            if line.replace(" ","").startswith("#"):
                continue
            if line.count("=") != 1:
                continue
            Values = line.split('=')
            soundIcon = Values[0].upper()
            Values[1] = Values[1].replace("'","")
            Values[1] = Values[1].replace('"',"")
            soundIconFile = ''
            if os.path.exists(Values[1]):
                soundIconFile = Values[1]
            else:
                if not soundIconPath.endswith("/"):
                    soundIconPath += '/'
                if os.path.exists(soundIconPath + Values[1]):
                    soundIconFile = soundIconPath + Values[1]
            self.env['soundIcons'][soundIcon] = soundIconFile
        siConfig.close()

    def loadDicts(self, dictConfigPath=os.path.dirname(os.path.realpath(__main__.__file__)) + '/../../config/punctuation/default.conf'):
        dictConfig = open(dictConfigPath,"r")
        currDictName = ''
        while(True):
            line = dictConfig.readline()
            if not line:
                break
            line = line.replace('\n','')
            if line.replace(" ","") == '':
                continue
            if line.replace(" ","").startswith("#"):
                continue
            if line.replace(" ","").upper().startswith("[") and \
              line.replace(" ","").upper().endswith("DICT]"):
                currDictName = line[line.find('[') + 1 :line.upper().find('DICT]') + 4].upper()
            else:
                if currDictName == '':
                    continue
                if not ":===:" in line:
                    continue
                sepLine = line.split(':===:')
                if len(sepLine) == 1:
                    sepLine.append('')
                elif len(sepLine) < 1:
                    continue
                elif len(sepLine) > 2:
                    sepLine[1] = ':===:'
                self.env['punctuation'][currDictName][sepLine[0]] = sepLine[1]
                self.env['runtime']['debug'].writeDebugOut("Punctuation: " + currDictName + '.' + str(sepLine[0]) + ' :' + sepLine[1] ,debug.debugLevel.INFO)    
        dictConfig.close()

    def loadSettings(self, settingConfigPath):
        if not os.path.exists(settingConfigPath):
            return False
        self.env['settings'] = ConfigParser()
        self.env['settings'].read(settingConfigPath)
        return True

    def setSetting(self, section, setting, value):
        self.env['settings'].set(section, setting, value)

    def getSetting(self, section, setting):
        value = ''
        try:
            value = self.env['settings'].get(section, setting)
        except:
            value = str(self.settings[section][setting])
        return value

    def getSettingAsInt(self, section, setting):
        value = 0
        try:
            value = self.env['settings'].getint(section, setting)
        except:
            value = self.settings[section][setting]
        return value

    def getSettingAsFloat(self, section, setting):
        value = 0.0
        try:
            value = self.env['settings'].getfloat(section, setting)
        except:
            value = self.settings[section][setting]
        return value

    def getSettingAsBool(self, section, setting):
        value = False
        try:
            value = self.env['settings'].getboolean(section, setting)
        except:
            value = self.settings[section][setting]
        return value

    def loadDriver(self, driverName, driverType):
        if self.env['runtime'][driverType] != None:
            print('shutdown %s',driverType)
            self.env['runtime'][driverType].shutdown(self.env)    
        spec = importlib.util.spec_from_file_location(driverName, os.path.dirname(os.path.realpath(__main__.__file__)) + "/" + driverType + '/' + driverName + '.py')
        driver_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(driver_mod)
        self.env['runtime'][driverType] = driver_mod.driver()
        self.env['runtime'][driverType].initialize(self.env)           

    def shutdownDriver(self, driverType):
        if self.env['runtime'][driverType] == None:
            return
        self.env['runtime'][driverType].shutdown()
        del self.env['runtime'][driverType]          

    def setFenrirKeys(self, keys):
        keys = keys.upper()
        keyList = keys.split(',')
        for key in keyList:
            if not key in  self.env['input']['fenrirKey']:
                self.env['input']['fenrirKey'].append(key)

    def keyIDasString(self, key):
        try:
            KeyID = self.getCodeForKeyID(key)
            return str(KeyID)
        except:
            return ''

    def initFenrirConfig(self, environment = environment.environment, settingsRoot = '/etc/fenrir/', settingsFile='settings.conf'):
        environment['runtime']['debug'] = debug.debug()
        environment['runtime']['debug'].initialize(environment)
        if not os.path.exists(settingsRoot):
            if os.path.exists(os.path.dirname(os.path.realpath(__main__.__file__)) +'/../../config/'):
                settingsRoot = os.path.dirname(os.path.realpath(__main__.__file__)) +'/../../config/'
            else:
                return None
               
        environment['runtime']['settingsManager'] = self 
        environment['runtime']['settingsManager'].initialize(environment)

        validConfig = environment['runtime']['settingsManager'].loadSettings(settingsRoot + '/settings/' + settingsFile)
        if not validConfig:
            return None
        self.setFenrirKeys(self.getSetting('general','fenrirKeys'))
        if not os.path.exists(self.getSetting('keyboard','keyboardLayout')):
            if os.path.exists(settingsRoot + 'keyboard/' + self.getSetting('keyboard','keyboardLayout')):  
                self.setSetting('keyboard', 'keyboardLayout', settingsRoot + 'keyboard/' + self.getSetting('keyboard','keyboardLayout'))
                environment['runtime']['settingsManager'].loadShortcuts(self.getSetting('keyboard','keyboardLayout'))
            if os.path.exists(settingsRoot + 'keyboard/' + self.getSetting('keyboard','keyboardLayout') + '.conf'):  
                self.setSetting('keyboard', 'keyboardLayout', settingsRoot + 'keyboard/' + self.getSetting('keyboard','keyboardLayout') + '.conf')
                environment['runtime']['settingsManager'].loadShortcuts(self.getSetting('keyboard','keyboardLayout'))
        else:
            environment['runtime']['settingsManager'].loadShortcuts(self.getSetting('keyboard','keyboardLayout'))
        
        if not os.path.exists(self.getSetting('sound','theme') + '/soundicons.conf'):
            if os.path.exists(settingsRoot + 'sound/'+ self.getSetting('sound','theme')):  
                self.setSetting('sound', 'theme', settingsRoot + 'sound/'+ self.getSetting('sound','theme'))
                if os.path.exists(self.getSetting('sound','theme') + '/soundicons.conf'):  
                    environment['runtime']['settingsManager'].loadSoundIcons(self.getSetting('sound','theme'))
        else:
            environment['runtime']['settingsManager'].loadSoundIcons(self.getSetting('sound','theme'))

        if not os.path.exists(self.getSetting('general','punctuationProfile')):
            if os.path.exists(settingsRoot + 'punctuation/' + self.getSetting('general','punctuationProfile')):  
                self.setSetting('general', 'punctuationProfile', settingsRoot + 'punctuation/' + self.getSetting('general','punctuationProfile'))
                environment['runtime']['settingsManager'].loadDicts(self.getSetting('general','punctuationProfile'))
            if os.path.exists(settingsRoot + 'punctuation/' + self.getSetting('general','punctuationProfile') + '.conf'):  
                self.setSetting('general', 'punctuationProfile', settingsRoot + 'punctuation/' + self.getSetting('general','punctuationProfile') + '.conf')
                environment['runtime']['settingsManager'].loadDicts(self.getSetting('general','punctuationProfile'))
        else:
            environment['runtime']['settingsManager'].loadDicts(self.getSetting('general','punctuationProfile'))

        environment['runtime']['inputManager'] = inputManager.inputManager()
        environment['runtime']['inputManager'].initialize(environment)             
        environment['runtime']['outputManager'] = outputManager.outputManager()
        environment['runtime']['outputManager'].initialize(environment)             
        environment['runtime']['commandManager'] = commandManager.commandManager()
        environment['runtime']['commandManager'].initialize(environment)  
        environment['runtime']['punctuationManager'] = punctuationManager.punctuationManager()
        environment['runtime']['punctuationManager'].initialize(environment)  
        environment['runtime']['cursorManager'] = cursorManager.cursorManager()
        environment['runtime']['cursorManager'].initialize(environment)  
        environment['runtime']['applicationManager'] = applicationManager.applicationManager()
        environment['runtime']['applicationManager'].initialize(environment)  
        
        if environment['runtime']['screenManager'] == None:
            environment['runtime']['screenManager'] = screenManager.screenManager()
            environment['runtime']['screenManager'].initialize(environment) 
            
        environment['runtime']['debug'].writeDebugOut('\/-------environment-------\/',debug.debugLevel.ERROR)        
        environment['runtime']['debug'].writeDebugOut(str(environment),debug.debugLevel.ERROR)
        environment['runtime']['debug'].writeDebugOut('\/-------settings.conf-------\/',debug.debugLevel.ERROR)        
        environment['runtime']['debug'].writeDebugOut(str(environment['settings']._sections
),debug.debugLevel.ERROR)        
        return environment
     