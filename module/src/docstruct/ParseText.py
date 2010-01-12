'''
Created on 2010-01-03

@author: cfournie
'''

import DocumentStructure
import re
import util

DISCOURSE_CONNECTIVES = [('[,]{1} ','actually',     '[ ,.]{1}'),
                         ('[,]{1} ','afterwards',   '[ ,.]{1}'),
                         ('[,]{1} ','again',        '[ ,.]{1}'),
                         ('[,]{1} ','although',     '[ ,.]{1}'),
                         ('[,]{1} ','&',          '[ ,.]{1}'),
                         ('[,]{1} ','and',          '[ ,.]{1}'),
                         ('[,]{1} ','as a result',  '[ ,.]{1}'),
                         ('[,]{1} ','because',      '[ ,.]{1}'),
                         ('[,]{1} ','but',          '[ ,.]{1}'),
                         ('[,]{1} ','even though',  '[ ,.]{1}'),
                         ('[,]{1} ','except when',  '[ ,.]{1}'),
                         ('[,]{1} ','instead',      '[ ,.]{1}'),
                         ('[,]{1} ','for instance', '[ ,.]{1}'),
                         ('[,]{1} ','however',      '[ ,.]{1}'),
                         ('[,]{1} ','moreover',     '[ ,.]{1}'),
                         ('[,]{1} ','nonetheless',  '[ ,.]{1}'),
                         ('[,]{1} ','or',           '[ ,.]{1}'),
                         ('[,]{1} ','previously',   '[ ,.]{1}'),
                         ('[,]{1} ','since',        '[ ,.]{1}'),
                         ('[,]{1} ','then',         '[ ,.]{1}'),
                         ('[,]{1} ','when',         '[ ,.]{1}'),
                         ('[,]{1} ','yet',          '[ ,.]{1}')]

class ParseTextNunberg(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.dot          = re.compile(r'\.')
        self.multispaces  = re.compile(r'[ \n]+')
        self.spacepunct1  = re.compile(r' [,]{1}')
        self.spacepunct2  = re.compile(r' [\.]{1}')
        self.sentence     = re.compile(r'(\. [A-Z"]{1}|\.["]{1} [A-Z]{1}|\. [A-Z]{1})')
        self.clause       = re.compile(r'(\, [a-zA-Z]{1}|\,["]{1} [a-zA-Z]{1})')
        
        self.phrase = ''
        for connective in DISCOURSE_CONNECTIVES:
            self.phrase = self.phrase + '(' + connective[0] + connective[1] + connective[2] + ')*'
        
        #self.phrase       = re.compile(r'( although[ ,.]{1})*( and[ ,]{1})*( as a result[ ,]{1})*( instead[ ,]{1})*( for instance[ ,.]{1})*( but[ ,]{1})*( however[ ,.]{1})*( moreover[ ,.]{1})*')
    
    
    def handle(self, dstree, dsnode):
        value = DocumentStructure.getValue(dsnode)
        
        if len(value) != 0:
            #value = self.dot.sub('. ', value)
            value = self.multispaces.sub(' ', value)
            value = self.spacepunct1.sub(',', value)
            value = self.spacepunct2.sub('.', value)
            
            value = value.strip()
            DocumentStructure.setValue(dsnode, value)
            
            if util.getLevel(dsnode) == DocumentStructure.PARAGRAPH:
                self.__handleParagraph__(dstree, dsnode, value.strip())
    
    
    def __handleParagraph__(self, dstree, dsnode, paragraph):
        sentences = self.sentence.split(paragraph)
        
        prevItem = ''
        for i, sentence in enumerate(sentences):
            if i % 2 != 0:
                prevItem = sentence
            elif len(sentence) > 0:
                
                if len(prevItem) > 0:
                    firstLetter = prevItem[(len(prevItem) - 1)]
                    sentence = firstLetter + sentence
                    prevItem = ''
                else:
                    firstLetter = sentence[0]
                
                if sentence[(len(prevItem) - 1)] != '.':
                    sentence = sentence + '.'
                    
                if firstLetter == DocumentStructure.SYMBOL_DBLQUOTE:
                    if sentence.count(DocumentStructure.SYMBOL_DBLQUOTE) % 2 != 0:
                        sentence += firstLetter
                elif firstLetter ==  DocumentStructure.SYMBOL_SINGLEQUOTE:
                    if sentence.count(DocumentStructure.SYMBOL_SINGLEQUOTE) % 2 != 0:
                        sentence += firstLetter
                    
                    
                self.__handleTextSentence__(dstree, dsnode, sentence.strip())
            
        DocumentStructure.deleteValue(dsnode)
    
    
    def __handleTextSentence__(self, dstree, dsnode, sentence):
        clauses = self.clause.split(sentence.strip())
        
        if len(clauses) == 1:
            dstree.addNode(dsnode, DocumentStructure.TEXT_SENTENCE, value = sentence)
        else:
            dschildnode = dstree.addNode(dsnode, DocumentStructure.TEXT_SENTENCE)
            
            prevItem = ''
            for i, clause in enumerate(clauses):
                if i % 2 != 0:
                    prevItem = clause
                else:
                    if len(prevItem) > 0:
                        clause = prevItem + clause
                        prevItem = ''
                    if clause.endswith('.') == False:
                        clause = clause
                    self.__handleTextClause__(dstree, dschildnode, clause)
        
        DocumentStructure.deleteValue(dsnode)
        
    
    def __handleTextClause__(self, dstree, dsnode, clause):
        phrases = re.split(self.phrase, clause.strip())
        
        if len(phrases) == 1:
            dstree.addNode(dsnode, DocumentStructure.TEXT_CLAUSE, value = clause)
        else:
            dschildnode = dstree.addNode(dsnode, DocumentStructure.TEXT_CLAUSE)
            for phrase in phrases:
                if phrase != None:
                    phrase = phrase.strip()
                    if len(phrase) > 0:
                        self.__handleTextPhrase__(dstree, dschildnode, phrase.strip())
        
        DocumentStructure.deleteValue(dsnode)
    
    
    def __handleTextPhrase__(self, dstree, dsnode, phrase):
            dstree.addNode(dsnode, DocumentStructure.TEXT_PHRASE, value = phrase)
        