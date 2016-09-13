import os
import sys

from lxml import etree
from io import StringIO, BytesIO


def create_tree(score_file):
    """ """
    sanitize(score_file)
    with open(score_file, 'r') as data:
        html = etree.parse(data)


def sanitize(data):
    """ """
    #check last line
    with open(data, 'a') as data:
        for line in data:
            pass 
        if '</html>' not in line:
            data.write('</html>')
        
