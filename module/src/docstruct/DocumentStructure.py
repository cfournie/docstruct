'''
Created on 2009-12-29

@author: cfournie
'''

import math
import util


from lxml import etree,html
from ParseXHTML import ParseXHTML10,ParseXHTML11
from ParseText import ParseTextNunberg
from igraph import Graph,plot


LEVELS = ('text-phrase',
          'text-clause',
          'text-sentence',
          'paragraph',
          'section-l6',
          'section-l5',
          'section-l4',
          'section-l3',
          'section-l2',
          'section-l1',
          'document')

TEXT_PHRASE     = LEVELS[0]
TEXT_CLAUSE     = LEVELS[1]
TEXT_SENTENCE   = LEVELS[2]
PARAGRAPH       = LEVELS[3]
SECTION_L6      = LEVELS[4]
SECTION_L5      = LEVELS[5]
SECTION_L4      = LEVELS[6]
SECTION_L3      = LEVELS[7]
SECTION_L2      = LEVELS[8]
SECTION_L1      = LEVELS[9]
DOCUMENT        = LEVELS[10]

XHTML_10_ID = '-//W3C//DTD XHTML 1.0'
XHTML_11_ID = '-//W3C//DTD XHTML 1.1'
XHTML_20_ID = '-//W3C//DTD XHTML 2.0'
HTML_50_ID = '-//W3C//DTD HTML 5'

SYMBOL_DBLQUOTE    = '"'
SYMBOL_SINGLEQUOTE = '\''
SYMBOL_QUOTE       = SYMBOL_DBLQUOTE


class DocStructTreeParser(object):
    
    def __init__(self):
        self.xmlparser = html.XHTMLParser(attribute_defaults = True,
                                          dtd_validation = True,
                                          load_dtd = True,
                                          no_network = False,
                                          ns_clean = True,
                                          recover = False,
                                          remove_blank_text = True,
                                          remove_comments = True,
                                          remove_pis = True,
                                          strip_cdata = True,
                                          compact = True,
                                          resolve_entities = True,
                                          huge_tree = True)
    
    
    def parse(self, htmlFile):
        # Parse html
        xmltree = self.__getEtree__(htmlFile)
        
        # Determine parsers
        tagparser  = None
        textparser = ParseTextNunberg()
        
        if xmltree.docinfo.public_id.find(XHTML_10_ID) != -1:
            tagparser = ParseXHTML10()
        elif xmltree.docinfo.public_id.find(XHTML_11_ID) != -1:
            tagparser = ParseXHTML11()
        elif xmltree.docinfo.public_id.find(XHTML_20_ID) != -1:
            raise etree.XMLSyntaxError, "XHTML 2.0 currently unsupported"
        elif xmltree.docinfo.public_id.find(HTML_50_ID) != -1:
            raise etree.XMLSyntaxError, "HTML 5.0 currently unsupported"
        else:
            raise etree.XMLSyntaxError, "Unsupported or unidentified XHTML or HTML type"
        
        # create DS tree
        dstree  = DocStructTree()
        dsnode  = dstree.getroot()
        self.__decorateIndent__(xmltree.getroot(), tagparser, 0)
        self.__parseUpperTree__(xmltree, dstree, dsnode, tagparser)
        self.__parseLowerTree__(dstree, dsnode, textparser)
        self.__parsePositions__(dstree.getroot())
        
        return xmltree, dstree
    
    
    def outputXML(self, tree, filename):
        root = tree.getroot()
        xmlfile = open(filename, 'w+')
        xmlfile.write(etree.tostring(root, xml_declaration=True, encoding='utf-8', pretty_print=True))
    
    
    def outputImage(self, tree, filename):
        root = tree.getroot()
        
        g = Graph(0)
        names = list()
        self.__drawTree__(root, g, -1, names)
        
        g.vs["label"] = names
        
        layout = g.layout("tree")
        visual_style = {}
        visual_style["vertex_size"] = [20] * g.vcount()
        visual_style["vertex_color"] = ["white"] * g.vcount()
        visual_style["vertex_label"] = g.vs["label"]
        visual_style["edge_width"] = [1] * g.vcount()
        visual_style["layout"] = layout
        visual_style["bbox"] = (2000, 900)
        visual_style["margin"] = 50
        visual_style["vertex_label_angle"] = [3 * math.pi / 2] * g.vcount()
        visual_style["vertex_label_size"] = [10] * g.vcount()
        
        plot(g, filename, **visual_style)
        
        
    def outputDOT(self, tree, filename):
        root = tree.getroot()
        
        g = Graph(0)
        names = list()
        self.__drawTree__(root, g, -1, names)
        
        g.vs["label"] = names
        
        layout = g.layout("tree")
        visual_style = {}
        visual_style["vertex_size"] = [20] * g.vcount()
        visual_style["vertex_color"] = ["white"] * g.vcount()
        visual_style["vertex_label"] = g.vs["label"]
        visual_style["edge_width"] = [1] * g.vcount()
        visual_style["layout"] = layout
        visual_style["bbox"] = (2000, 900)
        visual_style["margin"] = 50
        visual_style["vertex_label_angle"] = [3 * math.pi / 2] * g.vcount()
        visual_style["vertex_label_size"] = [10] * g.vcount()
        
        g.write_dot(filename)
    
    
    def __getEtree__(self, htmlFile):
        xmltree = etree.parse(htmlFile, parser=self.xmlparser)
        return xmltree
    
    
    def __parseUpperTree__(self, xmltree, dstree, dsnode, tagparser):
        for xmlnode in xmltree.iter(tag=etree.Element):
            dsnode = tagparser.handle(xmltree, xmlnode, dstree, dsnode)
            
            
    def __parseLowerTree__(self, dstree, dsnode, textparser):
        for dsnode in dstree.getroot().getroottree().iter(tag=etree.Element):
            textparser.handle(dstree, dsnode)
        
    
    def __parsePositions__(self, dsnode):
        children = list(dsnode)
        for i, child in enumerate(children):
            setPosition(child, i)
            self.__parsePositions__(child)
    
    
    def __decorateIndent__(self, xmlnode, tagparser, indent):
        children = list(xmlnode)
        
        if tagparser.isIndent(xmlnode):
            indent = indent + 1
        
        setIndent(xmlnode, indent)
        
        for child in children:
            self.__decorateIndent__(child, tagparser, indent)
        
            
    def __drawTree__(self, treeroot, graph, rootId, names):
        childId = len(names)
        graph.add_vertices(1)
        names.append(util.getTag(treeroot))
        
        if rootId >= 0:
            graph.add_edges([(rootId, childId)])
        
        children = list(treeroot)
        for child in children:
            self.__drawTree__(child, graph, childId, names)



class DocStructTree(object):
    '''
    classdocs
    '''
    
    CONSTITUENT = 'constituent'
    LEVEL       = 'level'
    INDENT      = 'indent'
    POSITION    = 'position'
    VALUE       = 'value'
    LANG       = 'lang'

    DEFAULT_INDENT   = 0
    DEFAULT_POSITION = 0
    DEFAULT_VALUE    = ''
    
    root   = None
    levels = None


    def __init__(self):
        '''
        Constructor
        '''
        rootnode = etree.Element(DOCUMENT,
                                 indent=str(DocStructTree.DEFAULT_INDENT),
                                 position=str(DocStructTree.DEFAULT_POSITION))
        self.root   = rootnode
        self.levels = LEVELS
        setValue(rootnode, DocStructTree.DEFAULT_VALUE)
        
        
    def setLang(self, lang):
        self.root.set(DocStructTree.LANG, str(lang))
        
    
    def addNode(self, parent, level, position = None, indent = None, value = None):
        node = etree.SubElement(parent, level)
        
        if position == None:
            setPosition(node, getPosition(parent))
        else:
            setPosition(node, position)
            
        if indent == None:
            setIndent(node, getIndent(parent))
        else:
            setIndent(node, indent)
            
        if value == None:
            pass
        else:
            setValue(node, value)
        
        return node
    
    
    def getroot(self):
        return self.root


def setNode(node, position = None, indent = None, value = None):
    if position != None:
        setPosition(node, position)
    if indent != None:
        setIndent(node, indent)
    if value != None:
        setValue(node, value)


def setPosition(node, position):
    node.set(DocStructTree.POSITION, str(position))
    
    
def setIndent(node, indent):
    if indent != None:
        node.set(DocStructTree.INDENT, str(indent))
    
    
def setValue(node, value):
    if value != None:
        node.set(DocStructTree.VALUE, unicode(value))
        
    
def getLevel(node):
    return util.getTag(node)
    
    
def getPosition(node):
    return int(node.get(DocStructTree.POSITION))
    
    
def getIndent(node):
    return int(node.get(DocStructTree.INDENT))
    
    
def getValue(node):
    value = node.get(DocStructTree.VALUE)
    if value != None:
        return value
    else:
        return ''

def deleteValue(node):
    attribs = node.attrib.items()
    node.attrib.clear()
    
    for attrib in attribs:
        if attrib[0] != DocStructTree.VALUE:
            node.set(attrib[0], attrib[1])
    