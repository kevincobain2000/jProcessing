#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This package uses the EDICT_ and KANJIDIC_ dictionary files.
These files are the property of the
Electronic Dictionary Research and Development Group_ , and
are used in conformance with the Group's licence_ .

.. _EDICT: http://www.csse.monash.edu.au/~jwb/edict.html
.. _KANJIDIC: http://www.csse.monash.edu.au/~jwb/kanjidic.html
.. _Group: http://www.edrdg.org/
.. _licence: http://www.edrdg.org/edrdg/licence.html
.. 
"""
# Copyright (c) 2011, Pulkit Kathuria
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
  
"""
Edict Parser By **Paul Goins**, see ``edict_search.py``
Edict Example sentences, by search query, **Pulkit Kathuria**
Edict examples pickle files are provided but latest example files
can be downloaded from the links provided.

Charset:

- utf-8 charset example file
- ISO-8859-1 edict_dictionary file

Outputs example sentences for a query in Japanese only for ambiguous words.
"""

import re, os, subprocess
from collections import defaultdict
from jNlp.edict_search import Parser
import cPickle as pickle


def word_and_id(BSent):
    results = []
    for item in BSent.split():
        brackets = re.compile('\[.*?\]')
        flter = re.sub('\(.*?\)','',item)
        word = re.split('\[|\]', re.sub('\{.*?\}','',flter))[0]
        try: s_id = re.split('\[|\]', re.sub('\{.*?\}','',flter))[1]
        except: pass
        if re.search(brackets, flter):
            results.append((word, s_id))
    return results

def parse_examples(edict_examples_file):
    """
    Edict examples format
    ---------------------
    ::
    
      A: 誰にでも長所と..  Everyone has....points.#ID=276471_4870
      B: 才[01]{歳} 以上[01] 生きる (こと){こと} は 決して ..
    
      ambiguous_words: @type = dictionary
      format: Kanji ==> id ==> [examples_sent_id, ..]
                才  ==> 01 ==> [#ID=276471_4870, ...]
      call:
        >>> ambiguous_words[kanji][01]
        ...[#ID=276471_4870, ...]
                
      edict_examples: @type = dictionary
      format:
                           ID  ==> u'example_sentence'
               #ID=276471_4870 ==> u'誰にでも長所と..  Everyone has....points'
    
    """
    ambiguous_words = {}
    edict_examples = {}
    for line in edict_examples_file.readlines():
        line = unicode(line,'utf-8')
        if line.startswith('A:'):
            eg_sent = line.split('#ID=')[0]
            eg_sent_id = line.split('#ID=')[1]
            edict_examples[eg_sent_id] = eg_sent
            continue
        for item in word_and_id(line):
            word = item[0]
            s_id = int(item[1])
            if not ambiguous_words.has_key(word): ambiguous_words[word] = {}
            if not ambiguous_words[word].has_key(s_id): ambiguous_words[word][s_id] = []
            ambiguous_words[word][s_id].append(eg_sent_id)
    return ambiguous_words, edict_examples

def edict_entry(edict_file_path, query):
    kp = Parser(edict_file_path)
    for entry in kp.search(query):
        if entry.to_string().split()[0] == query:
            entry = entry.to_string()
            glosses = re.findall('\(\d\).*?;',entry)
            s_ids = [int(re.search('\d',gloss).group(0)) for gloss in glosses]
            return s_ids, glosses
    return [],[]

def check_pickles(edict_examples_path):
    f = open(edict_examples_path)
    __checkpickles__ = ['edict_examples.p','ambiguous_words.p']
    for pickl in __checkpickles__:
        if not os.path.exists(pickl):
            ambiguous_words, edict_examples = parse_examples(f)
            pickle.dump(ambiguous_words, open("ambiguous_words.p",'wb'))
            pickle.dump(edict_examples, open("edict_examples.p",'wb'))
        else:
            ambiguous_words = pickle.load(open('ambiguous_words.p'))
            edict_examples = pickle.load(open('edict_examples.p'))
        return ambiguous_words, edict_examples
    
def search_with_example(edict_path, edict_examples_path, query):
    ambiguous_words, edict_examples = check_pickles(edict_examples_path)
    s_ids, glosses = edict_entry(edict_path, query)
    print query.encode('utf-8')
    for s_id, gloss in enumerate(glosses):
        print 
        print 'Sense', gloss
        if ambiguous_words.has_key(query) and ambiguous_words[query].has_key(s_ids[s_id]):
            for ex_num, ex_id in enumerate(ambiguous_words[query][s_ids[s_id]], 1):
                ex_sentence = edict_examples[ex_id].replace(query[0], '*'+query[0]+'*')
                print '\t', ex_sentence.replace('A:','EX:'+str(ex_num).zfill(2)).encode('utf-8')

def _mime(f_path):
    command = ['file','--mime',f_path]
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    charset = process.communicate()[0].split('charset=')[1]
    return charset.strip()

def _encoding_check(edict_path, edict_examples_path):
    if _mime(edict_path) <> 'iso-8859-1' or _mime(edict_examples_path) <>'utf-8':
        print _mime(edict_path)
        print 'examples file must utf-8 encoded'
        print 'edict dictionary must be iso-8859-1 encoded'
        print 'man iconv'
    return True
    
if __name__ == '__main__':
    query = u'出て'
    edict_path = '_dicts/edict-2011-08-30'
    edict_examples_path = '_dicts/edict_examples'
    search_with_example(edict_path, edict_examples_path, query)
    
    
    


    
            
            
        


    

