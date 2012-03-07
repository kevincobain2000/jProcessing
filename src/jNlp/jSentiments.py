#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import sys, subprocess, argparse
from subprocess import call
from jNlp.jTokenize import jTokenize
from jNlp.jColor import color

class Sentiment(object):
    def train(self, senti_path, wnjpn_path):
        """
        ``idSenti & idjWord = type<dict> `` ::

          idSenti[00004980] = [posScore, negScore]
          idjWord[u'kanji/jword'] = 00004980
        """
        self.idSenti = {}
        self.idjWord = {}
        with open(senti_path) as senti_f:
            senti_text = senti_f.readlines()
        for line in senti_text:
            if line.startswith('#'): continue
            try:
                ID, pScore, nScore = line.split()[1:4]
                self.idSenti[ID] = [float(pScore), float(nScore)]
            except (IndexError, ValueError): pass
        with open(wnjpn_path) as jwn_f:
            jwn_text = jwn_f.readlines()
        for line in jwn_text:
            ID = line.split()[0].split('-')[0]
            jWord = unicode(line.split()[1].strip(), 'utf-8')
            self.idjWord[jWord] = ID
        return self.idSenti, self.idjWord
    
    def polarScores_word(self, word):
        """
        returns pos, neg score for one kanji
        """
        if not self.idjWord.has_key(word): return 0.0, 0.0
        pScore = self.idSenti[self.idjWord[word]][0]
        nScore = self.idSenti[self.idjWord[word]][1]
        return pScore, nScore

    def polarScores_text(self, text):
        pScore = 0.0
        nScore = 0.0
        for sent in text.split(u'。'):
            for word in jTokenize(sent):
                if not self.idjWord.has_key(word): continue
                pScore += self.idSenti[self.idjWord[word]][0]
                nScore += self.idSenti[self.idjWord[word]][1]
        return pScore, nScore

    def baseline(self, text):
        pScore, nScore = self.polarScores_text(text)
        print 'Pos Score = %.3f Neg Score = %.3f'%(pScore, nScore)
        if pScore == nScore:
            print 'Text is Neural or Cannot Determine'
            return ''
        if pScore > nScore:
            print 'Text is', color('Positive', "green")
            return ''
        else:
            print 'Text is', color('Negative',"red")
            return ''

if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help = True)
    parser = argparse.ArgumentParser(description= 'Sentiment Classifier for Japanese Text')
    #parser.add_argument('-f', action="store", nargs = 2, dest="files", type=argparse.FileType('rt'), help='-f senti.txt jwn.txt')
    myarguments = parser.parse_args()

    jp_wn = '_dicts/wnjpn-all.tab'
    en_swn = '_dicts/SentiWordNet_3.0.0_20100908.txt'
    classifier = Sentiment()
    sentiwordnet, jpwordnet  = classifier.train(en_swn, jp_wn)
    positive_score = sentiwordnet[jpwordnet[u'全部']][0]
    negative_score = sentiwordnet[jpwordnet[u'全部']][1]
    print 'pos score = {0}, neg score = {1}'.format(positive_score, negative_score)

    text = u'監督、俳優、ストーリー、演出、全部最高！'
    print classifier.baseline(text)
    
    

    
