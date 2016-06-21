#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys 
import xml.etree.cElementTree as etree
#Package imports
from jNlp.jCabocha import *
import argparse
def add_target(jCabocha_tree,target_sent,**kwargs):
    """
    Following is to mark a target word
    Not called
    See jCabocha_with_target()
    """
    if kwargs.has_key('id'): attach_id = kwargs['id']
    else: attach_id = 'unknown'
    start_pos = len(target_sent.split('*')[0])
    tw = target_sent.split('*')[1]
    sent = u''
    for chunk in jCabocha_tree.getchildren():
        for tok in chunk:
            if tw in tok.text and len(sent) >= start_pos -3:
                tok.set("target", attach_id)
                return jCabocha_tree
            else: sent += tok.text
    return jCabocha_tree

def jTokenize(target_sent):
    default_marker = '*'
    target = target_sent.replace(default_marker,'')
    sentence = etree.fromstring(cabocha(target).encode('utf-8'))
    jTokenized_sent = []
    if default_marker in target_sent:
        added_target = add_target(sentence, target_sent)
    else: added_target = sentence
    for chunk in added_target.findall('chunk'):
        for tok in chunk.findall('tok'):
            if tok.get("target"): jTokenized_sent.append('*'+tok.text+'*')
            else: jTokenized_sent.append(tok.text)
    return jTokenized_sent

def jReads(target_sent):
    sentence = etree.fromstring(cabocha(target_sent).encode('utf-8'))
    jReadsToks = []
    for chunk in sentence:
        for tok in chunk.findall('tok'):
            if tok.get("feature"):
                read_tag = tok.get("feature").split(',')[-2]
                if read_tag == '*': read_tag = ''
            elif tok.get("read"):
                read_tag = tok.get("read")
            else:
                pass
            if read_tag: jReadsToks.append(read_tag)
    return jReadsToks

def jCabocha_with_target(target_sent, *args):
    #target_sent has to be marked with *
    if '*' not in target_sent: return cabocha(target_sent)
    if args: attach_id = args[0]
    else: attach_id = "unknown"
    sent_plain = etree.fromstring(cabocha(target_sent.replace('*', '')).encode('utf-8'))
    return add_target(sent_plain, target_sent, id = attach_id)

def jInfo(target_sent, infotype='base'):
    #return Info
    #Eg for base form do
    #>>>jInfo(target_sent, infotype='base')
    #...returns [word1baseform, word2baseform, ..]
    sentence = etree.fromstring(cabocha(target_sent).encode('utf-8'))
    Info = []
    for chunk in sentence:
        for tok in chunk:
            if tok.get(infotype): Info.append(tok.get(infotype))
    return Info


if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help = True)
    parser = argparse.ArgumentParser(description= 'No description sepecified')
    parser.add_argument('-a', action="store", dest="action", type=unicode, help='-a base')
    parser.add_argument('-s', action="store", dest="sentence", type=str, help='-s Sentence')
    myarguments = parser.parse_args()
    print cabocha(unicode(myarguments.sentence,'utf-8')).encode('utf-8')
    print jReads(unicode(myarguments.sentence,'utf-8'))

    """
    TO Mark the target word use * 1byte
    """
    """
    a = u'私は彼を５日前、つまりこの前の金曜日に駅で見かけた'
    print jTokenize(a)
    #print '--'.join(jTokenize(a)).encode('utf-8')
    #print '--'.join(jReads(a)).encode('utf-8')
    #--------------------------------------------------------------#
    a = u'私は彼を５日*前*、つまりこの前の金曜日に駅で見かけた'
    #print jTokenize(a)
    #input sentence has to be marked with target word otherwise target is not marked
    #print etree.tostring(jCabocha_with_target(a, 'nn:00:11'), 'utf-8')
    #print etree.tostring(jCabocha_with_target(a), 'utf-8') #default id = 'unknown'

    sent = u'日本最大級のポータルサイト'
    print jInfo(sent, 'base')
    #print ' '.join(jReads(a)).encode('utf-8')
    """
