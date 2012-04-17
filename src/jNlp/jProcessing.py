#!/usr/bin/env python
# -*- coding: utf-8 -*-
from jNlp.jTokenize import *
from pkg_resources import resource_stream
import sys, os, subprocess, re
from subprocess import call
import xml.etree.cElementTree as etree

def long_substr(str1, str2):
    data = [str1, str2]
    substr = ''
    if len(data) > 1 and len(data[0]) > 0:
        for i in range(len(data[0])):
            for j in range(len(data[0])-i+1):
                if j > len(substr) and all(data[0][i:i+j] in x for x in data):
                    substr = data[0][i:i+j]
    return substr.strip()

class Similarities(object):
    def minhash(self, *args):
        """
        :*args: tokenized string like a nd b
        :Sentences: should be tokenized in string
        a = u"これ はな ん です"
        b = u"かこ れ何 です"
        """
        score = 0.0
        tok_sent_1 = args[0]
        tok_sent_2 = args[1]
        shingles = lambda s: set(s[i:i+3] for i in range(len(s)-2))
        try:
            jaccard_distance = lambda seta, setb: len(seta & setb)/float(len(seta | setb))
            score = jaccard_distance(shingles(tok_sent_1), shingles(tok_sent_2))
            return score
        except ZeroDivisionError: return score

class Property(object):
    def __init__(self):
        pass
    def kanaChars(self):
        Chars = []
        tables = ['hiraganaChart.txt', 'katakanaChart.txt']
        for table in tables:
            buff = resource_stream('jNlp', 'data/%s'%table).readlines()
            for line in buff:
                line = unicode(line, 'utf-8')
                Chars += line.split()
        return Chars
            
    def iscontent(self, pos):
        self.pos = pos
        self.file = resource_stream('jNlp', 'data/chasen_pos.txt').readlines()
        self.content = {}
        for line in self.file:
            if not line.strip(): continue
            line = unicode(line,'utf-8')
            pos = line.split()[2].strip()
            self.content[pos] = int(line.split()[0].strip())
        if self.content.has_key(self.pos) and self.content[self.pos]: return True
        return False
    def tok_xml(self, sent, word):
        #Usage
        #tok_xml(u'これでアナタも冷え知らず', u'冷').get('pos')
        self.sent = sent.replace(word, '*'+word+'*')
        cTree = jCabocha_with_target(self.sent)
        for chunk in cTree.getchildren():#chunks
            for tok in chunk.getchildren():
                if tok.get('target'):return tok
        return etree.fromstring(u'<tok></tok>')
    def iskana(self, word):
        romaji = ['a', 'b', 'c', 'd', 'e', 'f', 'g', \
                  'h', 'i', 'j', 'k', 'l', 'm', 'n', \
                  'o', 'p', 'q', 'r', 's', 't', 'u', \
                  'v', 'w', 'x', 'y', 'z']
        if len(word) == 1 and word in self.kanaChars() and word not in romaji:
            return True
        else: return False
        
        

if __name__ == '__main__':
    a = 'Once upon a time in Italy'
    b = 'Thre was a time in America'
    #print long_substr(a, b)
    a = u'これでアナタも冷え知らず'
    b = u'これでア冷え知らずナタも'
    #print long_substr(a, b).encode('utf-8')
    #similarity = Similarities()
    #print similarity.minhash(' '.join(jTokenize(a)), ' '.join(jTokenize(b)))
    pos = Property()
    #print pos.iscontent(u'地域')
    #print pos.tok_xml(u'これでアナタも冷え知らず', u'冷').get('pos')
    print pos.iskana(u'冷')




    

