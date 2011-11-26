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


import re


def get_data(inspire_page):

    # title
    title_find = re.findall(r'<title>(.+?) - HEP</title>',inspire_page)
    if title_find == []:
        return {'status':'FAIL -- title not found'}
    else:
       title = title_find[0]
    
    # arxiv number
    arxiv_num_find = re.findall(r'e-Print: <b>arXiv:(.+?) \[.+?]</b>',inspire_page)
    if arxiv_num_find == []:
        arxiv_num = 'not found'
    else:
       arxiv_num = arxiv_num_find[0]

    # get author
    authors_find = re.findall(r'<a class="authorlink" href=".+?">(.+?)</a>', inspire_page, re.DOTALL)
    if authors_find == []:
        return {'status':'FAIL -- authors line not found'}
    # write the author data in the same format as that in arxiv_parser
    authors = []
    for name in authors_find:
        split_name = re.findall(r'(.+) (.+)', name)
        authors.append((split_name[0][1],split_name[0][0]))

    # get abstract
    abstract_find = re.findall(r'Abstract: </strong>(.+?)</small><br />', inspire_page, re.DOTALL)
    if abstract_find == []:
        abstract = 'not found'
    else:
        abstract = abstract_find[0]
    
    # get abstract link
    abs_link_find = re.findall(r'"(http://arXiv.org/abs/.+?)">Abstract', inspire_page)
    if abs_link_find == []:
        abs_link = 'not found'
    else:
        abs_link = abs_link_find[0]

    # get pdf link
    pdf_link_find = re.findall(r'"(http://arXiv.org/pdf/.+?)">PDF', inspire_page)
    if pdf_link_find == []:
        pdf_link = 'not found'
    else:
        pdf_link = pdf_link_find[0]


    # get submit date
    submit_date_find = re.findall(r'Record created (....)-(..)-(..)', inspire_page)
    if submit_date_find == []:
        return {'status':'FAIL -- submit date not found'}
    else:
        submit_date = "{}_{}_{}".format\
            (submit_date_find[0][0],submit_date_find[0][1],submit_date_find[0][2])


    # get date of current version
    ver_date_find = re.findall(r', last modified (....)-(..)-(..)', inspire_page)
    if ver_date_find == []:
        return {'status':'FAIL -- current version date not found'}
    else:
        ver_date = "{}_{}_{}".format\
            (ver_date_find[0][0],ver_date_find[0][1],ver_date_find[0][2])


    # get journal reference
    journal_find = re.findall\
        (r'pp.\n<br /><br /><strong>(.+?)<', inspire_page)
    if journal_find == []:
        journal = 'no publication information'
    else:
        journal = journal_find[0]

    # get inspire link
    inspire_link_find = re.findall(r'Information  </a></li><li class=""><a href="(.+?)">References', inspire_page)
    if inspire_link_find == []:
        inspire_link = 'not found'
    else:
        inspire_link = inspire_link_find[0]


    return {'arxiv_num':arxiv_num, 'title':title, 
            'authors':authors, 
            'abstract':abstract, 
            'abs_link':abs_link,
            'pdf_link':pdf_link, 
            'version':'?',
            'submit_date':submit_date, 
            'ver_date':ver_date,
            'journal':journal,
            'inspire_link':inspire_link,
            'status':'success'}
