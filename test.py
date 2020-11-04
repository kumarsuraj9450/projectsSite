from fastai.vision import load_learner, open_image

from os import getcwd
from pickle load

cwd = os.getcwd()

name = r"\static\c06bn5a1ziw51.jpg"

url = cwd + name

learner = load_learner('.',r'stage-1-export-file.pkl')

# print(learner.data.classes)


im = open_image(url)

with open('classes.pkl', 'rb') as f:
    data = load(f)

res = learner.predict(im)
predictedClass = data[res[1]]
print(predictedClass)





