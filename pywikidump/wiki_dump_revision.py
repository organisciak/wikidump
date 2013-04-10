import re
from nltk.tokenize import sent_tokenize
from utils import (strip_between, WIKI_INTERNAL_LINK, WIKI_PIPED_LINK,
                   WIKI_FORMATTING, parse_time)
from fingerprinting import nGramFingerprintKeyer


# CLASSES
class WikiDumpRevision(object):
    ''' Representation of a single revision of a Wikipedia page.'''
    def __init__(self, parent, start, end, rid, timestamp, text_start,
                 text_end, **kwargs):
        self.parent = parent
        self.start = start
        self.end = end
        self.id = rid
        self.text_start = text_start
        self.text_end = text_end
        self._timestamp = timestamp

    @property
    def name(self):
        '''Return the page name'''
        return self.parent.name

    @property
    def timestamp(self):
        ''' Return a parsed timestamp '''
        return parse_time(self._timestamp)

    @property
    def raw(self):
        ''' Return the raw xml of the revision '''
        return self.parent.parent.text(self.start, self.end)

    @property
    def text(self):
        ''' Return the unprocessed text content of the revision '''
        return self.parent.text(self.text_start, self.text_end)
        #return self.parent.parent.text(self.text_start, self.text_end)

    @property
    def plaintext(self):
        ''' The article text without wiki formatting '''
        return self._plaintext(self.text)

    def _plaintext(self, string):
        s = string
        # Remove infobox (assumes close tag is at the start of a line)
        s = strip_between("\{\{Infobox", "\n\}\}", s)
        # Remove tables
        s = strip_between(r"\{\|", r"\|\}", s)
        # Simplify links
        s = re.sub(WIKI_PIPED_LINK, r"\2", s)
        s = re.sub(WIKI_INTERNAL_LINK, r"\1", s)
        s = re.sub(WIKI_FORMATTING, "", s)
        return s

    def sentences(self):
        '''
        Return all the sentences from the text

        Since this may be run on a large number of texts, the smart parameter
        lets you tokenize with NLTK (smart=True) or with a faster, sloppy
        regular expression.

        '''
        sentences = sent_tokenize(self.plaintext)
        return sentences

    def keys(self, size=2):
        ''' Return fingerprinted keys for each sentence '''
        keyer = nGramFingerprintKeyer(size=size)
        keys = [keyer.key(s) for s in self.sentences()]
        return keys

    def __repr__(self):
        return '<WikiDumpRevision %s for \'%s\'>' % (self.id,
                                                     self.parent.name[:50])