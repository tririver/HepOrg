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


import refconf
import arxiv_parser
import inspire_parser
import org_fmt


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
    htmfile = open(htm_file_name)
    htm_string = htmfile.read()

    # try arxiv parser:
    logfile.write("Try arXiv parser ... \n")
    paper_data = arxiv_parser.get_data(htm_string)

    # try inspire parser:
    if paper_data['status'] == 'success':
        logfile.write("ArXiv parser returned successfully. \n")
    else:
        logfile.write("Try inspire parser ... \n")
        paper_data = inspire_parser.get_data(htm_string)

    if paper_data['status'] == 'success':
        logfile.write("Inspire parser returned successfully. \n")
    else:        
        logfile.write("Error: " + paper_data['status'] + "\n")
        logfile.write("Abort. \n")
        return
        

    pdf_fn = org_fmt.file_name(paper_data)
    if pdf_fn != '':
        local_pdf_name = pdf_dir + pdf_fn
    else:
        local_pdf_name = ''

    
    logfile.write("Writing to" + org_dir + org_file_name + "\n")
    orgfile.write(org_fmt.output(paper_data, local_pdf_name))


    if local_pdf_name == '':
        logfile.write("No pdf_link, thus no file to download or open\nDone.\n")
        return


    if dl == 'T':
        logfile.write("Downloading " + local_pdf_name + "\n")
        download_file(paper_data['pdf_link'], local_pdf_name)


    if open_reader == 'T':
        logfile.write("Starting reader: '" + refconf.pdf_reader + "'\n")
        if refconf.pdf_reader_arg =='':
            subprocess.call([refconf.pdf_reader, local_pdf_name])
        else:
            subprocess.call([refconf.pdf_reader, 
                             refconf.pdf_reader_arg, local_pdf_name])
        
    logfile.write("Done.\n")

    logfile.close()
    orgfile.close()
    htmfile.close()
