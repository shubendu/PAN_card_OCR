import json
import pytesseract
import cv2
import numpy as np
import sys
import re
import os
from PIL import Image
import ftfy
import pan_read           
import io

image_path = "pan1.jpg"

img = cv2.imread(image_path)
img = cv2.resize(img, None, fx=2, fy=2,interpolation=cv2.INTER_CUBIC)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
var = cv2.Laplacian(img, cv2.CV_64F).var()
if var < 50:
    print("Image is Too Blurry....")
    k= input('Press Enter to Exit.')
    exit(1)

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
filename = image_path
text = pytesseract.image_to_string(Image.open(filename), lang = 'eng')

text_output = open('output.txt', 'w', encoding='utf-8')
text_output.write(text)
text_output.close()

file = open('output.txt', 'r', encoding='utf-8')
text = file.read()

text = ftfy.fix_text(text)
text = ftfy.fix_encoding(text)


# for aadhar card
# data = aadhaar_read.adhaar_read_data(text)
# for pan card
data = pan_read.pan_read_data(text)
try:
    to_unicode = unicode
except NameError:
    to_unicode = str
with io.open('info.json', 'w', encoding='utf-8') as outfile:
    data = json.dumps(data, indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=False)
    outfile.write(to_unicode(data))

with open('info.json', encoding = 'utf-8') as data:
    data_loaded = json.load(data)


print("\n---------- PAN Details ----------")
print("\nPAN Number: ",data_loaded['PAN'])
print("\nName: ",data_loaded['Name'])
print("\nFather's Name: ",data_loaded['Father Name'])
print("\nDate Of Birth: ",data_loaded['Date of Birth'])
print("\n---------------------------------")

k = input("\n\nPress Enter To EXIT")
exit(0)