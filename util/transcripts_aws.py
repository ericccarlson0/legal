import boto3
import cv2
import io
import numpy as np
import os
import re
import time

from util.x_logging import log_execution
from pdf2image import convert_from_path, pdfinfo_from_path
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt

REGION = 'us-west-2'
PLA_BUCKET = 'deposition-pdf-plaintiff'

MINISCULE_TIME = 0.5
SMALL_TIME = 2

TEMP_DIR = os.path.join(os.getcwd(), f'temp-{__name__}')
if not os.path.isdir(TEMP_DIR):
    os.mkdir(TEMP_DIR)

def show_bbox(draw, bbox, w: int, h: int, color: str):
    left = w * bbox['Left']
    top = h * bbox['Top']

    draw.rectangle([left, top, left + (w * bbox['Width']), top + (h * bbox['Height'])], outline=color)

def show_selected(draw, bbox, w: int, h: int, color: str):
    left = w * bbox['Left']
    top = h * bbox['Top']

    draw.rectangle([left, top, left + (w * bbox['Width']), top + (h * bbox['Height'])], fill=color)

@log_execution
def textract_bucket(bucket: str, fname: str):
    textract = boto3.client('textract', region_name=REGION)

    resp = textract.start_document_text_detection(DocumentLocation={'S3Object': {'Bucket': bucket, 'Name': fname}})
    job_id = resp['JobId']

    resp = textract.get_document_text_detection(JobId=job_id)
    c = 0
    while resp['JobStatus'] != 'SUCCEEDED':
        time.sleep(SMALL_TIME)
        resp = textract.get_document_text_detection(JobId=job_id)

        c += 1
        print('check', c)

    next_token = resp['NextToken'] if 'NextToken' in resp else None
    pages = []
    pages.append(resp)
    c = 0
    while next_token:
        time.sleep(MINISCULE_TIME)
        resp = textract.get_document_text_detection(JobId=job_id, NextToken=next_token)
        pages.append(resp)
        next_token = resp['NextToken'] if 'NextToken' in resp else None

        c += 1
        print('page', c)

    return pages

def text_has_page_number(s: str) -> bool:
    return re.search(r"Page \d+", s)

def text_is_number(s: str) -> bool:
    return re.search(r"\d+", s)

MIN_BOUNDING_BOX_PROPORTION = 0.65
def divide_into_quarters(im_arr: np.ndarray):
    assert im_arr.ndim == 2

    edges = cv2.Canny(im_arr, 64, 127, apertureSize=3, L2gradient=True)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
    max_contour = max(contours, key=cv2.contourArea)
    h, w = im_arr.shape
    c_x, c_y, c_w, c_h = cv2.boundingRect(max_contour)

    if c_w < w * MIN_BOUNDING_BOX_PROPORTION or c_h < h * MIN_BOUNDING_BOX_PROPORTION:
        return None

    # A typical result would be (250, 140, 1250, 1850) or (250, 140, 1350, 1930)
    #   for image size 1700, 2200 (79.3% h, 87.5% w)
    tl_img = im_arr[c_y : c_y + (c_h // 2), c_x : c_x + (c_w // 2)]
    bl_img = im_arr[c_y + (c_h // 2) : c_y + c_h, c_x : c_x + (c_w // 2)]
    tr_img = im_arr[c_y : c_y + (c_h // 2), c_x + (c_w // 2) : c_x + c_w]
    br_img = im_arr[c_y + (c_h // 2) : c_y + c_h, c_x + (c_w // 2) : c_x + c_w]

    return tl_img, bl_img, tr_img, br_img

# return whether four or more pages out of the first ten are divided into 'Page X', 'Page X+1', 'Page X+2', 'Page X+3'
@log_execution(True)
def check_begin_for_quarters(fpath: str) -> int:
    textract = boto3.client('textract', region_name=REGION)

    quad_c = 0 # count of pages with four page numbers ('Page X')
    f_page_quad = -1 # first page with four page numbers ('Page X')
    for i in range(1, 10):
        im = convert_from_path(fpath, first_page=i, last_page=i, grayscale=True)[0]

        im_bytesio = io.BytesIO()
        im.save(im_bytesio, format='PNG')

        resp = textract.detect_document_text(Document={'Bytes': im_bytesio.getvalue()})
        
        blocks = resp['Blocks']
        blocks = [bl for bl in blocks if bl['BlockType'] == 'LINE']

        page_n_c = 0
        for bl in blocks:
            txt = bl['Text']
            if text_has_page_number(txt):
                page_n_c += 1
        
        if page_n_c >= 4:
            quad_c += 1
            if f_page_quad < 0:
                f_page_quad = i
    
    return f_page_quad if quad_c > 4 else -1

# TODO?
def arr_to_png_bytes(im_arr: np.ndarray):
    assert im_arr.ndim == 2

    im_pil = Image.fromarray(im_arr)
    im_bytesio = io.BytesIO()
    im_pil.save(im_bytesio, format='PNG')

    return im_bytesio.getvalue()

# TODO?
def textract_page(textract, im):
    im_bytesio = io.BytesIO()
    im.save(im_bytesio, format='PNG')
    im_bytes = im_bytesio.getvalue()
    
    return textract.detect_document_text(Document={'Bytes': im_bytes})

# TODO?
def textract_quarters_page(textract, im):
    im_arr = np.asarray(im)
    pages = []

    quarter_arrs = divide_into_quarters(im_arr)
    if not quarter_arrs:
        return None

    for arr in quarter_arrs:
        im_bytes = arr_to_png_bytes(arr)
        resp = textract.detect_document_text(Document={'Bytes': im_bytes})
        pages.append(resp)

    return pages

@log_execution(True)
def textract_pdf_to_image(fpath: str):
    textract = boto3.client('textract', region_name=REGION)

    pdfinfo = pdfinfo_from_path(fpath)
    n_pages = pdfinfo['Pages']
    # print(n_pages, 'pages')
    f_page_quad = check_begin_for_quarters(fpath)
    print('f_page_quad', f_page_quad)
    is_quarters = f_page_quad > 0

    pages = []
    for i in range(n_pages):
        print(i+1, '(textract)')
        im = convert_from_path(fpath, first_page=i+1, last_page=i+1, grayscale=True)[0]

        if not is_quarters:
            pages.append(textract_page(textract, im))
        elif i >= f_page_quad:
            responses = textract_quarters_page(textract, im)
            if responses:
                pages = pages + responses

    return pages

def transcript_from_textract(pages) -> str:
    transcript_arr = []
    for page in pages:
        for block in page['Blocks']:
            if block['BlockType'] == 'LINE':
                s = block['Text']
                if not text_is_number(s):
                    transcript_arr.append(s)
    
    ret = ' '.join(transcript_arr)
    ret = re.sub(r'\s+', ' ', ret)
    return ret

# PRINT INFO

def print_lines(blocks):
    line_blocks = [bl for bl in blocks if bl['BlockType'] == 'LINE']
    for bl in line_blocks:
        h1 = bl['Geometry']['Polygon'][0]['Y']
        h2 = bl['Geometry']['Polygon'][3]['Y']
        print('No Text' if 'Text' not in bl else bl['Text'])
        print(f'\t{h1:.4f} to {h2:.4f}')

def print_box(block):
    t_l, t_r, b_l, b_r = block['Geometry']['Polygon']
    t = (t_l['Y'] + t_r['Y']) / 2
    print(f'top:\t{t:.4f}')
    b = (b_l['Y'] + b_r['Y']) / 2
    print(f'bottom:\t{b:.4f}')
    l = (t_l['X'] + b_l['X']) / 2
    print(f'left:\t{l:.4f}')
    r = (t_r['X'] + b_r['X']) / 2
    print(f'right:\t{r:.4f}')

# There is lot of high-powered AI, and then there is the issue of trying to find the optimal way to cut out the line
# numbers on the side. Because we do not have multi-modal models available yet.
# .1210 - .1280, .1389 - .1508, .1629 - .1702, .190-.200, 
def print_numbers_x(blocks, print_all=True):
    line_blocks = [bl for bl in blocks if bl['BlockType'] == 'LINE']
    s = 0 # SUM
    c = 0 # COUNT
    for bl in line_blocks:
        if 'Text' not in bl:
            continue
        line_split = bl['Text'].split(' ')
        if len(line_split) > 1 or not line_split[0].isdigit():
            continue
        
        if print_all:
            print(f'{l:.4f}')
        t_l, _, b_l, _ = bl['Geometry']['Polygon']
        l = (t_l['X'] + b_l['X']) / 2
        c += 1
        s += l
    
    if c == 0:
        print('No numbers?')
    else:
        avg = s / c
        print(f'avg: {avg:.4f}')

def show_im_w_blocks(fpath: str, pages, page_n: int):
    im = convert_from_path(fpath, dpi=200, first_page=page_n+1, last_page=page_n+1, grayscale=True)[0]
    w, h = im.size
    draw = ImageDraw.Draw(im)

    blocks = pages[page_n]['Blocks']
    for block in blocks:
        bbox = block['Geometry']['BoundingBox']

        if block['BlockType'] == 'KEY_VALUE_SET':
            if (block['EntityTypes'][0] == 'KEY'):
                show_bbox(draw, bbox, w, h, 'red')
            else:
                show_bbox(draw, bbox, w, h, 'green')
        elif block['BlockType'] == 'TABLE':
            show_bbox(draw, bbox, w, h, 'blue')
        elif block['BlockType'] == 'CELL':
            show_bbox(draw, bbox, w, h, 'yellow')
        elif block['BlockType'] == 'SELECTION_ELEMENT' and block['SelectionStatus'] == 'SELECTED':
            show_selected(draw, bbox, w, h, 'blue')
        else:
            print(block['BlockType'], 'not addressed')
    
    im.show()

def show_im_w_lines(fpath: str, pages, page_n: int, max_block: int):
    im = convert_from_path(fpath, dpi=200, first_page=page_n+1, last_page=page_n+1, grayscale=True)[0]
    w, h = im.size
    draw = ImageDraw.Draw(im)

    blocks = pages[page_n]['Blocks']
    for i, block in enumerate(blocks):
        if i >= max_block:
            print(f'exceeded {i} blocks')
        
        if block['BlockType'] == 'LINE':
            bbox = block['Geometry']['BoundingBox']
            show_bbox(draw, bbox, w, h, 'red')

    im.show()

def imshow_2d(im_arr: np.ndarray):
    assert im_arr.ndim == 2

    expanded_im_arr = np.repeat(im_arr[:, :, np.newaxis], 3, axis=2)
    _, ax = plt.subplots()
    ax.imshow(expanded_im_arr)
    ax.set_xticks([])
    ax.set_yticks([])
    plt.show()

def vis_max_contours(fpath: str, page_n: int, n_contours: int = 1):
    im = convert_from_path(fpath, first_page=page_n, last_page=page_n, grayscale=True)[0]
    im_arr = np.asarray(im)

    edges = cv2.Canny(im_arr, 64, 127, apertureSize=3, L2gradient=True)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)

    expanded_im_arr = np.repeat(im_arr[:, :, np.newaxis], 3, axis=2)
    for i in range(n_contours):
        print('contour', i)
        im_to_show = cv2.drawContours(expanded_im_arr, sorted_contours, i, (0,255,0), 3)
    
    _, ax = plt.subplots()
    ax.imshow(im_to_show)
    ax.set_xticks([])
    ax.set_yticks([])
    plt.show()
