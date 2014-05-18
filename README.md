= PyWikiDump
'''A library for efficiently parsing Wikipedia export files.'''

## Installation

### Pre-requisites

 - memcached
 - pylibmc
 - matplotlib 

### Installing pywikidump

Download pywikidump and run:

    python setup.py install

Pywikidump uses NLTK for tokenization. Before starting it, you need to download some additional datasets.

    import nltk
    nltk.download('punkt')
