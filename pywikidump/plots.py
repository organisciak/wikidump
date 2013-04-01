'''
Collection of Matplotlib plots for wikidump.

@author:Peter Organisciak
'''
import matplotlib
from pylab import (xlabel, ylabel, title, grid, plot_date, show)


### DEFAULTS ###
def default_plot():
    grid(True)


### PLOTS ###
def plot_length_time(page):
    plot_date(revision_times(page), article_length(page), linewidth=1.0,
              linestyle='-')
    title('Article Length over time')
    default_plot()
    show()


def plot_sent_time(page):
    plot_date(revision_times(page), sentence_count(page), linewidth=1.0,
              linestyle='-')
    title('Sentence count over time')
    default_plot()
    show()


#### Building Blocks ####
# Y-Axis Builders
def plot_sentence_time(page):
    pass


def revision_times(page):
    rtimes = [revision.timestamp for revision in page.revisions]
    dates = matplotlib.dates.date2num(rtimes)
    xlabel('Date')
    return dates


# X-Axis Builders
def revision_index(page):
    a = range(0, len(page.revisions))
    xlabel("Revision")
    return a


def article_length(page):
    ylabel('Article length')
    rlengths = [len(revision.plaintext) for revision in page.revisions]
    return rlengths


def sentence_count(page):
    ylabel('Sentence Count')
    rlengths = [len(revision.sentences()) for revision in page.revisions]
    return rlengths
