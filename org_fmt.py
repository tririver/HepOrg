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


def file_name(paper_data):
    if paper_data['pdf_link'] == 'not found':
        return ''
    fn = ''
    for author in paper_data['authors']:
        fn = fn + author[0] + '_'
    arxiv_num_fmt = "arXiv_" \
        + paper_data['arxiv_num'].replace('.','_').replace('/','_') \
        + "_v" + paper_data['version']
    fn = fn + arxiv_num_fmt + '.pdf'
    return fn



def output(paper_data, local_pdf_name):
    title = paper_data['title']
    # crop title if too long
    len_limit = 70
    if len(paper_data['arxiv_num']) + len(title) > len_limit:
        title = title[:len_limit-len(paper_data['arxiv_num'])]

    # org mode grammar: [[link][description]]
    # thus output here: xxxx.xxxx (link to abs)  title (link to pdf)
    if paper_data['abs_link'] != 'not found':
        out_str = '** [['+ paper_data['abs_link'] + '][' \
            + paper_data['arxiv_num'] + ']]  [[' \
            + r'file://' + local_pdf_name + '][' + title + ']]\n'
    else:
        out_str = '** [['+ paper_data['inspire_link'] + '][' \
            + paper_data['journal'] + ']]  ' + title + '\n'

    out_str = out_str + ':PROPERTIES:\n'
    out_str = out_str + 'TITLE:  ' + paper_data['title'] + '\n\n'

    # write author list in a more readable form
    authors = ''
    for name in paper_data['authors']:
        authors = authors + name[1] + ' ' + name[0] + ', '
    authors = authors[:-2]
    out_str = out_str +'AUTHORS:  ' + authors + '\n\n'
    out_str = out_str +'ABSTRACT:\n' + paper_data['abstract'] + '\n\n'
    out_str = out_str +'VERSION:  v' + paper_data['version'] + ', ' \
              + paper_data['ver_date'] + '  (first version '\
              + paper_data['submit_date'] + ')\n\n'
    out_str = out_str + 'JOURNAL:  ' + paper_data['journal'] + '\n'
    out_str = out_str + ':END:\n'

    return out_str
