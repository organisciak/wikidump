'''
@author: Peter Organisciak
'''
import os
import re
import gzip


class WikiDumpExport(object):
    ''' Class for collecting Wikipedia pages, splitting them
    up by their first two characters, and writing them gzipped to disk'''
    
    def __init__(self, outpath):
        self.buffer = {}
        self.output = outpath
        ## make output dir if it doesn't exist
        if not os.path.exists(outpath):
            os.makedirs(outpath)
            
    def add(self, page, prefix=None):
        '''
        Take a page, parse the title, and save it to a buffer. Use dump() to writing to disk
        '''
        #No need to parse xml, just search regex
        if prefix is None:
            title = re.search("<title>(.*)</title>",page).group(1)
            title_prefix = title[:2].lower()
            if re.match("[a-z0-9]{2}", title_prefix) is None:
                title_prefix = "misc"
        else:
            title_prefix = prefix
            print page
        self.buffer.setdefault(title_prefix, []).append(page)
        
    def flush(self):
        ''' Save all pages in the buffer dict to disk. '''
        for (prefix,pages) in self.buffer.iteritems():
            text = "".join(pages)
            outFile = os.path.join(self.output, prefix+".gz")

            #Write to gzip, because it's faster and more fully featured, albeit not as effective at compression
            out = gzip.GzipFile(outFile, 'a')
            out.write(text)
            out.close()

        #Reset buffer to empty
        self.buffer = {}

