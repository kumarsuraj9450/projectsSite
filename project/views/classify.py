from project import app, templates, cwd

from typing import Optional, List
# from os import getcwd, remove
from os.path import basename, isfile
from fastapi import FastAPI, Request, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse
# from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
from shutil import copyfileobj
from fastai.vision import load_learner, open_image
from pickle import load
import requests
from urllib.parse import urlparse
# import numpy as np
# from torch import save

content = """
		<body>
		<form action="/files/" enctype="multipart/form-data" method="post">
		<input name="files" type="file" multiple>
		<input type="submit"></form>
		<form action="/classification/" enctype="multipart/form-data" method="post">
		<input name="files" type="file" multiple>
		<input type="submit">
		</form>
		</body>
		"""

def classify(name: str):
	try:
		# url = cwd+name
		# print(url)
		url = name
		learner = load_learner(cwd+r'\static',r'classification.pkl')

		# print(learner.data.classes)
		
		im = open_image(url)
		data = []
		with open(cwd+r'\static\classes.pkl','rb') as d:
			data = load(d)

		res = learner.predict(im)
		predictedClass = data[res[1]]
		# print(predictedClass)
	except Exception as e:
		predictedClass = f'Unknown Error occured {e}'
	return predictedClass,url

@app.get("/classification", response_class=HTMLResponse)
def read_image(request: Request):
	return templates.TemplateResponse("classification_form.html", {"request": request})
    # return HTMLResponse(content=content)

@app.post("/classification", response_class=HTMLResponse)
def post_image(request: Request, files: UploadFile = File(...)):
	try:
		if not "image" in str(files.content_type):
			raise HTTPException(status_code=404, detail="Not an image file")
	except:
		raise HTTPException(status_code=404, detail="Not an image file")

	with open(cwd+f"\\static\\userFiles\\{files.filename}", "wb") as buffer:
		copyfileobj(files.file, buffer)
	
	pred,url = classify(cwd+f"\\static\\userFiles\\{files.filename}")

	# if isfile(url):
	# 	remove(url)
	# print(f"pred => {pred}")
	# print(f"url => {url}")
	return templates.TemplateResponse("classify_result.html", 
		{"request": request, 
		"image":f"/static/userFiles/{files.filename}", 
		"file":files.filename , 
		"prediction":pred}
		)
			# return {"filename": image.filename}
	# return {"file":files.filename, "type":files.content_type}

@app.get("/classify_url", response_class=HTMLResponse)
def read_url(request: Request):
	return templates.TemplateResponse("classify_url_form.html", {"request": request})

@app.post("/classify_url", response_class=HTMLResponse)
def post_url(request: Request, files: str = Form(...)):
	print(type(files))
	try:
		resp = requests.get(files, stream=True)

		if not "image" in resp.headers['content-type'] : 
			del resp
			raise HTTPException(status_code=404, detail="Not an image file")

		a = urlparse(files)
		name = basename(a.path)
		with open(cwd+f"\\static\\userFiles\\{name}", 'wb') as local_file:
			resp.raw.decode_content = True
			copyfileobj(resp.raw, local_file)

		pred, url = classify(cwd+f"\\static\\userFiles\\{name}")

		# if isfile(url):
		# 	remove(url)

	except Exception as e:
		return {"Something went wrong while classifying url": f'{e}'}
	# return files

	return templates.TemplateResponse("classify_result.html", 
		{"request": request, 
		"image":f"/static/userFiles/{name}", 
		"file":name , 
		"prediction":pred
		}
		)