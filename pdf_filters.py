import subprocess
import re

def decide_bb(str):
    bb_str = re.findall(r'%%BoundingBox: (.+?) (.+?) (.+?) (.+?)\n', str)
    # for xmin, the first page is not considered because
    # on arxiv, there is always arXiv number on the boundary
    # for ymin, also there is sometimes a preprint number
    bb_xmin = min([eval(page[0]) for page in bb_str[1:]])
    bb_ymin = min([eval(page[1]) for page in bb_str[1:]])
    bb_xmax = max([eval(page[2]) for page in bb_str])
    bb_ymax = max([eval(page[3]) for page in bb_str])
    return ' --bbox "{} {} {} {}" '.format(bb_xmin, bb_ymin, bb_xmax, bb_ymax)

def pdfcrop(fn):
    try_crop = subprocess.getoutput('pdfcrop --verbose '+fn+' /dev/null')
    try_bb = decide_bb(try_crop)
    eval_str = 'pdfcrop'+try_bb+fn+' /tmp/tmp_by_pdfcrop.pdf'
    subprocess.getoutput(eval_str)
    subprocess.getoutput('cp /tmp/tmp_by_pdfcrop.pdf '+fn)

# run a test
# pdfcrop('/tmp/test.pdf')



list = [('pdfcrop', pdfcrop)]
