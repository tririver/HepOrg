#! /usr/bin/python3

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

import parsers
import pdf_filters
import org_fmt

try:
    import refconf
except ImportError:
    print("Error: refconf.py not found. Please run setup.sh first.")
    sys.exit(1)



def print_usage():
    print('''
Usage:

(a) heporg.py html_file_name

use html_file_name as input, the default tag is toread (thus generate default record file toread.org).

(b) heporg.py tag_name html_file_name

use html_file_name as input, and generate record file tag_name.org
''')



def msg(message, quiet='F', notify='F'):
    logfile = open(refconf.dir_prefix+'events.log', 'a')
    logfile.write(message + "\n")
    logfile.close()
    if quiet == 'F':
        print(message)
    if notify !='F':
        subprocess.call(["notify-send", "--hint=int:transient:1", 
                         "HepOrg: " + message])
    return



def code_exit(message, code = 1):
    msg(message, notify = refconf.notify)
    sys.exit(code)



def download_pdf(file_link, local_pdf_name):
    if refconf.download != 'T' or local_pdf_name == '':
        code_exit('HepOrg: written to '+org_file_name+', no pdf generated.', 0)
    msg("Downloading " + local_pdf_name)
    f = urllib.request.urlopen(file_link)    
    localFile = open(local_pdf_name, 'wb')
    localFile.write(f.read())
    localFile.close()
    return



def check_input(argv):
    if len(argv)==1:
        print_usage()
        code_exit('', "Error: found no input argument -- exit.")
    elif len(argv)==2:
        org_file_name = refconf.dir_prefix + 'org/toread.org'
        htm_file_name = argv[1]
    elif len(argv)==3:
        org_file_name = refconf.dir_prefix + 'org/' + argv[1] + '.org'
        htm_file_name = argv[2]
    msg("Start working from "+htm_file_name
        +" to "+org_file_name, notify = refconf.notify)

    try:
        htmfile = open(htm_file_name)
    except IOError:
        code_exit("Error: input file " + htm_file_name + " not found. Abort.")
    htm_string = htmfile.read()
    htmfile.close()

    return (org_file_name, htm_file_name, htm_string)



def try_parsers(htm_string):
    # try parsers defined in parsers.parser
    for parser in refconf.parser_list:
        msg("Try " + parser[0] + " parser ...")
        paper_data = parser[1](htm_string)
        if paper_data['status'] == 'success':
            msg("File parsed successfully")
            break
        else:
            msg(parser[0] + " cannot parse page correctly.")
        
    # if none of the parsers work:
    if paper_data['status'] != 'success':
        code_exit("Error: " + paper_data['status'] + ". Abort")

    return paper_data



def apply_pdf_filters(local_pdf_name):
    for pdf_filter in refconf.pdf_filter_list:
        msg("Applying "+pdf_filter[0])
        pdf_filter[1](local_pdf_name)
    return



def determine_pdf_name(paper_data):
    if paper_data['pdf_link'] == 'not found':
        msg("Found no pdf_link, thus no file to download or open")
        return ''
    fn = refconf.dir_prefix + 'pdf/'
    for author in paper_data['authors']:
        fn = fn + author[0] + '_'
    arxiv_num_fmt = "arXiv_" \
        + paper_data['arxiv_num'].replace('.','_').replace('/','_')
    fn = fn + arxiv_num_fmt + '.pdf'
    return fn



def open_reader(local_pdf_name):
    if refconf.open_reader != 'T' or local_pdf_name == '':
        return
    msg("Starting reader: " + refconf.pdf_reader)
    if refconf.pdf_reader_arg =='':
        subprocess.call([refconf.pdf_reader, local_pdf_name])
    else:
        subprocess.call([refconf.pdf_reader, 
                         refconf.pdf_reader_arg, local_pdf_name])



# main starts here

# Initialization: set dirs and file names
org_file_name, htm_file_name, htm_string = check_input(sys.argv)

# parse the htm file
paper_data = try_parsers(htm_string)

# determine pdf file name
local_pdf_name = determine_pdf_name(paper_data)

# write .org file
msg("Writing to" + org_file_name)
org_fmt.output(paper_data, local_pdf_name, org_file_name)

# download pdf
download_pdf(paper_data['pdf_link'], local_pdf_name)

# open reader
open_reader(local_pdf_name)

# apply pdf filters after opening reader because it may take a long time
apply_pdf_filters(local_pdf_name)

code_exit('HepOrg: Generated '+local_pdf_name+' and '+org_file_name, 0)
