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
import numpy as np
from torch import save

def segment(path: str, name: str):
	url = path #cwd+path

	# def acc_camvid(input, target):
	#     target = target.squeeze(1)
	#     mask = target != void_code
	#     return (input.argmax(dim=1)[mask]==target[mask]).float().mean()


	learn = load_learner(cwd+r'\static', "segmentation")

	im = open_image(url)

	data = learn.predict(im)

	data[0].save(cwd+f'\\static\\segment\\{name}.png')

	save(data[1], cwd+f'\\static\\segment\\{name}.pt')
		# pass
	# path = Path(r"/static")
	# name = r"\static\userFiles\BingWallpaper.jpg"


@app.get("/segment", response_class=HTMLResponse)
def read_url(request: Request):
	return templates.TemplateResponse("segment_form.html", {"request": request, "code": "/static/codes.txt"})

@app.post("/segment")
def post_url(request: Request, files: UploadFile = File(...)):
	print(type(files))

	try:
		if not "image" in str(files.content_type):
			raise HTTPException(status_code=404, detail="Not an image file")
	except:
		raise HTTPException(status_code=404, detail="Not an image file")

	with open(cwd+f"\\static\\userFiles\\{files.filename}", "wb") as buffer:
		copyfileobj(files.file, buffer)

	name = files.filename.split(".")[0]
	segment(cwd+f"\\static\\userFiles\\{files.filename}", f'{name}')

		# if isfile(url):
		# 	remove(url)
	# return files

	return templates.TemplateResponse("segment_result.html", 
		{"request": request, 
		"code": f"/static/codes.txt",
		"image":f"/static/segment/{name}.png", 
		"file":f"/static/segment/{name}.pt"
		}
		)


@app.get("/segment_url", response_class=HTMLResponse)
def read_url(request: Request):
	return templates.TemplateResponse("segment_url_form.html", {"request": request, "code": "/static/codes.txt"})


@app.post("/segment_url", response_class=HTMLResponse)
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

		print(f"name => {name.split('.')[0]} ")
		segment(cwd+f"\\static\\userFiles\\{name}", f"{name.split('.')[0]}")

		# if isfile(url):
		# 	remove(url)
		name = name.split('.')[0]

	except:
		return {'error':"Something went wrong while segmeting url"}
	# return files

	return templates.TemplateResponse("segment_result.html", 
		{"request": request, 
		"code":f"/static/codes.txt",
		"image":f"/static/segment/{name}.png", 
		"file":f"/static/segment/{name}.pt"
		}
		)