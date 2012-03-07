Edict Japanese Dictionary Search with Example sentences
=======================================================

Edict dictionary and example sentences parser.
----------------------------------------------

This package uses the EDICT_ and KANJIDIC_ dictionary files.
These files are the property of the
Electronic Dictionary Research and Development Group_ , and
are used in conformance with the Group's licence_ .

.. _EDICT: http://www.csse.monash.edu.au/~jwb/edict.html
.. _KANJIDIC: http://www.csse.monash.edu.au/~jwb/kanjidic.html
.. _Group: http://www.edrdg.org/
.. _licence: http://www.edrdg.org/edrdg/licence.html

Edict Parser By **Paul Goins**, see ``edict_search.py``
Edict Example sentences Parse by query, **Pulkit Kathuria**, see ``edict_examples.py``
Edict examples pickle files are provided but latest example files can be downloaded from the links provided.

Charset
-------
Two files

- ``utf8`` Charset example file if not using ``src/jNlp/data/edict_examples``

  To convert ``EUCJP/ISO-8859-1`` to ``utf8`` ::
       
    iconv -f EUCJP -t UTF-8 path/to/edict_examples > path/to/save_with_utf-8
      
- ``ISO-8859-1`` edict_dictionary file

Outputs example sentences for a query in Japanese only for ambiguous words.


Links
-----

**Latest** Dictionary files can be downloaded here_

.. _here: http://www.csse.monash.edu.au/~jwb/edict.html

``edict_search.py``
-------------------
:author: Paul Goins `License included` linkToOriginal_:

.. _linkToOriginal: http://repo.or.cz/w/jbparse.git/blame/8e42831ca5f721c0320b27d7d83cb553d6e9c68f:/jbparse/edict.py

For all entries of sense definitions

>>> from jNlp.edict_search import *
>>> query = u'認める'
>>> edict_path = 'src/jNlp/data/edict-yy-mm-dd'
>>> kp = Parser(edict_path)
>>> for i, entry in enumerate(kp.search(query)):
...     print entry.to_string().encode('utf-8')


``edict_examples.py``
---------------------
:`Note`: Only outputs the examples sentences for ambiguous words (if word has one or more senses)

:author: Pulkit Kathuria

>>> from jNlp.edict_examples import *
>>> query = u'認める'
>>> edict_path = 'src/jNlp/data/edict-yy-mm-dd'
>>> edict_examples_path = 'src/jNlp/data/edict_examples'
>>> search_with_example(edict_path, edict_examples_path, query)

Output ::

  認める

  Sense (1) to recognize;
    EX:01 我々は彼の才能を*認*めている。We appreciate his talent.

  Sense (2) to observe;
    EX:01 ｘ線写真で異状が*認*められます。We have detected an abnormality on your x-ray.

  Sense (3) to admit;
    EX:01 母は私の計画をよいと*認*めた。Mother approved my plan.
    EX:02 母は決して私の結婚を*認*めないだろう。Mother will never approve of my marriage.
    EX:03 父は決して私の結婚を*認*めないだろう。Father will never approve of my marriage.
    EX:04 彼は女性の喫煙をいいものだと*認*めない。He doesn't approve of women smoking.
    ...

