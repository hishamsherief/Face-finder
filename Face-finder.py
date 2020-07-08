import zipfile
import math
from PIL import Image
from PIL import ImageDraw
import pytesseract
import cv2 as cv
import numpy as np
from kraken import pageseg

# loading the face detection classifier
face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

data = {}

#saving the images to the directory data
zip_file = #Enter the file name of the zip file containing newspaper pages
with zipfile.ZipFile(zip_file, 'r') as file:
    for n in file.infolist():
        with file.open(n) as image:
            img = Image.open(image).convert('RGB')
            data[n.filename] = {'page':img}

#extracting and saving the text to the directory           
for filename in data.keys():
    text = pytesseract.image_to_string(data[filename]['page'])
    data[filename]['text'] = text

#finding bounding boxing of faces extracting them and saving to the directory
for filename in data.keys():
    open_cv_image = np.array(data[filename]['page']) 
    img_g = cv.cvtColor(open_cv_image, cv.COLOR_BGR2GRAY)
    faces_bounding_boxes = face_cascade.detectMultiScale(img_g, 1.3, 5)
    data[filename]['faces'] = []
    for x,y,w,h in faces_bounding_boxes:
        face = data[filename]['page'].crop((x,y,x+w,y+h))
        data[filename]['faces'].append(face)

#converting faces to thumnail size
for filename in data.keys():
    for face in data[filename]['faces']:
        face.thumbnail((100,100),Image.ANTIALIAS)

#defining search function
def search(keyword):
    for filename in data:
        if (keyword in data[filename]['text']):
            if(len(data[filename]['faces']) != 0):
                print("Result found in file {}".format(filename))
                h = math.ceil(len(data[filename]['faces'])/5)
                contact_sheet=Image.new('RGB',(500, 100*h))
                x = 0
                y = 0
                for img in data[filename]['faces']:
                    contact_sheet.paste(img, (x, y))
                    if x + 100 == contact_sheet.width:
                        x = 0
                        y += 100
                    else:
                        x += 100
                        
                display(contact_sheet)
            else:
                print("Result found in file {} \nBut there are no faces in the file\n\n".format(filename))
    return
