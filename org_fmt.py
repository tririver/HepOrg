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



def output(paper_data, local_pdf_name, org_dir_file_name):

    # determine what to write in the first link area
    if paper_data['abs_link'] == 'not found':
        num = paper_data['journal']
        link = paper_data['inspire_link']
    else:
        num = paper_data['arxiv_num']
        link = paper_data['abs_link']

    if local_pdf_name != '':
        pdf_link = local_pdf_name
    else:
        pdf_link = paper_data['journal_link']

    # write author list in a more readable form
    authors = ''
    for name in paper_data['authors']:
        authors = authors + name[1] + ' ' + name[0] + ', '
    authors = authors[:-2]

    org_append_str = r'''**[[{0}][{1}]]  [[{2}][{3}]]
:PROPERTIES:
TITLE: {4}

AUTHOR: {5}

ABSTRACT:
{6}

VERSION: v{7}, {8} (first version: {9})

JOURNAL: {10}
:END:
'''.format(link, num, pdf_link,
           paper_data['title'][:70-len(num)],
           paper_data['title'], authors, paper_data['abstract'],
           paper_data['version'][:2], 
           paper_data['ver_date'], paper_data['submit_date'],
           paper_data['journal']
           ).replace('not found', '')
    orgfile = open(org_dir_file_name, 'a')
    orgfile.write(org_append_str)
    orgfile.close()
    return
