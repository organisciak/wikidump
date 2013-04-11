import re
from nltk.tokenize import sent_tokenize
from utils import (strip_between, WIKI_INTERNAL_LINK, WIKI_PIPED_LINK,
                   WIKI_FORMATTING, WIKI_CATEGORIES, WIKI_LANGUAGES,
                   WIKI_HEADING, parse_time)
from fingerprinting import nGramFingerprintKeyer
import HTMLParser


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
        # Unescape HTML
        s = HTMLParser.HTMLParser().unescape(s.decode("UTF-8"))
        # Remove all special {{}} tags, for the time being
        #s = strip_between(r'\*? ?{{', r'}}', s)
        # Remove infobox (assumes close tag is at the start of a line)
        #s = strip_between("\{\{Infobox", "\n\}\}", s)
        # Remove tables
        s = strip_between(r"\{\|", r"\|\}", s)
        # Remove comments
        s = strip_between(r"<!--", r"-->", s)
        # Simplify links
        s = re.sub(WIKI_PIPED_LINK, r"\2", s)
        s = re.sub(WIKI_INTERNAL_LINK, r"\1", s)
        s = re.sub(WIKI_FORMATTING, "", s)
        # Remove Categories
        s = re.sub(WIKI_CATEGORIES, "", s)
        s = re.sub(WIKI_LANGUAGES, "", s)
        # Replace Links with just their text
        s = re.sub(r"\[http.*? (.*?)]", "\g<1>", s)
        return s

    def sentences(self):
        '''
        Return all the sentences from the text

        Since this may be run on a large number of texts, the smart parameter
        lets you tokenize with NLTK (smart=True) or with a faster, sloppy
        regular expression.

        '''
        s = self.plaintext
        # Clean up for sentence tokenizing
        s = re.sub(WIKI_HEADING, "\g<title>.", s)
        # Make lists into sentences
        s = re.sub(r'^[\*\#](.*?)$', r'\g<1>.', s, flags=re.MULTILINE)
        # Remove References
        #s = strip_between(r"<ref name=["'](.*?)["']", r"<\/ref>", s)
        WIKI_REFS = re.compile(r'''<ref name=["'](.*?)["'].*?>(.*)<\/ref>''')
        s = re.sub(WIKI_REFS, "[[\g<1>]]", s)
        s = re.sub(r"([\.\?\!])\s{0,3}(\[\[.*?\]\])", r"\g<2>\g<1>", s)
        # Tokenize
        sentences = sent_tokenize(s)
        # Strip whitespace
        sentences = [sentence.strip() for sentence in sentences]
        return sentences

    def keys(self, size=2):
        ''' Return fingerprinted keys for each sentence '''
        keyer = nGramFingerprintKeyer(size=size)
        keys = [keyer.key(s) for s in self.sentences()]
        return keys

    def __repr__(self):
        return '<WikiDumpRevision %s for \'%s\'>' % (self.id,
                                                     self.parent.name[:50])
