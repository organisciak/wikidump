Tutorial
========
Below is a short introduction to pywikidump. For a brief overview of what can be done with the library, see :doc:`overview`.

Setup
-----------
Prior to trying this tutorial, make sure you have :py:mod:`pywikidump` and dependencies installed according to the :doc:`installation` instructions.

PyWikiDump interfaces with Wikipedia full history bzip2 data dumps. These can be obtained at `Wikimedia
<http://dumps.wikimedia.org/enwiki/latest>`_ with the filenames ``enwiki-latest-pages-meta-history….bz2``. For this tutorial, you can use a small sample found in ``test/tiny_wikipedia_export.bz2``.

To set-up for the examples below, first we'll load memcached. In a separate console window, type :command:`memcached` in your terminal to load the memcached daemon on the default port.

Loading a Wikipedia Export File
--------------------------------
Wikipedia files are represented with :py:class:`pywikidump.WikiDumpFile`, instantiated with the path to the file and a memcached client from pylibmc.

.. code-block:: python
   :emphasize-lines: 4,5

   from pywikidump import WikiDumpFile
   import pylibmc
   # Connect to memcached
   mc = pylibmc.Client(["127.0.0.1"], binary=True)
   path = 'test/tiny_wikipedia_export.bz2'
   wikifile = WikiDumpFile(path, memcached=mc)

Fetching Wikipedia Pages
------------------------
Pages are read consecutively in the bz2 stream. :py:meth:`WikiDumpFile.next_page` reads the WikiDumpFile until a page ends. By default, only pages from the main namespace (i.e. the articles) are returned, and redirects are skipped.

.. code-block:: python

    # Get a Page
    page = wikifile.next_page()

:meth:`next_page` returns a :class:`pywikidump.WikiDumpPage` instance of the next page in the file::

    >>> page.name
    Kozhukhovskaya
    >>> page.id
    4758087
    >>> page.text()
    <title>Kozhukhovskaya</title>\n<ns>0</ns>\n<id>4758087</id>...

The parent file is also accessible through :data:`parent`::

    >>> page.parent.name
    tiny_wikipedia_export.bz2

Note that reading a page moves the pointer through the WikiDumpFile, saving the new byte location in :py:data:`WikiDumpFile.loc`.::

    >>> print "File location is {0}".format(wikifile.loc)
    File location is 58908 
    >>> for i in range(0, 7):
    ...    page = wikifile.next_page()
    >>> print "New file location is {0}".format(wikifile.loc)
    New file location is 2262794

One thing to note is that :class:`WikiDumpPage` does not save the text. Instead, it remembers the byte locations of the page in the export file. Since seeking through such a large file can be costly, memcached saves the article text temporarily. If the memcached entry is no longer available, text is read from the main file with :py:meth:`WikiDumpFile.read`.

.. code-block:: python

    >>> page.start
    2235
    >>> page.end
    58908

Moments in time with revisions
------------------------------
One way to think of :class:`WikiDumpPage` is as the entire history of a Wikipedia article. However, articles are constantly being editing. A snapshot of an article at a particular moment in time is known as '''revision'''. Revisions are represented as :class:`WikiDumpRevision` and accessed through :meth:`WikiDumpPage.revisions`::

        >>> for i, revision in enumerate(page.revisions):
        ...     print "{0}\t{1}\t{2}\t{3}".format(i, revision.id, revision.timestamp,
        ...                                       revision.name)
        0       48559048        2006-04-15 12:24:27     Kozhukhovskaya
        1       49064796        2006-04-18 22:00:36     Kozhukhovskaya
        2       49064837        2006-04-18 22:00:53     Kozhukhovskaya
        3       49064954        2006-04-18 22:01:50     Kozhukhovskaya
        …
        21      422120151       2011-04-03 10:18:08     Kozhukhovskaya
        22      422150476       2011-04-03 14:56:23     Kozhukhovskaya
        23      465930271       2011-12-15 02:28:29     Kozhukhovskaya

Through :class:`WikiDumpRevision`, it is easy to access data such as :meth:`sentences`, :data:`plaintext`, and :data:`timestamp`. Below is an example of how such information could be used with mimal code.

.. image:: images/tutorial-time-length.png
   :height: 600px
   :width: 800px
   :scale: 50%

(Code: :doc:`examples/plot-time-length`)

Tracking text across revisions
==============================
You can track sentences across all revisions with :meth:`WikiDumpPage.sent_keys`.

On a lower level, sentence tracking is made possible through :class:`WikiDumpRevision`'s keying `NGram Fingerprinter<https://github.com/OpenRefine/OpenRefine/wiki/Clustering-In-Depth#n-gram-fingerprint>`_:

        >>> revision = page.revisions[0]
        >>> revision.keys()
        ['alanasatayblcoemetgrhehohuinioiskakhkolalily…ascskslsttathtitrubuku\xd0vswmyayuzh, … , adalarataubiblcechcoctdeeaecedeie…meoeperesetf']
