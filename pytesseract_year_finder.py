"""
Created on Sun May 10 18:06:33 2020
@author: robandev
Uses Tesseract-OCR to read images of receipts including scanned images
Renames all image files with year, example: filename.jpg --> 2011_filename.jpg
If scanned image is in pdf format it converts it to jpg before scanning and renaming
This is useful for organizing receipts by Year for accounting purpose
Dependencies:
pdf2image
pytesseract
PIL (Python Image Library)
"""

try:
    from PIL import Image
except ImportError:
    import Image
import time
import re
import os
import pytesseract
# import tempfile
from pdf2image import convert_from_path
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)

# requires Tesseract-OCR
pytesseract.pytesseract.tesseract_cmd = r"path/to/Tesseract-OCR/tesseract executable"

# declare constants
path = "path/to/input/folder/"
DPI = 200
OUTPUT_FOLDER = "path/to/output/folder/"
FIRST_PAGE = 1
LAST_PAGE = 1
FORMAT = 'jpg'
THREAD_COUNT = 1
USERPWD = None
USE_CROPBOX = False
STRICT = False

def pdftopil():
    # This method reads a pdf and converts it into a sequence of images
    # path sets the path to the PDF file
    # dpi parameter assists in adjusting the resolution of the image
    # output_folder parameter sets the path to the folder to which the PIL images can be stored (optional)
    # first_page parameter allows you to set a first page to be processed by pdftoppm 
    # last_page parameter allows you to set a last page to be processed by pdftoppm
    # fmt parameter allows to set the format of pdftoppm conversion (PpmImageFile, TIFF)
    # thread_count parameter allows you to set how many thread will be used for conversion.
    # userpw parameter allows you to set a password to unlock the converted PDF
    # use_cropbox parameter allows you to use the crop box instead of the media box when converting
    # strict parameter allows you to catch pdftoppm syntax error with a custom type PDFSyntaxError
    
    pdf_names = {}    
    for root, dirs, files in os.walk(path):
        for file in files:
            extension = re.search("pdf|PDF$", file)
            if extension:
                pil_images = convert_from_path(path + file, dpi=DPI, output_folder=OUTPUT_FOLDER, first_page=FIRST_PAGE, last_page=LAST_PAGE, fmt=FORMAT, thread_count=THREAD_COUNT, userpw=USERPWD, use_cropbox=USE_CROPBOX, strict=STRICT)
                pdf_names.update({file: pil_images})
    return pdf_names
    # return pil_images
    
def save_images(pil_images):
    # converts the images in PIL Image file format to the required image format and saves in jpg with old name
    for name, image in pil_images.items():
        # print(name)
        # print(image[0].filename)
        # print(image[0])
        # print("\n")
        image[0].save(name + ".jpg")
        new_name = name[:len(name)-4]
        # print(new_name)
        os.rename(image[0].filename, path + new_name + ".jpg")

# read and rename all image files with year, example: filename.jpg --> 2011_filename.jpg
def rename_images():
    for root, dirs, files in os.walk(path):
        for file in files:
            extension = re.search("pdf|PDF$", file)
            if not extension:
                text = pytesseract.image_to_string(path+file)
                # print(file)
                # print(text)
                print("\n" + path+file + " >>>>>")
                year = re.search("[/]20\d{2}\s", text)
                while year == None:
                    year = re.search("\d{2}[/]\d{2}\s", text)
                    if year is not None:
                        break
                    year = re.search("([\s]20\d{2})\s", text)
                    break
                try:
                    year_formatted = '20' + year.group()[3:5].strip().replace('/','')
                except AttributeError:
                    year_formatted = '0000'
                finally:
                    print(year_formatted + "_" + file)
                    os.rename(path + file, path + year_formatted + "_" + file)
                            
pil_images = pdftopil()
save_images(pil_images)
rename_images()