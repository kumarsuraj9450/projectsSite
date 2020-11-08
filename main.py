from typing import Optional, List
from os import getcwd, remove
from os.path import basename, isfile
from fastapi import FastAPI, Request, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from shutil import copyfileobj
from fastai.vision import load_learner, open_image
from pickle import load
import requests
from urllib.parse import urlparse

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

cwd = getcwd()

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
	content = r"go to /item/{id}?q={query+string}"
	return templates.TemplateResponse("home.html", {"request": request, "content": content})


@app.get("/items", response_class=HTMLResponse)
def read_item(request: Request, q: Optional[str] = None):
	return templates.TemplateResponse("item.html", {"request": request, "id": "None", 'q': q})


@app.get("/items/{id}", response_class=HTMLResponse)
def read_item_with_id(request: Request, id: int, q: Optional[str] = None):
	return templates.TemplateResponse("item.html", {"request": request, "id": id, 'q': q})


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


@app.get("/classification", response_class=HTMLResponse)
def read_image(request: Request):
	return templates.TemplateResponse("classification.html", {"request": request})
    # return HTMLResponse(content=content)

def predict(name: str):
	try:
		url = cwd+name
		print(url)
		learner = load_learner('.',r'stage-1-export-file.pkl')

		# print(learner.data.classes)
		
		im = open_image(url)
		data = []
		with open('classes.pkl','rb') as d:
			data = load(d)
		res = learner.predict(im)
		predictedClass = data[res[1]]
		# print(predictedClass)
	except Exception as e:
		predictedClass = f'Unknown Error occured {e}'
	return predictedClass,url


@app.post("/classification", response_class=HTMLResponse)
def post_image(request: Request, files: UploadFile = File(...)):
	try:
		if not "image" in str(files.content_type):
			raise HTTPException(status_code=404, detail="Not an image file")
	except:
		raise HTTPException(status_code=404, detail="Not an image file")

	with open(f"static/userFiles/{files.filename}", "wb") as buffer:
		copyfileobj(files.file, buffer)
	
	pred,url = predict(f"\\static\\userFiles\\{files.filename}")

	# if isfile(url):
	# 	remove(url)
	return templates.TemplateResponse("vision.html", 
		{"request": request, 
		"image":f"static/userFiles/{files.filename}", 
		"file":files.filename , 
		"prediction":pred}
		)
			# return {"filename": image.filename}
	# return {"file":files.filename, "type":files.content_type}

@app.get("/classify_url", response_class=HTMLResponse)
def read_url(request: Request):
	return templates.TemplateResponse("classify_url.html", {"request": request})

@app.post("/classify_url")
def post_url(request: Request, files: str = Form(...)):
	print(type(files))
	try:
		resp = requests.get(files, stream=True)

		if not "image" in resp.headers['content-type'] : 
			del resp
			raise HTTPException(status_code=404, detail="Not an image file")

		a = urlparse(files)
		name = basename(a.path)
		with open(f"static/userFiles/{name}", 'wb') as local_file:
			resp.raw.decode_content = True
			copyfileobj(resp.raw, local_file)

		pred, url = predict(f"\\static\\userFiles\\{name}")

		# if isfile(url):
		# 	remove(url)

	except:
		return {'error':"Something went wrong while classifying url"}
	# return files

	return templates.TemplateResponse("vision.html", 
		{"request": request, 
		"image":f"static/userFiles/{name}", 
		"file":name , 
		"prediction":pred}
		)