=======
PyWikiDump
==========

*A library for efficiently parsing Wikipedia export files.*

### Documentation

http://organisciak.github.com/wikidump/

### Tutorial

http://organisciak.github.com/wikidump/tutorial.html

### Installing pywikidump

Download pywikidump and run:

    python setup.py install

Pywikidump uses NLTK for tokenization. Before starting it, you need to download some additional datasets.

    import nltk
    nltk.download('punkt')
