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


def get_data(arxiv_page):

    # get arxiv number and title
    title_block_re = re.compile(r'<title>\[(.+?)] (.+?)</title>', re.DOTALL)
    title_block = re.findall(title_block_re, arxiv_page)
    if title_block == []:
        return {'status':'FAIL -- title line not found'}
    arxiv_num = title_block[0][0]
    title = title_block[0][1]

    # get author
    authors = re.findall(r'<meta name="citation_author" content="(.+?), (.+?)" />', arxiv_page)
    if authors == []:
        return {'status':'FAIL -- authors line not found'}

    # get abstract
    abstract_re = re.compile(r'<blockquote class="abstract">\n<span class="descriptor">Abstract:</span> (.+)\n</blockquote>', re.DOTALL)
    abstract_find = re.findall(abstract_re, arxiv_page)
    if abstract_find == []:
        return {'status':'FAIL -- abstract not found'}
    else:
        abstract = abstract_find[0]
    
    # get abstract link
    abs_link_find = re.findall(r'dc:identifier="(.+?)"', arxiv_page)
    if abs_link_find == []:
        return {'status':'FAIL -- abstract link not found'}
    else:
        abs_link = abs_link_find[0]

    # get pdf link
    pdf_link_find = re.findall(r'citation_pdf_url" content="(.+?)" />', arxiv_page)
    if pdf_link_find == []:
        return {'status':'FAIL -- pdf link not found'}
    else:
        pdf_link = pdf_link_find[0]


    # get version
    version_find = re.findall(r'<b>\[v(.+?)]</b>', arxiv_page)
    if version_find == []:
        return {'status':'FAIL -- paper version not found'}
    else:
        version = version_find[0]


    # get submit date
    submit_date_find = re.findall\
        (r'citation_date" content="(.+?)/(.+?)/(.+?)"'\
             , arxiv_page)
    if submit_date_find == []:
        return {'status':'FAIL -- submit date not found'}
    else:
        submit_date = "{}_{}_{}".format\
            (submit_date_find[0][0],submit_date_find[0][1],submit_date_find[0][2])


    # get date of current version
    ver_date_find = re.findall\
        (r'citation_online_date" content="(.+?)/(.+?)/(.+?)"'\
             , arxiv_page)
    if ver_date_find == []:
        return {'status':'FAIL -- current version date not found'}
    else:
        ver_date = "{}_{}_{}".format\
            (ver_date_find[0][0],ver_date_find[0][1],ver_date_find[0][2])


    # get journal reference
    journal_find = re.findall\
        (r'td class="tablecell jref">(.+?)</td>', arxiv_page)
    if journal_find == []:
        journal = 'no publication information'
    else:
        journal = journal_find[0]


    # get inspire link
    inspire_link_find = re.findall('Citations</h3><ul><li><a href="(.+?)">INSPIRE', arxiv_page)
    if inspire_link_find == []:
        inspire_link = 'not found'
    else:
        inspire_link = inspire_link_find[0]


    return {'arxiv_num':arxiv_num, 'title':title, 
            'authors':authors, 
            'abstract':abstract, 
            'abs_link':abs_link,
            'pdf_link':pdf_link, 
            'version':version,
            'submit_date':submit_date, 
            'ver_date':ver_date,
            'journal':journal,
            'inspire_link':inspire_link,
            'status':'success'}
