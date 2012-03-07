Sentiment Analysis Japanese Text
================================

This section covers (1) Sentiment Analysis on Japanese text using Word Sense Disambiguation, Wordnet-jp_ (Japanese Word Net file name ``wnjpn-all.tab``), SentiWordnet_ (English SentiWordNet file name ``SentiWordNet_3.*.txt``).

.. _Wordnet-jp: http://nlpwww.nict.go.jp/wn-ja/eng/downloads.html
.. _SentiWordnet: http://sentiwordnet.isti.cnr.it/

Wordnet files download links
----------------------------

1. http://nlpwww.nict.go.jp/wn-ja/eng/downloads.html
2. http://sentiwordnet.isti.cnr.it/

How to Use
----------

The following classifier is baseline, which works as simple mapping of Eng to Japanese using Wordnet and classify on polarity score using SentiWordnet. 

- (Adnouns, nouns, verbs, .. all included)
- No WSD module on Japanese Sentence
- Uses word as its common sense for polarity score

>>> from jNlp.jSentiments import *
>>> jp_wn = '../../../../data/wnjpn-all.tab'
>>> en_swn = '../../../../data/SentiWordNet_3.0.0_20100908.txt'
>>> classifier = Sentiment()
>>> classifier.train(en_swn, jp_wn)
>>> text = u'監督、俳優、ストーリー、演出、全部最高！'
>>> print classifier.baseline(text)
...Pos Score = 0.625 Neg Score = 0.125
...Text is Positive

Japanese Word Polarity Score
----------------------------

>>> from jNlp.jSentiments import *
>>> jp_wn = '_dicts/wnjpn-all.tab' #path to Japanese Word Net
>>> en_swn = '_dicts/SentiWordNet_3.0.0_20100908.txt' #Path to SentiWordNet
>>> classifier = Sentiment()
>>> sentiwordnet, jpwordnet  = classifier.train(en_swn, jp_wn)
>>> positive_score = sentiwordnet[jpwordnet[u'全部']][0]
>>> negative_score = sentiwordnet[jpwordnet[u'全部']][1]
>>> print 'pos score = {0}, neg score = {1}'.format(positive_score, negative_score)
...pos score = 0.625, neg score = 0.0
