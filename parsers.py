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



def get(re_str, page, re_option=0, fmt=''):
    try_search = re.findall(re_str, page, re_option)
    if try_search ==[]:
        return 'not found'
    elif fmt == '':
        return try_search[0]
    else:
        return fmt(try_search)
        
        

def arxiv(page):

    title = get(r'<title>\[.+?] (.+?)</title>', 
                      page, re_option=re.DOTALL)
    if title == 'not found':
        return {'status':'try arxiv failed -- title not found'}

    arxiv_num = get(r'<title>\[(.+?)] .+?</title>', 
                      page, re_option=re.DOTALL)

    abstract = get(r'<blockquote class="abstract">\n<span class="descriptor">Abstract:</span> (.+)\n</blockquote>', 
                      page, re_option=re.DOTALL)    
    if abstract == 'not found':
        return {'status':'try arxiv failed -- abstract not found'}

    abs_link = get(r'dc:identifier="(.+?)"', page)

    pdf_link = get(r'citation_pdf_url" content="(.+?)" />', page)
    if pdf_link == 'not found':
        return {'status':'try arxiv failed -- pdf_link not found'}

    version = get(r'<b>\[v(.+?)]</b>', page)

    journal = get(r'td class="tablecell jref">(.+?)</td>', page)

    journal_link = get(r'(http://dx.doi.org/.+?)"', page)

    inspire_link = get('Citations</h3><ul><li><a href="(.+?)">INSPIRE',
                       page)

    authors = get(r'<meta name="citation_author" content="(.+?), (.+?)" />',
                  page, fmt=lambda res: res)

    submit_date = get(r'citation_date" content="(.+?)/(.+?)/(.+?)"',
                      page, fmt=lambda res:
                          "{}_{}_{}".format(res[0][0],res[0][1],res[0][2]))

    ver_date = get(r'citation_online_date" content="(.+?)/(.+?)/(.+?)"',
                      page, fmt=lambda res:
                          "{}_{}_{}".format(res[0][0],res[0][1],res[0][2]))

    return {'page':'arxiv', 'arxiv_num':arxiv_num, 'title':title, 
            'authors':authors, 'abstract':abstract, 
            'abs_link':abs_link, 'pdf_link':pdf_link, 'version':version,
            'submit_date':submit_date, 'ver_date':ver_date,
            'journal':journal, 'journal_link':journal_link,
            'inspire_link':inspire_link,
            'status':'success'}




def inspire(page):

    title = get(r'<title>(.+?) - HEP</title>', page)
    if title == 'not found':
        return {'status':'try inspire failed -- title not found'}

    arxiv_num = get(r'e-Print: <b>arXiv:(.+?) \[.+?]</b>', page)

    abstract = get(r'Abstract: </strong>(.+?)</small><br />', 
                      page, re_option=re.DOTALL)    

    abs_link = get(r'"(http://arXiv.org/abs/.+?)">Abstract', page)

    pdf_link = get(r'"(http://arXiv.org/pdf/.+?)">PDF', page)

    submit_date = get(r'Record created (....)-(..)-(..)', page, fmt=lambda
                      res: "{}_{}_{}".format(res[0][0],res[0][1],res[0][2]))

    ver_date = get(r', last modified (....)-(..)-(..)', page, fmt=lambda 
                   res: "{}_{}_{}".format(res[0][0],res[0][1],res[0][2]))


    journal = get(r'pp.\n<br /><br /><strong>(.+?)<', page)

    journal_link = get(r'(http://dx.doi.org/.+?)"', page)

    inspire_link = get(r'Information  </a></li><li class=""><a href="(.+?)">References', page)

    # write the author data in the same format as that in arxiv_parser
    # like [(family_name, given_name), (family_name, given_name), ...]

    def author_fmt(res):
        authors = []
        for name in res:
            split_name = re.findall(r'(.+) (.+)', name)
            authors.append((split_name[0][1],split_name[0][0]))
        return authors

    authors = get(r'<a class="authorlink" href=".+?">(.+?)</a>', page, 
                  re_option=re.DOTALL, fmt=author_fmt)
    if authors == 'not found':
        return {'status':'try inspire failed -- authors not found'}

    return {'page':'inspire', 'arxiv_num':arxiv_num, 'title':title, 
            'authors':authors, 'abstract':abstract, 'abs_link':abs_link,
            'pdf_link':pdf_link, 'version':'?',
            'submit_date':submit_date, 'ver_date':ver_date,
            'journal':journal,'inspire_link':inspire_link,
            'journal_link':journal_link,
            'status':'success'}
