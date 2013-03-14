from wiki_dump_revision import WikiDumpRevision


class WikiDumpPage(object):
    revisions = []

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

    def __repr__(self):
        return '<WikiDumpPage for \'%s\'>' % self.title[:50]
