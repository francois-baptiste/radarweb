import math

from radarplot.CIKM import CIKM
from jinja2 import Environment, FileSystemLoader
import os

TEMPLATE_DIR = 'templates'
ITEMS_PER_PAGE = 60
ANCHOR_PAG = 9
WEB_DIR = 'web'
IMG_DIR = WEB_DIR + '/img'
VID_DIR = WEB_DIR + '/vid'
INDEX_PAGE_NAME = 'index'
VIDEO_PAGE_NAME = 'video'

template = Environment(
    autoescape=False,
    loader=FileSystemLoader(TEMPLATE_DIR),
    trim_blocks=False)
cikm0 = CIKM('../data/train1.txt', '../data/train1.index')
cikm1 = CIKM('../data/train2.txt', '../data/train2.index')

radar_data = []
pagesn = math.ceil(cikm0.getSize() / ITEMS_PER_PAGE) # number of pages

def pagination (n, anchor, size):
    """Returns a list with the pagination numbers.
    n is the current page, anchor is the number of pages in
    the pagination bar and size is the total number of pages to
    be paginated. Page list start at 1 and ends at size."""
    padding = int(anchor / 2)
    if (n > padding and n <= (size - padding)):
        a = n - padding
        b = n + padding
    elif (n <= padding):
        a = 1
        b = anchor
    elif (n > (size - padding)):
        a = size - anchor + 1
        b = size
    return range(a, b + 1)

for (i, (radar0, radar1)) in enumerate(zip(cikm0.getAllRadars(reversed=True),cikm1.getAllRadars(reversed=True))):
    print("Reading radar {}".format(radar0.getID()))
    posinpage = i % ITEMS_PER_PAGE     # postion of the image in the page
    page = int(i / ITEMS_PER_PAGE)
    
    meta = {}
    meta["thumbnail"] = "img/{}.png".format(radar0.getID())
    meta["id"] = radar0.getID()
    meta["label"] = radar0.getLabel()
    meta["video0"] = "vid/0_{}".format(radar0.getID())
    meta["video1"] = "vid/1_{}".format(radar0.getID())
    meta["videohtml"] = "vid{}".format(radar0.getID())
    radar_data.append(meta)

    os.makedirs(IMG_DIR, exist_ok=True)
    radar0.plotThumbnail('{}/{}'.format(IMG_DIR, radar0.getID()))
    os.makedirs(VID_DIR, exist_ok=True)
    radar0.plot('{}/0_{}.mp4'.format(VID_DIR, radar0.getID()))
    os.makedirs(VID_DIR, exist_ok=True)
    radar1.plot('{}/1_{}.mp4'.format(VID_DIR, radar1.getID()))

    print('Rendering video page {}'.format(page + 1))
    with open('{}/{}.html'.format(WEB_DIR, meta["videohtml"]), 'w') as f:
        tpl = template.get_template('video-basic.html')
        html = tpl.render(meta=meta,
                          pagination=pagination(i + 1, ANCHOR_PAG, pagesn),
                          current=i + 1,
                          last=pagesn - 1)
        f.write(html)
               
    # if we are in the last element of the page we render the current page
    if (posinpage == ITEMS_PER_PAGE - 1):
        print('Rendering index page {}'.format(page + 1))
        with open('{}/{}{}.html'.format(WEB_DIR, INDEX_PAGE_NAME, str(page)), 'w') as f:
            tpl = template.get_template('index-basic.html')
            html = tpl.render(radars = radar_data,
                              pagination = pagination(page + 1, ANCHOR_PAG, pagesn),
                              current = page + 1,
                              last = pagesn - 1)
            f.write(html)
        radar_data = []
