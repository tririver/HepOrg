import subprocess
import re

# determine boundary boxes, called by pdfcrop
def decide_bb(str):
    bdry = 5
    bb_str = re.findall(r'%%BoundingBox: (.+?) (.+?) (.+?) (.+?)\n', str)
    # for xmin, the first page is not considered because
    # on arxiv, there is always arXiv number on the boundary
    # for ymax, also there is sometimes a preprint number
    bb_xmin = min([eval(page[0]) for page in bb_str[1:]]) - bdry
    bb_ymin = min([eval(page[1]) for page in bb_str]) - bdry
    bb_xmax = max([eval(page[2]) for page in bb_str]) + bdry
    bb_ymax = max([eval(page[3]) for page in bb_str[1:]]) + bdry
    return ' --bbox "{} {} {} {}" '.format(bb_xmin, bb_ymin, bb_xmax, bb_ymax)

def pdfcrop(fn):
    try_crop = subprocess.getoutput('pdfcrop --verbose '+fn+' /dev/null')
    try_bb = decide_bb(try_crop)
    eval_str = 'pdfcrop'+try_bb+fn+' /tmp/tmp_by_pdfcrop.pdf'
    subprocess.getoutput(eval_str)
    subprocess.getoutput('cp /tmp/tmp_by_pdfcrop.pdf '+fn)
