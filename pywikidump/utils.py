import re
import datetime

# Regular Expressions

# [[Wikipedia_page|Text on the page]]
#   Group 1 is link, 2 is text
WIKI_PIPED_LINK = re.compile(r"\[\[(.*?)\|(.*?)\]\]")
# [[PAGE]]
WIKI_INTERNAL_LINK = re.compile(r'\[\[(.*?)\]\]', re.DOTALL)
# [url/link.html Text of page]
WIKI_EXTERNAL_LINK = re.compile(r'\[(\w*) (.*)\]', re.DOTALL)
# Formatting marks
WIKI_FORMATTING = re.compile(r"""
                             '{2,5}        # Bold or italic ticks
                             |<\/?strike>  # Strike start and end tags
                             |<\/?nowiki(?: \/)?>  # nowiki tags
                             """,
                             re.VERBOSE | re.DOTALL | re.IGNORECASE
                             )
WIKI_HEADING = re.compile(r"""
                          ^(=+)     # One or more equal signs at line start
                          (?P<title>.*?) # Named group for heading title
                          (\1)$    # Same number of equal signs as earlier
                          """, re.VERBOSE | re.MULTILINE)

# Special tags
WIKI_CATEGORIES = re.compile(r"^Category:.*?\n", re.MULTILINE)
langs = ['en', 'pl', 'ru', 'it', 'pt', 'cs', 'fr', 'nl']
WIKI_LANGUAGES = re.compile(r"^(?:{0}):.*?$\n?".format("|".join(langs)),
                            re.MULTILINE)


# Functions
def strip_between(a, b, string):
    """
    Removes anything between (and including) string a and b inside the given
    string.
    From Pattern.web: github.com/clips/pattern/ (too small for dependency)
    """
    p = "%s.*?%s" % (a, b)
    p = re.compile(p, re.DOTALL | re.I)
    return re.sub(p, "", string)


def parse_time(time):
    ''' Parse  a timestamp string in the form of 2006-04-18T22:00:53Z or
    2006-04-18T22:00:53.
    Note that the Zulu timezone in the first form is not parsed.

    Returns a datetime object.
    '''
    if time[-1] == 'Z':
        time = time[:-1]
    time = datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S')
    return time
