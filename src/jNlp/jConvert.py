#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys 
from jNlp.jTokenize import jTokenize, jReads
from jNlp.jCabocha import cabocha
from pkg_resources import resource_stream

class ChartParser(object):
    def __init__(self, chartFile):
        self.chart = resource_stream('jNlp', chartFile).read()
    def chartParse(self):
        """
        @return chartDict
        ガ ==> g,a
        キ ==> k,i
        キャ ==> k,ya
        Similarily for Hiragana
        @setrofim : http://www.python-forum.org/pythonforum/viewtopic.php?f=3&t=31935
        """
        lines = self.chart.split('\n')
        chartDict = {}
        output = {}
        col_headings = lines.pop(0).split()
        for line in lines:
            cells = line.split()
            for i, c in enumerate(cells[1:]):
                output[c] = (cells[0], col_headings[i])
        for k in sorted(output.keys()):
            #@k = katakana
            #@r = first romaji in row
            #@c = concatinating romaji in column
            r, c = output[k]
            k, r, c = [unicode(item,'utf-8') for item in [k,r,c]]
            if k == 'X':continue
            romaji = ''.join([item.replace('X', '') for item in [r,c]])
            chartDict[k] = romaji
        return chartDict
    
def tokenizedRomaji(jSent):
    kataDict = ChartParser('data/katakanaChart.txt').chartParse()
    tokenizeRomaji = []
    for kataChunk in jReads(jSent):
        romaji = ''
        for idx, kata in enumerate(kataChunk,1):
            if idx != len(kataChunk):
                doubles = kata+kataChunk[idx]
                if kataDict.has_key(doubles):
                    romaji += kataDict[doubles]
                    continue
            if kataDict.has_key(kata):
                romaji += kataDict[kata]
            else:
                pass
                #checkPunctuation(kata)
        tokenizeRomaji.append(romaji)
    return tokenizeRomaji

if __name__ == '__main__':
    #kataDict = ChartParser('data/katakanaChart.txt').chartParse()
    sent = u'気象庁が２１日午前４時４８分、発表した天気概況によると、'
    print ' '.join(tokenizedRomaji(sent)).encode('utf-8')
    #print tokenizedRomaji(sent)

    

            
    








        
    
    
    
    

        
            
    

    
