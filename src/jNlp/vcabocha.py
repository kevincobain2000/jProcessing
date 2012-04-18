#! /usr/bin/env python
# -*- coding: utf-8 -*-
from jNlp.jCabocha import *
from jNlp.jTokenize import *
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help = True)
    parser = argparse.ArgumentParser(description= 'No description sepecified')
    parser.add_argument('-a', action="store", dest="action", type=unicode, help='-a [cabocha, tokenize, base, read, pos]')
    parser.add_argument('-s', action="store", dest="sentence", type=str, help='-s Sentence')
    myarguments = parser.parse_args()
    sent = unicode(myarguments.sentence,'utf-8')
    print myarguments.action
    if myarguments.action == "cabocha":
        print cabocha(sent).encode('utf-8')
    elif myarguments.action == "tokenize":
        print 'Tokenized'
        print '========='
        print '\n'.join(jTokenize(sent))
    elif myarguments.action:
        tokenized = jTokenize(sent)
        info = jInfo(sent, infotype=myarguments.action)
        mxlen = len(max(max(tokenized, key=len), max(info, key=len))) + 30
        print '{0:{mx}}{1:}'.format('Sent',myarguments.action, mx = mxlen)
        print '{0:{mx}}{1:}'.format('====','='*len(myarguments.action), mx = mxlen)
        
        for i, j in zip(tokenized, info):
            i = i.encode('utf-8')
            j = j.encode('utf-8')
            print '{0:{mx}}{1:<}'.format(i,j, mx = mxlen)
    else:
        print cabocha(sent).encode('utf-8')
        


        
