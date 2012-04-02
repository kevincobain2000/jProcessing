#!/usr/bin/env python
# -*- coding: utf-8 -*-
  
# Copyright (c) 2009, Paul Goins
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
  
"""A parser for EDICT.
  
This version is intended to be a more-or-less complete EDICT parser,
with the exception of not doing special parsing for loan word tags.
If you require special handling for those, then you probably ought to
be using JMdict instead.
  
"""
  
import sys, os, re, gzip, gettext
gettext.install('pyjben', unicode=True)
  
  
# Below follows the information codes sorted more-or-less as they are
# on http://www.csse.monash.edu.au/~jwb/edict_doc.html, however more
# up to date.  These sets are accurate as of 2009-Jul-17.
  
# Part of speech codes
valid_pos_codes = set((
    "adj-i", "adj-na", "adj-no", "adj-pn", "adj-t", "adj-f", "adj",
    "adv", "adv-to", "aux", "aux-v", "aux-adj", "conj", "ctr", "exp",
    "int", "iv", "n", "n-adv", "n-suf", "n-pref", "n-t", "num", "pn",
    "pref", "prt", "suf", "v1", "v2a-s", "v4h", "v4r", "v5", "v5aru",
    "v5b", "v5g", "v5k", "v5k-s", "v5m", "v5n", "v5r", "v5r-i", "v5s",
    "v5t", "v5u", "v5u-s", "v5uru", "v5z", "vz", "vi", "vk", "vn",
    "vr", "vs", "vs-s", "vs-i", "vt",
    ))
  
# Field of application codes
valid_foa_codes = set((
    "Buddh", "MA", "comp", "food", "geom", "ling", "math", "mil",
    "physics", "chem"
    ))
  
# Miscellaneous marking codes
valid_misc_codes = set((
    "X", "abbr", "arch", "ateji", "chn", "col", "derog", "eK", "ek",
    "fam", "fem", "gikun", "hon", "hum", "iK", "id", "ik", "io",
    "m-sl", "male", "male-sl", "oK", "obs", "obsc", "ok", "on-mim",
    "poet", "pol", "rare", "sens", "sl", "uK", "uk", "vulg"
    ))
  
# Dialect codes
valid_dialect_codes = set((
    "kyb", "osb", "ksb", "ktb", "tsb", "thb", "tsug", "kyu", "rkb",
    "nab"
    ))
  
# Grab all ()'s before a gloss
all_paren_match = re.compile("^(\([^)]*\)[ ]*)+")
# Grab the first () data entry, with group(1) set to the contents
paren_match = re.compile(u"^[ ]*\(([^)]+)\)[ ]*")
  
def info_field_valid(i_field):
    """Returns whether a given info code is valid."""
  
    # Validity is a sticky issue since there's so many fields:
    #
    # - Sense markers (1, 2, 3, ...)
    # - Part of speech markers (n, adv, v5r)
    # - Field of application markers (comp, math, mil)
    # - Miscellaneous meanings (X, abbr, arch, ateji, ..........)
    # - Word priority (P)
    # ? Okurigana variants (Maybe this is JMdict only?)
    # - Loan words, a.k.a. Gairaigo
    # - Regional Japanese words (Kansai-ben, etc.)
    #
    # Thankfully, this function should be reusable in the edict2 parser...
  
    if i_field in valid_pos_codes: return True
    if i_field == "P": return True
    if i_field in valid_misc_codes: return True
    if i_field in valid_foa_codes: return True
    if i_field[:-1] in valid_dialect_codes: return True
    # Check for (1), (2), etc.
    try:
        i = int(i_field)
        return True
    except:
        return False
  
class EdictEntry(object):
  
    def __init__(self, raw_entry, quick_parsing=True):
  
        # Japanese - note, if only a kana reading is present, it's
        # stored as "japanese", and furigana is left as None.
        self.japanese = None
        self.furigana = None
        # Native language glosses
        self.glosses = []
        # Info fields should be inserted here as "tags".
        self.tags = set()
        # Currently unhandled stuff goes here...
        self.unparsed = []
  
        # Most people don't need ultra-fancy parsing and can happily
        # take glosses with keywords stuck in them.  In this case,
        # they can save processing time by using parse_entry_quick.
        # However, this will mean that "J-Ben"-style entry sorting may
        # not work exactly as expected because of tags being appended
        # to the beginning or end.
  
        # Note: Even with full parsing, due to a few entries with tags
        # at the end of their glosses, there's a few entries which will not
        # successfully match on an "ends with" search.
  
        # ENABLE THIS once parse_entry_quick is implemented.
        if quick_parsing:
            self.parse_entry_quick(raw_entry)
        else:
            self.parse_entry(raw_entry)
  
    def parse_entry(self, raw_entry):
        if not raw_entry:
            return None
  
        jdata, ndata = raw_entry.split(u'/', 1)
  
        # Get Japanese
        pieces = jdata.split(u'[', 1)
        self.japanese = pieces[0].strip()
        if len(pieces) > 1:
            # Store furigana without '[]'
            self.furigana = pieces[1].strip()[:-1]
  
        #if self.furigana:
        #    print "JAPANESE: %s, FURIGANA: %s" % (self.japanese, self.furigana)
        #else:
        #    print "JAPANESE: %s" % self.japanese
  
        # Get native language data
        glosses = ndata.split(u'/')
        for gloss in glosses:
            # For each gloss, we need to check for ()'s at the beginning.
            # Multiple such ()'s may be present.
            # The actual gloss does not begin until the last set (or
            # an unhandled one) is encountered.
  
            if not gloss: continue
            #print "Unparsed gloss: [%s]" % gloss
  
            info = None
            m = all_paren_match.match(gloss)
            if m:
                info = m.group(0)
            if info:
                gloss_start = m.span()[1]
                gloss = gloss[gloss_start:]
                #print "Info field captured: [%s]" % info
  
            while info:
                m = paren_match.match(info)
                #if not m: break  # Shouldn't ever happen...
                i_field = m.group(1)
                #print "INFO FIELD FOUND:", i_field
                i_fields = i_field.split(u',')
  
                # Check that all i_fields are valid
                bools = map(info_field_valid, i_fields)
                ok = reduce(lambda x, y: x and y, bools)
  
                if not ok:
                    #print "INVALID INFO FIELD FOUND, REVERTING"
                    #print "INFO WAS %s, GLOSS WAS %s" % (info, gloss)
                    print info
                    gloss = info + gloss
                    #print "RESTORED GLOSS:", gloss
                    break
  
                for tag in i_fields:
                    self.tags.add(tag.rstrip(':')) # Handles "ksb:"
                                                    # and other
                                                    # dialect codes
                    #print "INFO FIELD FOUND:", i
                next_i = m.span()[1]
                info = info[next_i:]
  
            #print "APPENDING GLOSS:", gloss
            self.glosses.append(gloss)
  
    def parse_entry_quick(self, raw_entry):
        if not raw_entry:
            return None
  
        jdata, ndata = raw_entry.split(u'/', 1)
  
        # Get Japanese
        pieces = jdata.split(u'[', 1)
        self.japanese = pieces[0].strip()
        if len(pieces) > 1:
            # Store furigana without '[]'
            self.furigana = pieces[1].strip()[:-1]
  
        # Get native language data
        self.glosses = [g for g in ndata.split(u'/') if g]
  
    def to_string(self, **kwargs):
        if self.furigana:
            ja = _(u"%s [%s]") % (self.japanese, self.furigana)
        else:
            ja = self.japanese
        native = _(u"; ").join(self.glosses)
        return _(u"%s: %s") % (ja, native)
  
    def __unicode__(self):
        """Dummy string dumper"""
        return unicode(self.__repr__())
  
class Parser(object):
    def __init__(self, filename, use_cache=True, encoding="EUC-JP"):
        if not os.path.exists(filename):
            raise Exception("Dictionary file does not exist.")
        self.filename = filename
        self.encoding = encoding
        self.use_cache = use_cache
        self.cache = {}
  
    def search(self, query):
        """Returns a list of entries matching the query."""
        results = []
  
        def proc_entry(entry):
            if query in entry.japanese:
                results.append(entry)
            else:
                for gloss in entry.glosses:
                    if query in gloss:
                        results.append(entry)
                        break
  
        if self.use_cache and self.cache:
            # Read from cache
            for k, entry in self.cache.iteritems():
                proc_entry(entry)
        else:
            # Read from file
            if len(self.filename) >= 3 and self.filename[-3:] == ".gz":
                f = gzip.open(self.filename)
            else:
                f = open(self.filename, "rb")
            fdata = f.read()
            f.close()
            fdata = fdata.decode(self.encoding)
            lines = fdata.splitlines()
            lines = [line for line in lines if line and (line[0] != u"#")]
  
            data = {}
            for line in lines:
                entry = EdictEntry(line)
                if self.use_cache:
                    self.cache[entry.japanese] = entry
                proc_entry(entry)
  
        # Very simple sorting of results.
        # (Requires that (P) is left in glosses...)
        common = []
        other = []
  
        for item in results:
            is_common = False
            for gloss in item.glosses:
                if u'(P)' in gloss:
                    is_common = True
                    break
            if is_common:
                common.append(item)
            else:
                other.append(item)
  
        results = common
        results.extend(other)
  
        # Return results
        return results
  
if __name__ == "__main__":
    kp = Parser('../_dicts/edict-2011-08-30')
    query = u'私'
    for i, entry in enumerate(kp.search(query)):
        print entry.to_string().encode('utf-8')

