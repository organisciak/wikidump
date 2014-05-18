'''
Test WikiDumpFile class and related.


'''
import os
import sys
import logging
from pywikidump import WikiDumpFile
#from pywikidump.plots import (plot_length_time)
#import pylibmc


def main():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                        level=logging.DEBUG)
    #path = os.path.join('/Users/dccuser/Documents/data/wikipedia/'
    #        'enwiki-latest-pages-meta-history15.xml-p004758087p004825000.bz2')
    path = 'data/tiny_wikipedia_export.bz2'
    #mc = pylibmc.Client(["127.0.0.1"], binary=True)
    #wikifile = WikiDumpFile(path, memcached=mc)
    wikifile = WikiDumpFile(path)

    # Get a Page
    page = wikifile.next_page()

    print "File location is {0}".format(wikifile.loc)
    #Skip Some Pages
    for i in range(0, 7):
        page = wikifile.next_page()
    print "New file location is {0}".format(wikifile.loc)

    # View Page Information
    print "Page {0}({1}) hae {2} revisions between bytes {3}-{4} of {5}" \
        .format(page.name, page.id, len(page.revisions), page.start,
                page.end, page.parent.name)

    # View Page Revisions
    print page.revisions
    #plot_length_time(page)
    for i, revision in enumerate(page.revisions):
        print "{0}\t{1}\t{2}\t{3}".format(i, revision.id, revision.timestamp,
                                          revision.name)

    # Inspect the last revision
    revision = page.revisions[-1]
    print revision.text[:500] + "..."

    print revision.keys()
    # View all the sentence keys for the page
    # print page.sent_keys(key_size=2, cache=False)

    print "\n=======\n".join(page.revisions[-1].sentences())
    return
    #start = time.time()

    #print page, page.plaintext[:1000]
    #for revision in page.revisions:
    #print page.revisions[-1], page.revisions[-1].timestamp
    #print page.revisions[-1].plaintext#[:100]

    # Inspect last five revisions
    #for rev in page.revisions[-5:]:
    #    print "\n".join(rev.keys(size=2))
    #for revision in page.revisions:
    #    revision.keys(size=2)
    #    revision.text
    #end = time.time()
    #logging.debug("Getting sentence keys x100 took: {0}".format(end-start))
    #print len(a)
    #b = [a[key]['lifespan'] for key in a.iterkeys()]
    #print b

if __name__ == '__main__':
    main()
