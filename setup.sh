#!/bin/bash

# modify if want to use other dir as data dir
LOCALDIR=$(pwd)

# modify if want to use custom pdf reader
READER=/usr/bin/xdg-open 
READERARG=

mkdir -p $LOCALDIR/pdf
mkdir -p $LOCALDIR/org
echo "pdf_reader = '$READER'" > refconf.py
echo "pdf_reader_arg = '$READERARG'" >> refconf.py
echo "dir_prefix = '$LOCALDIR/'" >> refconf.py

# run a test
echo "Setup finished, running a test..."
echo ""
echo "Download a paper may need some time"
echo "If everything works, you will find your system pdf-reader popup,"
echo "  and the pdf file is saved to ./pdf/Maldacena_astro-ph_0210603.pdf"
echo "Also, the meta data is restored in ./org/classic.org"
echo "It is a text file, but best read by emacs org-mode."
echo "In emacs org-mode, you can use tab key to fold / unfold details"
echo ""
echo "If there is a problem, have a look at refconf.py"
echo "Or report bug to tririverwangyi@gmail.com"
./heporg.py test_arxiv.htm

