import re

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
#WIKI_TABLE = re.compile


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
