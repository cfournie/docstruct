'''
Created on 2009-12-29

@author: cfournie
'''

import util
import DocumentStructure
from lxml import etree


IGNORE       = 'ignore'
IGNORE_TRUE  = 'true'
IGNORE_FALSE = 'false'

ABBR       = 'abbrFound'
ABBR_TRUE  = 'true'
ABBR_FALSE = 'false'


class _ParseXHTML_Abstract(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
    def handleReplace(self, dstree, dsnode, value):
        util.appendToValue(dsnode, value)
        
        
    def handleReplaceQuoted(self, dstree, dsnode, value):
        util.appendToValue(dsnode, value)
    

class _ParseXHTML_Base(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        ''' 
        self.abstractHandler      = _ParseXHTML_Abstract()
        self.peudodsnode          = None
        self.peudodsnodereplace   = None
        self.peudoTrigger         = False
        self.preInsertedParagraph = False
        
    
    def handle(self, xmltree, xmlnode, dstree, dsnode):
        # Determine whether to ignore
        if xmlnode.get(IGNORE) == IGNORE_TRUE:
            return dsnode
            
        if xmlnode.getparent() != None:
            parentTag = util.getTag(xmlnode.getparent())
            
            if self.peudodsnode != None and parentTag != 'p':
                self.peudoTrigger = True
                dsnode = self.peudodsnode
            
        # Process tag
        tag = util.getTag(xmlnode)
        
        if tag == 'em':
            return self.__handle_em__(xmlnode, dstree, dsnode)
        
        elif tag == 'html':
            return self.__handle_html__(xmlnode, dstree, dsnode)
            
        elif tag == 'title':
            return self.__handle_title__(xmlnode, dstree, dsnode)
        
        elif tag == 'abbr':
            return self.__handle_abbr__(xmlnode, dstree, dsnode)
        
        elif tag == 'acronym':
            return self.__handle_acronym__(xmlnode, dstree, dsnode)
        
        elif tag == 'address':
            return self.__handle_address__(xmlnode, dstree, dsnode)
            
        elif tag == 'blockquote':
            return self.__handle_blockquote__(xmlnode, dstree, dsnode)
        
        elif tag == 'br':
            return self.__handle_br__(xmlnode, dstree, dsnode)
        
        elif tag == 'cite':
            return self.__handle_cite__(xmlnode, dstree, dsnode)
            
        elif tag == 'dfn':
            return self.__handle_dfn__(xmlnode, dstree, dsnode)
            
        elif tag == 'em':
            return self.__handle_em__(xmlnode, dstree, dsnode)
            
        elif tag == 'h1':
            return self.__handle_h1__(xmlnode, dstree, dsnode)
            
        elif tag == 'h2':
            return self.__handle_h2__(xmlnode, dstree, dsnode)
            
        elif tag == 'h3':
            return self.__handle_h3__(xmlnode, dstree, dsnode)
            
        elif tag == 'h4':
            return self.__handle_h4__(xmlnode, dstree, dsnode)
            
        elif tag == 'h5':
            return self.__handle_h5__(xmlnode, dstree, dsnode)
            
        elif tag == 'h6':
            return self.__handle_h6__(xmlnode, dstree, dsnode)
            
        elif tag == 'kbd':
            return self.__handle_kbd__(xmlnode, dstree, dsnode)
            
        elif tag == 'p':
            return self.__handle_p__(xmlnode, dstree, dsnode)
        
        elif tag == 'pre':
            return self.__handle_pre__(xmlnode, dstree, dsnode)
            
        elif tag == 'q':
            return self.__handle_q__(xmlnode, dstree, dsnode)
            
        elif tag == 'samp':
            return self.__handle_samp__(xmlnode, dstree, dsnode)
            
        elif tag == 'span':
            return self.__handle_span__(xmlnode, dstree, dsnode)
            
        elif tag == 'strong':
            return self.__handle_strong__(xmlnode, dstree, dsnode)
            
        elif tag == 'var':
            return self.__handle_var__(xmlnode, dstree, dsnode)
            
        elif tag == 'a':
            return self.__handle_a__(xmlnode, dstree, dsnode)
            
        elif tag == 'dl':
            return self.__handle_dl__(xmlnode, dstree, dsnode)
            
        elif tag == 'dt':
            return self.__handle_dt__(xmlnode, dstree, dsnode)
            
        elif tag == 'dd':
            return self.__handle_dd__(xmlnode, dstree, dsnode)
            
        elif tag == 'ol':
            return self.__handle_ol__(xmlnode, dstree, dsnode)
            
        elif tag == 'ul':
            return self.__handle_ul__(xmlnode, dstree, dsnode)
            
        elif tag == 'li':
            return self.__handle_li__(xmlnode, dstree, dsnode)
            
        elif tag == 'b':
            return self.__handle_b__(xmlnode, dstree, dsnode)
            
        elif tag == 'big':
            return self.__handle_big__(xmlnode, dstree, dsnode)
            
        elif tag == 'i':
            return self.__handle_i__(xmlnode, dstree, dsnode)
            
        elif tag == 'small':
            return self.__handle_small__(xmlnode, dstree, dsnode)
            
        elif tag == 'sub':
            return self.__handle_sub__(xmlnode, dstree, dsnode)
            
        elif tag == 'sup':
            return self.__handle_sup__(xmlnode, dstree, dsnode)
            
        elif tag == 'tt':
            return self.__handle_tt__(xmlnode, dstree, dsnode)
            
        elif tag == 'del':
            return self.__handle_del__(xmlnode, dstree, dsnode)
        
        elif tag == 'ins':
            return self.__handle_ins__(xmlnode, dstree, dsnode)
            
        elif tag == 'caption':
            return self.__handle_caption__(xmlnode, dstree, dsnode)
            
        elif tag == 'table':
            return self.__handle_table__(xmlnode, dstree, dsnode)
            
        elif tag == 'img':
            return self.__handle_img__(xmlnode, dstree, dsnode)
        
        elif tag == 'tr':
            # Ignore subtree
            xmlchildtree = etree.ElementTree(xmlnode)
            for xmlchildnode in xmlchildtree.iter(tag=etree.Element):
                xmlchildnode.set(IGNORE, IGNORE_TRUE)
            return dsnode
        
        else:
            return dsnode
    
    
    def prepareNode(self, dstree, dsnode, level, indent = None):
        curLevel     = util.levelToInt(DocumentStructure.getLevel(dsnode))
        levelAbove   = util.levelToInt(util.levelAbove(level))
        levelDesired = util.levelToInt(level)
        
        if curLevel >= levelAbove:
            while curLevel > levelAbove:
                newLevel = util.levelBelow(DocumentStructure.getLevel(dsnode))
                dsnode = dstree.addNode(dsnode, level = newLevel, indent = indent)
                curLevel = util.levelToInt(DocumentStructure.getLevel(dsnode))
                
            if level == DocumentStructure.PARAGRAPH:
                self.preInsertedParagraph = True
                dsnode = dstree.addNode(dsnode, level = DocumentStructure.PARAGRAPH, indent = indent)
            else:
                self.preInsertedParagraph = False
                
        elif curLevel < levelAbove:
            while curLevel < levelDesired:
                dsnode = dsnode.getparent()
                curLevel = util.levelToInt(DocumentStructure.getLevel(dsnode))
                
            if level != DocumentStructure.PARAGRAPH:
                dsnode = dsnode.getparent()
                
            DocumentStructure.setIndent(dsnode, indent)
                
        return dsnode
    
    
    def isIndent(self, xmlnode):
        tag = util.getTag(xmlnode)
        return tag == 'blockquote'
    
    
    def handleIndent(self, dsnode, xmlnode):
        indent = DocumentStructure.getIndent(xmlnode)
        DocumentStructure.setIndent(dsnode, indent)
        return dsnode
    
    
    def __handle_body__(self, xmlnode, dstree, dsnode):
        dsnode = self.prepareNode(dstree, dsnode, DocumentStructure.PARAGRAPH)
        self.abstractHandler.handleReplace(dstree, dsnode, util.parseValueFrom(xmlnode))
        return dsnode
    

    def __handle_html__(self, xmlnode, dstree, dsnode):
        xmllang = None
        if None in xmlnode.nsmap:
            xmllang = '{' + xmlnode.nsmap[None] + '}lang'
        
        if 'lang' in xmlnode.attrib:
            dstree.setLang(xmlnode.attrib['lang'])
        elif xmllang != None and xmllang in xmlnode.attrib:
            dstree.setLang(xmlnode.attrib[xmllang])
        
        return dsnode
    
    
    def __handle_title__(self, xmlnode, dstree, dsnode):
        # Assumes document node
        if DocumentStructure.getLevel(dsnode) != DocumentStructure.DOCUMENT:
            raise Exception, "Unexpected level" 
        
        DocumentStructure.setNode(dsnode, value=util.parseValueFrom(xmlnode))
        return dsnode
    
    
    def __handle_abbr__(self, xmlnode, dstree, dsnode):
        # Tag subtree as ABBR
        xmlchildtree = etree.ElementTree(xmlnode)
        xmlchildlastnode = None
        for xmlchildnode in xmlchildtree.iter(tag=etree.Element):
            xmlchildnode.set(ABBR, ABBR_TRUE)
            xmlchildlastnode = xmlchildnode
        xmlchildlastnode.set(ABBR, ABBR_FALSE)
                
        dsnode = self.prepareNode(dstree, dsnode, DocumentStructure.PARAGRAPH)
        self.abstractHandler.handleReplace(dstree, dsnode, util.parseValueFrom(xmlnode) + ' ')
        return self.handleIndent(dsnode, xmlnode)
    
    
    def __handle_acronym__(self, xmlnode, dstree, dsnode):
        dsnode = self.prepareNode(dstree, dsnode, DocumentStructure.PARAGRAPH)
        self.abstractHandler.handleReplace(dstree, dsnode, util.parseValueFrom(xmlnode))
        return self.handleIndent(dsnode, xmlnode)
    
    
    def __handle_address__(self, xmlnode, dstree, dsnode):
        dsnode = self.prepareNode(dstree, dsnode, DocumentStructure.PARAGRAPH)
        self.abstractHandler.handleReplace(dstree, dsnode, util.parseValueFrom(xmlnode))
        return self.handleIndent(dsnode, xmlnode)
    
    
    def __handle_blockquote__(self, xmlnode, dstree, dsnode):
        # Ignore inner value, text data is not allowed
        valueTail = xmlnode.tail
        
        # Encounter paragraph data assumed to be without a pre-inserted p entry
        if valueTail != None and len(valueTail.strip()) > 0:
            dsnodeParent = dsnode
            if util.getLevel(dsnodeParent) != util.levelAbove(DocumentStructure.PARAGRAPH):
                dsnodeParent = util.getparent(dstree, dsnode)
            self.peudodsnode = dstree.addNode(dsnodeParent, DocumentStructure.PARAGRAPH, value = valueTail)
            self.peudodsnodereplace = dsnode
        
        return dsnode
    
    
    def __handle_br__(self, xmlnode, dstree, dsnode):
        dsnode = self.prepareNode(dstree, dsnode, DocumentStructure.PARAGRAPH)
        self.abstractHandler.handleReplace(dstree, dsnode, util.parseValueFrom(xmlnode))
        return self.handleIndent(dsnode, xmlnode)
    
    
    def __handle_cite__(self, xmlnode, dstree, dsnode):
        dsnode = self.prepareNode(dstree, dsnode, DocumentStructure.PARAGRAPH)
        self.abstractHandler.handleReplace(dstree, dsnode, util.parseValueFrom(xmlnode))
        return self.handleIndent(dsnode, xmlnode)
    
    
    def __handle_dfn__(self, xmlnode, dstree, dsnode):
        dsnode = self.prepareNode(dstree, dsnode, DocumentStructure.PARAGRAPH)
        self.abstractHandler.handleReplace(dstree, dsnode, util.parseValueFrom(xmlnode))
        return self.handleIndent(dsnode, xmlnode)
    
    
    def __handle_em__(self, xmlnode, dstree, dsnode):
        dsnode = self.prepareNode(dstree, dsnode, DocumentStructure.PARAGRAPH)
        self.abstractHandler.handleReplace(dstree, dsnode, util.parseValueFrom(xmlnode))
        return self.handleIndent(dsnode, xmlnode)
    
    
    def __handle_h1__(self, xmlnode, dstree, dsnode):
        level = DocumentStructure.SECTION_L1
        value = util.parseValueFrom(xmlnode)
        dsnode = self.prepareNode(dstree, dsnode, level)
        dsnode = dstree.addNode(dsnode, level, value = value)
        return self.handleIndent(dsnode, xmlnode)
    
    
    def __handle_h2__(self, xmlnode, dstree, dsnode):
        level = DocumentStructure.SECTION_L2
        value = util.parseValueFrom(xmlnode)
        dsnode = self.prepareNode(dstree, dsnode, level)
        dsnode = dstree.addNode(dsnode, level, value = value)
        return self.handleIndent(dsnode, xmlnode)
    
    
    def __handle_h3__(self, xmlnode, dstree, dsnode):
        level = DocumentStructure.SECTION_L3
        value = util.parseValueFrom(xmlnode)
        dsnode = self.prepareNode(dstree, dsnode, level)
        dsnode = dstree.addNode(dsnode, level, value = value)
        return self.handleIndent(dsnode, xmlnode)
    
    
    def __handle_h4__(self, xmlnode, dstree, dsnode):
        level = DocumentStructure.SECTION_L4
        value = util.parseValueFrom(xmlnode)
        dsnode = self.prepareNode(dstree, dsnode, level)
        dsnode = dstree.addNode(dsnode, level, value = value)
        return self.handleIndent(dsnode, xmlnode)
    
    
    def __handle_h5__(self, xmlnode, dstree, dsnode):
        level = DocumentStructure.SECTION_L5
        value = util.parseValueFrom(xmlnode)
        dsnode = self.prepareNode(dstree, dsnode, level)
        dsnode = dstree.addNode(dsnode, level, value = value)
        return self.handleIndent(dsnode, xmlnode)
    
    
    def __handle_h6__(self, xmlnode, dstree, dsnode):
        level = DocumentStructure.SECTION_L6
        value = util.parseValueFrom(xmlnode)
        dsnode = self.prepareNode(dstree, dsnode, level)
        dsnode = dstree.addNode(dsnode, level, value = value)
        return self.handleIndent(dsnode, xmlnode) 
    
    
    def __handle_kbd__(self, xmlnode, dstree, dsnode):
        dsnode = self.prepareNode(dstree, dsnode, DocumentStructure.PARAGRAPH)
        self.abstractHandler.handleReplaceQuoted(dstree, dsnode, util.parseQuotedValueFrom(xmlnode))
        return self.handleIndent(dsnode, xmlnode)
    
    
    def __handle_p__(self, xmlnode, dstree, dsnode):
        # End a pseudo-p trigger
        if self.peudoTrigger == True:
            self.peudoTrigger = False
            dsnode = self.peudodsnodereplace
            self.peudodsnodereplace = None
            self.peudodsnode = None
        
        valueText = xmlnode.text
        valueTail = xmlnode.tail
        
        if valueText != None:
            valueText = valueText.strip()
        if valueTail != None:
            valueTail = valueTail.strip()
        
        # Encounter a p tag with a pre-inserted p entry
        if self.preInsertedParagraph == True:
            dsnode = self.prepareNode(dstree, dsnode, DocumentStructure.PARAGRAPH)
            self.abstractHandler.handleReplace(dstree, dsnode, valueText)
            
        # Encounter a p tag without a pre-inserted p entry
        else:
            dsnode = self.prepareNode(dstree, dsnode, DocumentStructure.PARAGRAPH)
                
            if self.preInsertedParagraph != True:
                dsnode = self.prepareNode(dstree, dsnode, DocumentStructure.PARAGRAPH)
                dsnode = util.getparent(dstree, dsnode)
                dsnode = dstree.addNode(dsnode, level = DocumentStructure.PARAGRAPH, value = valueText)
            else:
                self.abstractHandler.handleReplace(dstree, dsnode, valueText)
                    
            self.preInsertedParagraph = False
                        
        # Encounter a p tag without a pre-inserted p entry
        if valueTail != None and len(valueTail.strip()) > 0:
            dsnodeParent = dsnode
            if util.getLevel(dsnodeParent) != util.levelAbove(DocumentStructure.PARAGRAPH):
                dsnodeParent = util.getparent(dstree, dsnode)
            self.peudodsnode = dstree.addNode(dsnodeParent, DocumentStructure.PARAGRAPH, value = valueTail)
            self.peudodsnodereplace = dsnode
            
        return self.handleIndent(dsnode, xmlnode)
    
    
    def __handle_pre__(self, xmlnode, dstree, dsnode):
        dsnode = self.prepareNode(dstree, dsnode, DocumentStructure.PARAGRAPH)
        self.abstractHandler.handleReplace(dstree, dsnode, util.parseValueFrom(xmlnode))
        return self.handleIndent(dsnode, xmlnode)
    
    
    def __handle_q__(self, xmlnode, dstree, dsnode):
        dsnode = self.prepareNode(dstree, dsnode, DocumentStructure.PARAGRAPH)
        self.abstractHandler.handleReplaceQuoted(dstree, dsnode, util.parseQuotedValueFrom(xmlnode))
        return self.handleIndent(dsnode, xmlnode)
    
    
    def __handle_samp__(self, xmlnode, dstree, dsnode):
        dsnode = self.prepareNode(dstree, dsnode, DocumentStructure.PARAGRAPH)
        self.abstractHandler.handleReplaceQuoted(dstree, dsnode, util.parseQuotedValueFrom(xmlnode))
        return self.handleIndent(dsnode, xmlnode)
    
    
    def __handle_span__(self, xmlnode, dstree, dsnode):
        dsnode = self.prepareNode(dstree, dsnode, DocumentStructure.PARAGRAPH)
        self.abstractHandler.handleReplace(dstree, dsnode, util.parseValueFrom(xmlnode))
        return self.handleIndent(dsnode, xmlnode)
    
    
    def __handle_strong__(self, xmlnode, dstree, dsnode):
        dsnode = self.prepareNode(dstree, dsnode, DocumentStructure.PARAGRAPH)
        self.abstractHandler.handleReplace(dstree, dsnode, util.parseValueFrom(xmlnode))
        return self.handleIndent(dsnode, xmlnode)
    
    
    def __handle_var__(self, xmlnode, dstree, dsnode):
        dsnode = self.prepareNode(dstree, dsnode, DocumentStructure.PARAGRAPH)
        self.abstractHandler.handleReplaceQuoted(dstree, dsnode, util.parseQuotedValueFrom(xmlnode))
        return self.handleIndent(dsnode, xmlnode)
    
    
    def __handle_a__(self, xmlnode, dstree, dsnode):
        value = util.parseValueFrom(xmlnode)
        if xmlnode.get(ABBR) != ABBR_TRUE:
            value = value + ' '
        
        self.abstractHandler.handleReplace(dstree, dsnode, value)
        return self.handleIndent(dsnode, xmlnode)
    
    
    def __handle_dl__(self, xmlnode, dstree, dsnode):
        level = DocumentStructure.TEXT_SENTENCE
        dsnode = self.prepareNode(dstree, dsnode, level)
        dsnode = dstree.addNode(dsnode, level)
        return self.handleIndent(dsnode, xmlnode)
    
    
    def __handle_dt__(self, xmlnode, dstree, dsnode):
        level = DocumentStructure.TEXT_CLAUSE
        value = util.parseValueFrom(xmlnode)
        dsnode = self.prepareNode(dstree, dsnode, level)
        dsnode = dstree.addNode(dsnode, level, value = value)
        return self.handleIndent(dsnode, xmlnode)
    
    
    def __handle_dd__(self, xmlnode, dstree, dsnode):
        level = DocumentStructure.TEXT_CLAUSE
        value = util.parseValueFrom(xmlnode)
        dsnode = self.prepareNode(dstree, dsnode, level)
        dsnode = dstree.addNode(dsnode, level, value = value)
        return self.handleIndent(dsnode, xmlnode)
    
    
    def __handle_ol__(self, xmlnode, dstree, dsnode):
        level = DocumentStructure.TEXT_SENTENCE
        dsnode = self.prepareNode(dstree, dsnode, level)
        dsnode = dstree.addNode(dsnode, level)
        return self.handleIndent(dsnode, xmlnode)
    
    
    def __handle_ul__(self, xmlnode, dstree, dsnode):
        level = DocumentStructure.TEXT_SENTENCE
        dsnode = self.prepareNode(dstree, dsnode, level)
        dsnode = dstree.addNode(dsnode, level)
        return self.handleIndent(dsnode, xmlnode)
    
    
    def __handle_li__(self, xmlnode, dstree, dsnode):
        level = DocumentStructure.TEXT_CLAUSE
        value = util.parseValueFrom(xmlnode)
        dsnode = self.prepareNode(dstree, dsnode, level)
        dsnode = dstree.addNode(dsnode, level, value = value)
        return self.handleIndent(dsnode, xmlnode)
    
    
    def __handle_b__(self, xmlnode, dstree, dsnode):
        dsnode = self.prepareNode(dstree, dsnode, DocumentStructure.PARAGRAPH)
        self.abstractHandler.handleReplace(dstree, dsnode, util.parseValueFrom(xmlnode))
        return self.handleIndent(dsnode, xmlnode)
    
    
    def __handle_big__(self, xmlnode, dstree, dsnode):
        dsnode = self.prepareNode(dstree, dsnode, DocumentStructure.PARAGRAPH)
        self.abstractHandler.handleReplace(dstree, dsnode, util.parseValueFrom(xmlnode))
        return self.handleIndent(dsnode, xmlnode)
    
    
    def __handle_i__(self, xmlnode, dstree, dsnode):
        dsnode = self.prepareNode(dstree, dsnode, DocumentStructure.PARAGRAPH)
        self.abstractHandler.handleReplace(dstree, dsnode, util.parseValueFrom(xmlnode))
        return self.handleIndent(dsnode, xmlnode)
    
    
    def __handle_small__(self, xmlnode, dstree, dsnode):
        dsnode = self.prepareNode(dstree, dsnode, DocumentStructure.PARAGRAPH)
        self.abstractHandler.handleReplace(dstree, dsnode, util.parseValueFrom(xmlnode))
        return self.handleIndent(dsnode, xmlnode)
    
    
    def __handle_sub__(self, xmlnode, dstree, dsnode):
        dsnode = self.prepareNode(dstree, dsnode, DocumentStructure.PARAGRAPH)
        self.abstractHandler.handleReplace(dstree, dsnode, util.parseValueFrom(xmlnode))
        return self.handleIndent(dsnode, xmlnode)
    
    
    def __handle_sup__(self, xmlnode, dstree, dsnode):
        dsnode = self.prepareNode(dstree, dsnode, DocumentStructure.PARAGRAPH)
        self.abstractHandler.handleReplace(dstree, dsnode, util.parseValueFrom(xmlnode))
        return self.handleIndent(dsnode, xmlnode)
    
    
    def __handle_tt__(self, xmlnode, dstree, dsnode):
        dsnode = self.prepareNode(dstree, dsnode, DocumentStructure.PARAGRAPH)
        self.abstractHandler.handleReplace(dstree, dsnode, util.parseValueFrom(xmlnode))
        return self.handleIndent(dsnode, xmlnode)
    
    
    def __handle_del__(self, xmlnode, dstree, dsnode):
        dsnode = self.prepareNode(dstree, dsnode, DocumentStructure.PARAGRAPH)
        
        # Ignore the inner data of xmlnode.text because it has been deleted
        valueTail = xmlnode.tail
        
        self.abstractHandler.handleReplace(dstree, dsnode, valueTail)
        return self.handleIndent(dsnode, xmlnode)
    
    
    def __handle_ins__(self, xmlnode, dstree, dsnode):
        dsnode = self.prepareNode(dstree, dsnode, DocumentStructure.PARAGRAPH)
        self.abstractHandler.handleReplace(dstree, dsnode, util.parseValueFrom(xmlnode))
        return self.handleIndent(dsnode, xmlnode)
    
    
    def __handle_caption__(self, xmlnode, dstree, dsnode):
        dsnode = self.prepareNode(dstree, dsnode, DocumentStructure.PARAGRAPH)
        value = util.parseValueFrom(xmlnode)
        
        if DocumentStructure.getLevel(dsnode) == DocumentStructure.PARAGRAPH:
            value = util.ensureEndsInPeriod(value)
                
        self.abstractHandler.handleReplace(dstree, dsnode, value)
        return self.handleIndent(dsnode, xmlnode)
    
    
    def __handle_table__(self, xmlnode, dstree, dsnode):
        if 'summary' in xmlnode.attrib:
            value = xmlnode.attrib['summary']
            dsnode = self.prepareNode(dstree, dsnode, DocumentStructure.PARAGRAPH)
            
            if DocumentStructure.getLevel(dsnode) == DocumentStructure.PARAGRAPH:
                value = util.ensureEndsInPeriod(value)
            
            util.appendToValue(dsnode, ' ' + value + ' ')
        
        return self.handleIndent(dsnode, xmlnode)
    
    
    def __handle_img__(self, xmlnode, dstree, dsnode):
        value = ''
        
        if 'alt' in xmlnode.attrib:
            value = xmlnode.attrib['alt']
        elif 'title' in xmlnode.attrib:
            value = xmlnode.attrib['title']
        
        dsnode = self.prepareNode(dstree, dsnode, DocumentStructure.PARAGRAPH)
        
        if DocumentStructure.getLevel(dsnode) == DocumentStructure.PARAGRAPH:
            value = util.ensureEndsInPeriod(value)
        
        util.appendToValue(dsnode, ' ' + value + ' ')
        return self.handleIndent(dsnode, xmlnode)
    

class ParseXHTML10(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.base = _ParseXHTML_Base()
    
    
    def handle(self, xmltree, xmlnode, dstree, dsnode):
        return self.base.handle(xmltree, xmlnode, dstree, dsnode)
    
    def isIndent(self, xmlnode):
        return self.base.isIndent(xmlnode)


class ParseXHTML11(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.base = ParseXHTML10()
    
    
    def handle(self, xmltree, xmlnode, dstree, dsnode):
        return self.base.handle(xmltree, xmlnode, dstree, dsnode)
    
    def isIndent(self, xmlnode):
        return self.base.isIndent(xmlnode)