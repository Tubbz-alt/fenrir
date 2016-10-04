#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug

def getPrevWord(currX,currY, currText):
    if currText == '':
        return -1, -1, ''
    x, y, currWord = getCurrentWord(currX,currY,currText)
    wrappedLines = currText.split('\n') 
    if (currWord == ''):
        return currX, currY, '' 
    while True:
        if x < 2:
            if y != 0:
                y -= 1
            else:
                 return currX, currY, '' 
            x = len(wrappedLines[y]) - 1
        else:
            x -= 1
        if wrappedLines[y] != '':
            break
    x, y, currWord = getCurrentWord(x, y, currText)
    if currWord == '':
        return currX, currY, ''
    return x, y, currWord

def getCurrentWord(currX,currY, currText):
    if currText == '':
        return -1, -1, ''
    x = currX
    y = currY
    wrappedLines = currText.split('\n')
    wordFound = False
    currWord = ''
    currLine = wrappedLines[y].replace("\t"," ")
    if currLine[x] == ' ' and  x > 1:
        x = x - 2
    while not wordFound:
        x = currLine[:x].rfind(" ")
        if x == -1:
            x = 0
        else:
            x += 1
        wordEnd = currLine[x + 1:].find(" ")
        if wordEnd == -1:
            wordEnd = len(currLine)
        else:
            wordEnd += x + 1
        currWord = currLine[x:wordEnd]
        wordFound = currWord.strip(" \t\n") != ''
        if wordFound:
            break
        if x == 0:
            if y != 0:
                y -= 1
                currLine = wrappedLines[y].replace("\t"," ")
            else:
                 return currX, currY, '' 
            x = len(wrappedLines[y]) - 1
        else:
            x -= 1
    return x, y, currWord

def getNextWord(currX,currY, currText):
    if currText == '':
        return -1, -1, ''
    x = currX
    y = currY
    wrappedLines = currText.split('\n')
    wordFound = False
    currWord = ''
    currLine = wrappedLines[y].replace("\t"," ")
    while not wordFound:
        xtmp = 0
        if  x + 1 >= len(currLine):
            if y < len(wrappedLines):
                y += 1
                currLine = wrappedLines[y].replace("\t"," ")
            else:
                 return currX, currY, '' 
            x = 0
        else:
            x += 1
            xtmp = x    
            x = currLine[x:].find(" ")          
        if x == -1:
            x = len(currLine)
            continue
        else:
            if xtmp != 0:
              xtmp += 1
            x += xtmp
        if x + 1 < len(currLine):
            wordEnd = currLine[x + 1:].find(" ")
        else:
            wordEnd = -1
        if wordEnd == -1:
            wordEnd = len(currLine)
        else:
            wordEnd += x + 1
        if wordEnd >= len(currLine) and y + 1 >= len(wrappedLines):
            return currX, currY, ''
        currWord = currLine[x:wordEnd]
        wordFound = currWord.strip(" \t\n") != ''
        if not wordFound:
            x = wordEnd
    return x, y, currWord
