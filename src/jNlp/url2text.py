#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division 
from HTMLParser import HTMLParser  
from re import sub  
from sys import stderr  
from traceback import print_exc  
from urllib import *
import re, string
 
class Parser(HTMLParser):  
    def __init__(self):  
        HTMLParser.__init__(self)  
        self.__text = []  
 
    def handle_data(self, data):  
        text = data.strip()  
        if len(text) > 0:  
            text = sub('[ \t\r\n]+', ' ', text)  
            self.__text.append(text + ' ')  
 
    def handle_starttag(self, tag, attrs):  
        if tag == 'p':  
            self.__text.append('\n\n')  
        elif tag == 'br':  
            self.__text.append('\n')  
 
    def handle_startendtag(self, tag, attrs):  
        if tag == 'br':  
            self.__text.append('\n\n')  
 
    def text(self):  
        return ''.join(self.__text).strip()  
class Url2Text(object):
    def raw_text(self, html_text):  
        try:
            parser = Parser()  
            parser.feed(html_text)  
            parser.close()  
            return parser.text()  
        except:
            print "Couldn't extract"
            exit()
    
    def url2text(self, url):
        clean_text = []
        html_text = urlopen(url).read()
        count = lambda l1, l2: len(list(filter(lambda c: c in l2, l1)))
        counts = []
        text = self.raw_text(html_text)
        for line in text.splitlines():
            counts.append(count(line, string.punctuation))
        for line, punct in zip(text.splitlines(), counts):
            if line and punct < max(counts)/3:
                clean_text.append(line.strip())
        return clean_text
    
if __name__ == '__main__':
    url = "http://content.usatoday.com/communities/onpolitics/post/2012/03/mitt-romney-super-tuesday-results-rick-santorum-ohio/1"
    #url = 'http://www.terminally-incoherent.com/blog/2007/09/19/latex-squeezing-the-vertical-white-space/'
    a = Url2Text()
    print a.url2text(url)
    
    

