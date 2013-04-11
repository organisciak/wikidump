import datetime


class PageHistory(object):
    sentences = {}
    revisions = []

    def _init_(self, *args, **kw):
        pass

    def add_history(self, sentinfo, revindex):
        (key, text) = sentinfo
        if key not in self.sentences:
            self._new_key(sentinfo)
        self.sentences[key]['history'] += [revindex]

    def add_revision(self, timestamp, index=None):
        self.revisions += [timestamp]
        if index:
            assert 1 + index == len(self.revisions)

    def _new_key(self, sentinfo):
        (key, text) = sentinfo
        self.sentences[key] = {
            'history': [],
            'text': text
        }

    def first_revision(self, key):
        first_rev = min(self._history(key))
        return self.revisions[first_rev]

    def last_revision(self, key):
        ''' Returns the revision when the sentence disappears '''
        last_rev = max(self._history(key)) + 1
        if last_rev == len(self.revisions):
            # TODO: Return time of wiki export, and an indicator
            # that it was never deleted
            return None
        else:
            return self.revisions[last_rev]

    def survival(self, key, type='time'):
        ''' Returns the survival life of the given sentence.
        Set with type=time or type=edits
        '''
        if type == 'time':
            last = self.last_revision(key)
            if not last:
                last = datetime.datetime.now()
            return last - self.first_revision(key)
        elif type == 'edits':
            l = self._history(key)
            return max(l)-min(l)+1

    def _history(self, key, value=None):
        ''' Getter/setter for sentence history '''
        if value:
            self.sentences[key]['history'] += [value]
        return self.sentences[key]['history']
