'''
Created on 2010-01-06

@author: cfournie
'''

import re
import DocumentStructure


def getTag(element):
    prefix = re.compile(r'[\{]{1}[a-zA-Z0-9/:.]+[\}]{1}')
    # Remove namespace
    return prefix.sub('', element.tag).lower()


def getLevel(dsnode):
    return DocumentStructure.getLevel(dsnode)


def levelToInt(level):
    return DocumentStructure.LEVELS.index(level)


def intToLevel(int):
    return DocumentStructure.LEVELS[int]


def levelAbove(level):
    intLevel = levelToInt(level)
    return intToLevel(intLevel + 1)


def levelBelow(level):
    intLevel = levelToInt(level)
    return intToLevel(intLevel - 1)


def parseValueFrom(node):
    value = ''
    
    if node.text != None:
        value = node.text
        
    if node.tail != None:
        value = value + ' ' + node.tail
        
    return value.strip()


def parseQuotedValueFrom(node):
    value = ''
    
    if node.text != None:
        value = DocumentStructure.SYMBOL_QUOTE + node.text + DocumentStructure.SYMBOL_QUOTE
        
    if node.tail != None:
        value = value + ' ' + node.tail
        
    return value.strip()

    
def appendToValue(dsnode, value):
    newValue = DocumentStructure.getValue(dsnode)
    
    if value != None:
        if newValue != None:
            # Ensure a space is added between tags
            newValue = newValue + ' ' + value
        else:
            newValue = value
        
    DocumentStructure.setNode(dsnode, value = newValue)
    


def ensureEndsInPeriod(value):
    if value.endswith('.') == False:
        value = value + '.'
    return value
    
    
def getparent(dstree, dsnode):
    parent = dsnode.getparent()
    if parent == None:
        parent = dstree.getroot()
    return parent