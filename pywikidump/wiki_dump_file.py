'''
Created on Dec 11, 2012

@author: Peter Organisciak
'''
import bz2
import re
import logging
import os
from wiki_dump_page import WikiDumpPage

### Regular Expressions ###

# Tags
TEXT_TAG_START = re.compile('\s*\<text xml:space="preserve"')
TEXT_TAG_END = re.compile('.*<\/text>\n?')
PAGE_TAG_END = re.compile('\s*\<\/page>')
REVISION_TAG_START = re.compile('\s*\<revision\>\n?')
REVISION_TAG_END = re.compile('.*\<\/revision\>\n?')
# Example: <timestamp>2006-04-15T12:24:27Z</timestamp>
TIMESTAMP_TEXT_MATCH = re.compile(r'<timestamp>(.*)<\/timestamp>')
COMMENT_TEXT_MATCH = re.compile(r'<comment>(.*)<\/comment>')
USER_TEXT_MATCH = re.compile(r'<i[d|p]>(.*)<\/i[d|p]>')
# Syntax
# In addition to the #REDIRECT tag, account for the invalid but seen REDIRECT:
REDIRECT = re.compile('\#REDIRECT|REDIRECT:', re.IGNORECASE)


### Classes ###
class WikiDumpFile(object):
    '''
    Handler for Wikipedia bzip2 export files.
    '''
    def __init__(self, file, bytes=0, memcached=None):
        self.file = bz2.BZ2File(file, 'r')
        self.page = os.path.abspath(file)
        self.name = os.path.basename(file)
        self.loc = bytes
        if self.loc > 0:
            self.file.seek(self.loc)
        self.lines = 0
        self.pages = 0
        self.memcached = memcached

    def next_page(self, namespaces=[0]):
        ''' Return a WikiDumpPage object representing the next page
        in the file '''
        page_buffer = ""
        page = {}
        revision = {}
        page_open = False
        revision_open = False
        skip_page = False

        # Compile Regex of allowable namespaces
        accept_ns = re.compile(
            r'\s*<ns>(%s)</ns>' % "|".join([str(a) for a in namespaces])
        )

        while True:
            line = self.file.readline()
            self.lines += 1
            self.loc = self.file.tell()

            if page_open and not skip_page:
                #Write line to buffer
                page_buffer = page_buffer + line
                page['lines'] += 1
                if page['lines'] is 1:
                    #First line of <page> is title
                    page['title'] = line.strip()[7:-8]
                if page['lines'] is 2:
                    #Second line of <page> is namespace
                    # Check for namespace. If the page is not in acceptable
                    # namespace, turn on skip_page flag
                    # again with next page
                    if not accept_ns.match(line):
                        skip_page = True
                elif page['lines'] is 3:
                    # Third line of <page> is id
                    page["page_id"] = line.strip()[4:-5]

                if revision_open:
                    revision['lines'] += 1
                    # Line count heuristics for less Regex
                    if revision['lines'] is 1:
                        # First line of <revision> is id
                        revision['rid'] = line.strip()[4:-5]
                    elif revision['lines'] is 2 or revision['lines'] is 3:
                        timestamp = TIMESTAMP_TEXT_MATCH.search(line)
                        if timestamp is not None:
                            revision['timestamp'] = timestamp.group(1)
                    elif revision['lines'] is 5 or revision['lines'] is 6:
                        author = USER_TEXT_MATCH.search(line)
                        if author is not None:
                            revision['author'] = author.group(1)
                    elif REVISION_TAG_END.search(line):
                        revision_open = False
                        revision['end'] = self.loc
                        page['revisions'] += [revision]
                    elif TEXT_TAG_START.match(line):
                        revision['text_start'] = self.loc - len(line) + 33
                        if line[30:35] == 'e" />':
                            logging.debug("Skipping blank revision")
                            revision_open = False
                            revision = {}
                        if REDIRECT.search(line):
                            # TO CONFIRM: Assumes redirects are always at the
                            # start of the text.
                            logging.debug("Skipping revision due to redirect.")
                            revision_open = False
                            revision = {}
                    else:
                        # Comments are infrequent, so saving this for last
                        comment = COMMENT_TEXT_MATCH.search(line)
                        if comment is not None:
                            revision['comment'] = comment.group(1)
                    # No elif b/c <text> can start and end on the same line
                    if TEXT_TAG_END.search(line):
                        #line[-8:] == '</text>\n':
                        revision['text_end'] = self.loc - 8

                if REVISION_TAG_START.match(line):
                    revision_open = True
                    revision = {'start': self.loc - len(line),
                                'lines': 0
                                }

                if PAGE_TAG_END.match(line):
                    page_open = False
                    self.pages += 1
                    page['end'] = self.loc
                    if len(page['revisions']) is 0:
                        logging.debug("No valid revisions found, skipping")
                        return self.next_page(namespaces)
                    else:
                        if self.memcached:
                            #Save page buffer to memcached
                            self.memcached.set(page["page_id"], page_buffer)
                        return WikiDumpPage(self, **page)
                    #page_buffer = ""
            # Only check for end of page tag when skipping page
            elif page_open and skip_page:
                if line == '  </page>\n':
                    logging.debug("Skipping pages due to namespace.")
                    return self.next_page(namespaces)
            elif line == '  <page>\n':
                logging.info("Opening page")
                page_open = True
                page = {'lines': 0,
                        'start': self.loc - len(line),
                        'revisions': [],
                        'memcached': self.memcached
                        }
                page_buffer = line
            elif not page_open:
                # Check if file is done
                if line == '':
                    logging.info("No more pages left in file")
                    #page_buffer = False
                    break

    def text(self, start, end, return_to_original=True):
        '''
        Read text between two byte points, then return to the previous read
        state.
        '''
        logging.debug('seeking in WikiDumpFile')
        self.file.seek(start)
        text = self.file.read(end - start)
        if return_to_original:
            self.file.seek(self.loc)
        return text


if __name__ == '__main__':
    pass
