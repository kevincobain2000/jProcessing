Libraries and Modules
=====================

Tokenize ``jTokenize.py``
-------------------------
In ``Python`` ::

  >>>from jNlp.jTokenize import jTokenize
  >>>input_sentence = u'私は彼を５日前、つまりこの前の金曜日に駅で見かけた'
  >>>list_of_tokens = jTokenize(input_sentence)
  >>>print list_of_tokens
  >>>print '--'.join(list_of_tokens).encode('utf-8')

Returns: 

::

  ...[u'\u79c1', u'\u306f', u'\u5f7c', u'\u3092', u'\uff15'...]
  ...私--は--彼--を--５--日--前--、--つまり--この--前--の--金曜日--に--駅--で--見かけ--た

Katakana Pronunciation:

::

  >>>print '--'.join(jReads(input_sentence)).encode('utf-8')
  ...ワタシ--ハ--カレ--ヲ--ゴ--ニチ--マエ--、--ツマリ--コノ--マエ--ノ--キンヨウビ--ニ--エキ--デ--ミカケ--タ


Cabocha ``jCabocha.py``
-----------------------

Run Cabocha_ with original ``EUCJP`` or ``IS0-8859-1`` configured encoding, with ``utf8`` python

.. _Cabocha: http://code.google.com/p/cabocha/

- If cobocha is configured as ``utf8`` then see this http://nltk.googlecode.com/svn/trunk/doc/book-jp/ch12.html#cabocha

In ``Python`` ::

>>>from jNlp.jCabocha import cabocha
>>>print cabocha(input_sentence).encode('utf-8')

Output:

::

  <sentence>
   <chunk id="0" link="8" rel="D" score="0.971639" head="0" func="1">
    <tok id="0" read="ワタシ" base="私" pos="名詞-代名詞-一般" ctype="" cform="" ne="O">私</tok>
    <tok id="1" read="ハ" base="は" pos="助詞-係助詞" ctype="" cform="" ne="O">は</tok>
   </chunk>
   <chunk id="1" link="2" rel="D" score="0.488672" head="2" func="3">
    <tok id="2" read="カレ" base="彼" pos="名詞-代名詞-一般" ctype="" cform="" ne="O">彼</tok>
    <tok id="3" read="ヲ" base="を" pos="助詞-格助詞-一般" ctype="" cform="" ne="O">を</tok>
   </chunk>
   <chunk id="2" link="8" rel="D" score="2.25834" head="6" func="6">
    <tok id="4" read="ゴ" base="５" pos="名詞-数" ctype="" cform="" ne="B-DATE">５</tok>
    <tok id="5" read="ニチ" base="日" pos="名詞-接尾-助数詞" ctype="" cform="" ne="I-DATE">日</tok>
    <tok id="6" read="マエ" base="前" pos="名詞-副詞可能" ctype="" cform="" ne="I-DATE">前</tok>
    <tok id="7" read="、" base="、" pos="記号-読点" ctype="" cform="" ne="O">、</tok>
   </chunk>



Kanji / Katakana /Hiragana to Tokenized Romaji ``jConvert.py``
--------------------------------------------------------------

Uses ``data/katakanaChart.txt`` and parses the chart. See katakanaChart_.

Usage ::

>>>from jNlp.jConvert import *
>>>input_sentence = u'気象庁が２１日午前４時４８分、発表した天気概況によると、'
>>>print ' '.join(tokenizedRomaji(input_sentence))
>>>print tokenizedRomaji(input_sentence)

Output ::

...kisyoutyou ga ni ichi nichi gozen yon ji yon hachi hun  hapyou si ta tenki gaikyou ni yoru to
...[u'kisyoutyou', u'ga', u'ni', u'ichi', u'nichi', u'gozen',...]

 
**katakanaChart.txt**


.. _katakanaChart:

- katakanaChartFile_ and hiraganaChartFile_

.. _katakanaChartFile: https://raw.github.com/kevincobain2000/jProcessing/master/src/jNlp/data/katakanaChart.txt

.. _hiraganaChartFile: https://raw.github.com/kevincobain2000/jProcessing/master/src/jNlp/data/hiraganaChart.txt


Longest Common String Japanese ``jProcessing.py``
-------------------------------------------------

On English Strings ::

>>> from jNlp.jProcessing import long_substr
>>> a = 'Once upon a time in Italy'
>>> b = 'Thre was a time in America'
>>> print long_substr(a, b)

Output ::

...a time in

On Japanese Strings ::

>>> a = u'これでアナタも冷え知らず'
>>> b = u'これでア冷え知らずナタも'
>>> print long_substr(a, b).encode('utf-8')

Output ::

...冷え知らず

Similarity between two sentences ``jProcessing.py``
---------------------------------------------------
Uses MinHash by checking the overlap http://en.wikipedia.org/wiki/MinHash

:English Strings:

>>> from jNlp.jProcessing import Similarities
>>> s = Similarities()
>>> a = 'There was'
>>> b = 'There is'
>>> print s.minhash(a,b)
...0.444444444444

:Japanese Strings:

>>> from jNlp.jProcessing import *
>>> a = u'これは何ですか？'
>>> b = u'これはわからないです'
>>> print s.minhash(' '.join(jTokenize(a)), ' '.join(jTokenize(b)))
...0.210526315789

