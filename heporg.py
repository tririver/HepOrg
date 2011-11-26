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


def err_exit(logfile, message, notify='F'):
    if notify !='F':
        subprocess.call(["notify-send", "--hint=int:transient:1", 
                         "HepOrg: " + message])
    msg(logfile, message)
    sys.exit(1)



def download_file(file_link, file_name):
    f = urllib.request.urlopen(file_link)    
    localFile = open(file_name, 'wb')
    localFile.write(f.read())
    localFile.close()
    return



def main(htm_file_name, org_file_name, 
         dl='T', open_reader='T', notify='F'):

    cur_dir = refconf.dir_prefix
    pdf_dir = cur_dir + 'pdf/'
    org_dir = cur_dir + 'org/'

    logfile = open(cur_dir+'events.log', 'w') # 'a' for appending
    orgfile = open(org_dir+org_file_name, 'a')
    try:
        htmfile = open(htm_file_name)
    except IOError:
        err_exit(logfile, 
                 "Error: input file " + htm_file_name + " not found. Abort."
                 , notify)
    htm_string = htmfile.read()

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
        err_exit(logfile,"Error: " + paper_data['status'] + ". Abort", notify)
        

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

if refconf.notify !='F':
    subprocess.call(["notify-send", "--hint=int:transient:1",
                     "HepOrg: start parsing and downloading..."])

if len(sys.argv)==1:
    print_usage()
    err_exit('', "Error: found no input argument -- exit.",
             notify=refconf.notify)
elif len(sys.argv)==2:
    org_file_name = 'toread.org'
    htm_file_name = sys.argv[1]
elif len(sys.argv)==3:
    org_file_name = sys.argv[1] + '.org'
    htm_file_name = sys.argv[2]
    
main(htm_file_name, org_file_name, notify=refconf.notify, dl='T')

if refconf.notify !='F':
    subprocess.call(["notify-send", "--hint=int:transient:1",
                     "HepOrg: Done :)"])
