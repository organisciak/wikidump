from wiki_dump_revision import WikiDumpRevision


class WikiDumpPage(object):
    revisions = []
    _sent_cache = {}

    def __init__(self, parent, start, end, title, pid, revisions, **kwargs):
        self.parent = parent
        self.start = start
        self.end = end
        self.title = title
        self.pid = pid
        for revision in revisions:
            self.revisions += [WikiDumpRevision(self, **revision)]
        for key, value in kwargs.iteritems():
            print "Additional arguments:"
            print "%s = %s" % (key, value)

    @property
    def plaintext(self):
        ''' Return the raw text of the page '''
        return self.parent.text(self.start, self.end)

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
            sent_index = {}
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
            return sent_index

    def __repr__(self):
        return '<WikiDumpPage for \'%s\'>' % self.title[:50]
