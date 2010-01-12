'''
Created on 2010-01-03

@author: cfournie
'''

import os
import sys


from docstruct.DocumentStructure import DocStructTreeParser
from lxml import etree

class DocStructParser(object):
    '''
    classdocs
    '''
    #docStructs = list()


    def __init__(self, inputDir, outputDir):
        '''
        Constructor
        '''
        self.inputDir   = inputDir
        self.outputDir  = outputDir
        self.treeParser = DocStructTreeParser()
        self.logfile    = None
        
    
    def parse(self):
        i = 0
        for root, dirs, files in os.walk(self.inputDir):
            for file in files:
                i = i + 1
                
                xmltree = None
                dstree  = None
                
                try:
                    xmltree, dstree = self.treeParser.parse(os.path.join(root, file))
                except etree.XMLSyntaxError:
                    if self.logfile == None:
                        self.logfile = open('error.log', 'w+')
                    self.logfile.write("XHTML Syntax Error detected, file skipped: " + str(os.path.join(root, file)))
                else:
                    (shortname, extension) = os.path.splitext(file)
                    
                    # output diagnostic html renders
                    #self.treeParser.outputImage(xmltree, os.path.join(self.outputDir, str(i) + '_' + 'html' + '_' + shortname + '.png'))
                    #self.treeParser.outputXML(xmltree, os.path.join(self.outputDir, str(i) + '_' + 'html'+ '_' + shortname + '.xml'))
                    #self.treeParser.outputDOT(xmltree, os.path.join(self.outputDir, str(i) + '_' + 'html' + '_' + shortname + '.dot'))
                    
                    # output diagnostic DS renders
                    #self.treeParser.outputImage(dstree, os.path.join(self.outputDir, str(i) + '_' + 'ds' + '_' + shortname + '.png'))
                    self.treeParser.outputXML(dstree, os.path.join(self.outputDir, str(i) + '_' + 'ds' + '_' + shortname + '.xml'))
                    #self.treeParser.outputDOT(dstree, os.path.join(self.outputDir, str(i) + '_' + 'ds' + '_' + shortname + '.dot'))
