'''
Created on 2009-11-17

@author: cfournie
'''

import os, sys


from docstruct.Parser import DocStructParser


if __name__ == '__main__':
    input = '../data/'
    output = '../output/'
    
    for i, arg in enumerate(sys.argv):
        if i == 1:
            input = arg
        elif i == 2:
            output = arg
    
    for root, dirs, files in os.walk(output):
            for file in files:
                os.remove(os.path.join(root, file))
    
    try:
        os.mkdir(output)
    except:
        pass #print "Unexpected error:", sys.exc_info()[0]
    
    parser = DocStructParser(input, output)
    parser.parse()
