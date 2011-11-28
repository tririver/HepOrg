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

try:
    import refconf
except ImportError:
    print("Error: refconf.py not found. Please run setup.sh first.")
    sys.exit(1)

import parsers
import pdf_filters
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
    if logfile!= '':
        logfile.write(message + "\n")
    if quiet == 'F':
        print(message)
    return



def code_exit(logfile, message, code = 1):
    if refconf.notify !='F':
        subprocess.call(["notify-send", "--hint=int:transient:1", 
                         "HepOrg: " + message])
    msg(logfile, message)
    logfile.close()
    sys.exit(code)



def download_pdf(file_link, local_pdf_name):
    if refconf.download != 'T' or local_pdf_name == '':
        code_exit(logfile, 
                  'HepOrg: written to '+org_file_name+', no pdf generated.', 0)
    msg(logfile,"Downloading " + local_pdf_name)
    f = urllib.request.urlopen(file_link)    
    localFile = open(local_pdf_name, 'wb')
    localFile.write(f.read())
    localFile.close()
    return



def check_input(argv):
    cur_dir = refconf.dir_prefix
    pdf_dir = cur_dir + 'pdf/'
    org_dir = cur_dir + 'org/'

    if len(argv)==1:
        print_usage()
        code_exit('', "Error: found no input argument -- exit.")
    elif len(argv)==2:
        org_file_name = 'toread.org'
        htm_file_name = argv[1]
    elif len(argv)==3:
        org_file_name = argv[1] + '.org'
        htm_file_name = argv[2]
    if refconf.notify !='F':
        subprocess.call(["notify-send", "--hint=int:transient:1",
                         "HepOrg: From "+htm_file_name+" to "+org_file_name])
    return (cur_dir, pdf_dir, org_dir, org_file_name, htm_file_name)



def try_parsers(htm_string, logfile):
    # try parsers defined in parsers.parser
    for parser in parsers.list:
        msg(logfile,"Try " + parser[0] + " parser ...")
        paper_data = parser[1](htm_string)
        if paper_data['status'] == 'success':
            msg(logfile,"File parsed successfully")
            break
        else:
            msg(logfile, parser[0] + " cannot parse page correctly.")
        
    # if none of the parsers work:
    if paper_data['status'] != 'success':
        code_exit(logfile,"Error: " + paper_data['status'] + ". Abort")

    return paper_data



def apply_pdf_filters(local_pdf_name, logfile):
    for pdf_filter in pdf_filters.list:
        msg(logfile,"Applying "+pdf_filter[0])
        pdf_filter[1](local_pdf_name)
    return



def determine_pdf_name(paper_data):
    pdf_fn = org_fmt.file_name(paper_data)
    if pdf_fn != '':
        local_pdf_name = pdf_dir + pdf_fn
    else:
        local_pdf_name = ''
        msg(logfile,"No pdf_link, thus no file to download or open")
    return local_pdf_name



def open_reader(local_pdf_name):
    if refconf.open_reader != 'T' or local_pdf_name == '':
        return
    msg(logfile,"Starting reader: " + refconf.pdf_reader)
    if refconf.pdf_reader_arg =='':
        subprocess.call([refconf.pdf_reader, local_pdf_name])
    else:
        subprocess.call([refconf.pdf_reader, 
                         refconf.pdf_reader_arg, local_pdf_name])



# main starts here

# Initialization: set dirs and file names
cur_dir, pdf_dir, org_dir, org_file_name, htm_file_name = check_input(sys.argv)

# open the log, org and htm files
logfile = open(cur_dir+'events.log', 'w') # 'a' for appending
orgfile = open(org_dir+org_file_name, 'a')
try:
    htmfile = open(htm_file_name)
except IOError:
    code_exit(logfile, 
             "Error: input file " + htm_file_name + " not found. Abort.")
htm_string = htmfile.read()

# parse the htm file
paper_data = try_parsers(htm_string, logfile)

# determine pdf file name
local_pdf_name = determine_pdf_name(paper_data)

# write .org file
msg(logfile,"Writing to" + org_dir + org_file_name)
orgfile.write(org_fmt.output(paper_data, local_pdf_name))

# download pdf
download_pdf(paper_data['pdf_link'], local_pdf_name)

# open reader
open_reader(local_pdf_name)

# apply pdf filters after opening reader because it may take a long time
apply_pdf_filters(local_pdf_name, logfile)

code_exit(logfile, 
          'HepOrg: Generated '+local_pdf_name+' and '+org_file_name, 0)

# clean up (log file is closed inside code_exit)
orgfile.close()
htmfile.close()
