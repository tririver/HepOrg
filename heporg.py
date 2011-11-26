#! /usr/bin/python

# Copyright (C) 2011 by Yi Wang
# tririverwangyi@gmail.com
#
# This file is part of HepOrg.
#
# HepOrg is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# HepOrg is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with HepOrg.  If not, see <http://www.gnu.org/licenses/>.


import subprocess
import urllib.request
import sys

import refconf
import arxiv_parser
import inspire_parser
import org_fmt



def print_usage():
    usage = '''
Usage:

(a) heporg.py html_file_name

use html_file_name as input, the default tag is toread (thus generate default record file toread.org).

(b) heporg.py tag_name html_file_name

use html_file_name as input, and generate record file tag_name.org
'''
    print(usage)



def msg(logfile, message, quiet='F'):
    logfile.write(message + "\n")
    if quiet == 'F':
        print(message)
    return



def download_file(file_link, file_name):
    f = urllib.request.urlopen(file_link)    
    localFile = open(file_name, 'wb')
    localFile.write(f.read())
    localFile.close()
    return



def main(htm_file_name, org_file_name, 
         dl='T', open_reader='T'):

    cur_dir = refconf.dir_prefix
    pdf_dir = cur_dir + 'pdf/'
    org_dir = cur_dir + 'org/'

    logfile = open(cur_dir+'events.log', 'w') # 'a' for appending
    orgfile = open(org_dir+org_file_name, 'a')
    try:
        htmfile = open(htm_file_name)
    except IOError:
        msg(logfile, "Input file " + htm_file_name + " not found. Abort.")
        sys.exit(1)
    htm_string = htmfile.read()

    # try arxiv parser:
    msg(logfile,"Try arXiv parser ...")
    paper_data = arxiv_parser.get_data(htm_string)

    # try inspire parser:
    if paper_data['status'] != 'success':
        msg(logfile,"Try inspire parser ...")
        paper_data = inspire_parser.get_data(htm_string)

    if paper_data['status'] == 'success':
        msg(logfile,"File parsed successfully")
    else:
        msg(logfile,"Error: " + paper_data['status'])
        msg(logfile,"Abort")
        sys.exit(1)
        

    pdf_fn = org_fmt.file_name(paper_data)
    if pdf_fn != '':
        local_pdf_name = pdf_dir + pdf_fn
    else:
        local_pdf_name = ''

    
    msg(logfile,"Writing to" + org_dir + org_file_name)
    orgfile.write(org_fmt.output(paper_data, local_pdf_name))


    if local_pdf_name == '':
        msg(logfile,"No pdf_link, thus no file to download or open\nDone.")
        return


    if dl == 'T':
        msg(logfile,"Downloading " + local_pdf_name)
        download_file(paper_data['pdf_link'], local_pdf_name)


    if open_reader == 'T':
        msg(logfile,"Starting reader: " + refconf.pdf_reader)
        if refconf.pdf_reader_arg =='':
            subprocess.call([refconf.pdf_reader, local_pdf_name])
        else:
            subprocess.call([refconf.pdf_reader, 
                             refconf.pdf_reader_arg, local_pdf_name])
        
    msg(logfile,"Done.")

    logfile.close()
    orgfile.close()
    htmfile.close()



# main starts here

# examine passing-in parameter:

if len(sys.argv)==1:
    print_usage()
    sys.exit(1)
elif len(sys.argv)==2:
    org_file_name = 'toread.org'
    htm_file_name = sys.argv[1]
elif len(sys.argv)==3:
    org_file_name = sys.argv[1] + '.org'
    htm_file_name = sys.argv[2]
    
main(htm_file_name, org_file_name)
