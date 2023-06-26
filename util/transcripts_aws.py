import boto3
import os
import time
import uuid

from util.x_logging import pickled
from pdf2image import convert_from_path, pdfinfo_from_path
from PIL import ImageDraw

# QUARTERS
# America Cuaresma, Edwin Munoz Martinez, Felipe Mares, Jesse Burns, Michael Diles

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

# s3.create_bucket(Bucket=BUCKET,
#                  CreateBucketConfiguration={'LocationConstraint': 'us-west-2'})

@pickled
def textract_pages(bucket: str, fname: str):
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

# s3_conn = boto3.resource('s3')
# s3_ob = s3_conn.Object(bucket, document)
# s3_resp = s3_ob.get()
# bytes_stream = io.BytesIO(s3_resp['Body'].read())
# im_binary = bytes_stream.getvalue()
# im = Image.open(io.BytesIO(bytes_stream))

@pickled
def textract_pdf_to_image(fpath: str):
    textract = boto3.client('textract', region_name=REGION)

    pdfinfo = pdfinfo_from_path(fpath)
    n_pages = pdfinfo['Pages']
    print(n_pages, 'pages')

    rand_id = str(uuid.uuid4())

    pages = []
    for i in range(1, n_pages+1):
        print(i)
        
        im = convert_from_path(fpath, first_page=i, last_page=i, grayscale=True)[0]

        save_to_fpath = os.path.join(TEMP_DIR, f'{rand_id}-{i}.png')
        im.save(save_to_fpath)
        with open(save_to_fpath, 'rb') as f:
            im_bytes = bytearray(f.read())
        os.remove(save_to_fpath)

        # im_encoded = base64.b64encode(im_bytes)
        resp = textract.detect_document_text(Document={'Bytes': im_bytes})
        pages.append(resp)

    return pages

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
