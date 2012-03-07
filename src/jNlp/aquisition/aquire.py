#! /usr/bin/env python
# -*- coding: utf-8 -*-
from OpenSubtitles import *

def get_movie_names(directory):
    movienames = []
    for line in open('movies.txt').readlines():
        if not line.strip():continue
        movienames.append(line.strip())
    return movienames

if __name__ == '__main__':
    opensubs = OpenSubtitles()
    out = open('download_subs.xml','wb')
    for moviename in get_movie_names('movies.txt'):
        avail_en = ''
        avail_jp = ''
        try:
            all_langs = opensubs.query(moviename)
            for info_dic in all_langs:
                if info_dic['lang'] == 'en':
                    avail_en = 'en'
                    down_en = info_dic['link']
                if info_dic['lang'] == 'ja':
                    avail_jp = 'jp'
                    down_jp = info_dic['link']
        
            if avail_en and avail_jp:
                print moviename
                output = "<movie name='%s' down_en='%s' down_jp='%s'></movie>"%(moviename, down_en, down_jp)
                out.write(output)
                out.write('\n')
        except: pass
    

