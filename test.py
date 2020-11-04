# from fastai.vision import load_learner, open_image

# from os import getcwd
# from pickle load

# cwd = os.getcwd()

# name = r"\static\c06bn5a1ziw51.jpg"

# url = cwd + name

# learner = load_learner('.',r'stage-1-export-file.pkl')

# # print(learner.data.classes)


# im = open_image(url)

# with open('classes.pkl', 'rb') as f:
#     data = load(f)

# res = learner.predict(im)
# predictedClass = data[res[1]]
# print(predictedClass)

# Import requests, shutil python module.
import requests

import shutil

# This is the image url.
# image_url = "https://en.wikipedia.org/wiki/Cat_intelligence#/media/File:An_up-close_picture_of_a_curious_male_domestic_shorthair_tabby_cat.jpg"

image_url = "https://www.dev2qa.com/demo/images/green_button.jpg"
image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/An_up-close_picture_of_a_curious_male_domestic_shorthair_tabby_cat.jpg/1024px-An_up-close_picture_of_a_curious_male_domestic_shorthair_tabby_cat.jpg"
# Open the url image, set stream to True, this will return the stream content.
# resp = requests.get(image_url, stream=True)

# print(resp.image_url)

# Open a local file with wb ( write binary ) permission.
# local_file = open('local_image.jpg', 'wb')

# # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
# resp.raw.decode_content = True

# # Copy the response stream raw data to local image file.
# shutil.copyfileobj(resp.raw, local_file)

# # Remove the image url response object.
# del resp



import os
from urllib.parse import urlparse

url = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/An_up-close_picture_of_a_curious_male_domestic_shorthair_tabby_cat.jpg/1024px-An_up-close_picture_of_a_curious_male_domestic_shorthair_tabby_cat.jpg"

a = urlparse(url)

print(a.path)
print(os.path.basename(a.path))
name = os.path.basename(a.path)
resp = requests.get(url, stream=True)
local_file = open(name, 'wb')
resp.raw.decode_content = True
shutil.copyfileobj(resp.raw, local_file)
local_file.close()
print(hash(name))
# local_file = open('local_image.jpg', 'wb')