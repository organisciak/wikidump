from wiki_dump_revision import WikiDumpRevision
from collections import defaultdict


class WikiDumpPage(object):
    '''
    Representation of a page from a Wikipedia export.
    '''
    revisions = []
    _sent_cache = {}

    def __init__(self, parent, start, end, title, page_id, revisions,
                 memcached=None, **kwargs):
        self.parent = parent
        self.start = start
        self.end = end
        self.name = title
        # I'm doing it, I'm totally doing it: overriding the built-in id
        self.id = page_id
        self.memcached = memcached
        for revision in revisions:
            self.revisions += [WikiDumpRevision(self, **revision)]
        for key, value in kwargs.iteritems():
            print "Additional arguments:"
            print "%s = %s" % (key, value)

    @property
    def plaintext(self):
        ''' Return the raw text of the page '''
        return self.text(self.start, self.end)

    def sent_keys(self, cache=True, key_size=2):
        '''
        An index of sentence keys.
        For each unique fingerprint, an entry is created, with the following
        structure:

        sentence_key : {
                        history: [rev_index1, rev_index2...rev_indexN]
                        first_rev: int,
                        last_rev: int,
                        lifespan: int
                        text: String
                        }

        Note that the revisions are identified by their index, NOT the id of
        the revision. The id can be recovered with Page.revisions[rev_index].

        The "text" field is saved with the first instance of the sentences.
        For performance, it makes sense to save it only once, rather than
        each time a sentence is saved. Intuitively, however, is is sensible
        that the last revision of the same sentence would be the most correct.
        '''
        if cache is True and self._sent_cache:
            return self._sent_cache
        if cache is False or not self._sent_cache:
            '''sent_index = {}
            for i, revision in enumerate(self.revisions):
                keys = revision.keys(size=key_size)
                for key in keys:
                    if key not in sent_index:
                        sent_index[key] = {
                            'history': [],
                            'first_rev': i,
                            'last_rev': 0,
                            'lifespan': 0
                        }
                    sent_index[key]['history'] += [i]
                    sent_index[key]['last_rev'] = i

            # Calculate sentence lifetimes
            for key in sent_index.iterkeys():
                sent_index[key]['lifespan'] = (1 + sent_index[key]['last_rev']
                                               - sent_index[key]['first_rev'])

            if cache is True:
                self._sent_cache = sent_index
            return sent_index'''
            sent_history = defaultdict(list)
            #sent_firstrev = {}
            #sent_lastrev = defaultdict(int)

            for i, revision in enumerate(self.revisions):
                keys = revision.keys(size=2)
                for key in keys:
                    sent_history[key].append(i)
            return sent_history

    def text(self, start=None, end=None):
        '''
        Return the text of the page.

        The start and end args specify byte locations, relative to the parent
        WikiDumpFile. If specified, they need to be within the boundaries of
        this page's byte locations.
        '''
        if not self.memcached:
            return self._uncached_text(start=start, end=end)

        if start is None:
            start = self.start
        if end is None:
            end = self.end

        # If caching, it make sense to get the full page first, regardless
        # of whether you're returning everything or just a part
        page_text = self.memcached.get(self.id)
        if page_text is None:
            page_text = self.parent.text(self.start, self.end)
            self.memcached.set(self.id, page_text)

        return page_text[start-self.start:end-self.end]

    def _uncached_text(self, start=None, end=None):
        if start is None:
            return self.parent.text(self.start, self.end)
        else:
            assert start >= self.start and end <= self.end
            return self.parent.text(start, end)

    def __repr__(self):
        return '<WikiDumpPage for \'%s\'>' % self.name[:50]
