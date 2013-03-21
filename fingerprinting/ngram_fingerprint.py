'''
Generate a N-Gram Fingerprint for a string.

Based on OpenRefine:
Details: https://github.com/OpenRefine/OpenRefine/wiki/Clustering-In-Depth
Code
https://github.com/OpenRefine/OpenRefine/blob/master/main/src/com/google/\
        refine/clustering/binning/NGramFingerprintKeyer.java

@author:Peter Organisciak
'''
import string


class nGramFingerprintKeyer:
    def __init__(self, size=2):
        self.size = size
        self.table = string.maketrans("", "")
        self.punc_ctrl = string.punctuation + self.table[:32]

    def key(self, s):
        s = s.lower()

        # Remove punctuation, control characters, and whitespace
        s = s.translate(self.table, self.punc_ctrl)
        s = "".join(s.split())

        # Split into NGrams, remove duplicates, and sort
        ngrams = self.ngram_split(s)
        ngrams = list(set(ngrams))
        ngrams.sort()

        # Rejoin sorted ngrams
        s = "".join(ngrams)

        #TODO: convert extended characters to ASCII
        return s

    def ngram_split(self, s):
        size = self.size
        ngrams = [
            s[i:i+size] for i, l in enumerate(s)
            if i <= len(s)-size
        ]
        return ngrams

if __name__ == '__main__':
    s = "This is a test string."
    keyer = nGramFingerprintKeyer(size=4)
    print keyer.key(s)
