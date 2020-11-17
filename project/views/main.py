from project import app, templates, cwd

from typing import Optional, List
from os import getcwd, remove
# from os.path import basename, isfile
from fastapi import Request
from fastapi.responses import HTMLResponse
# from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
# from shutil import copyfileobj
# from fastai.vision import load_learner, open_image
# from pickle import load
# import requests
# from urllib.parse import urlparse
# import numpy as np
# from torch import save

# app = FastAPI()

# app.mount("/static", StaticFiles(directory="./project/static"), name="static")

# templates = Jinja2Templates(directory="./project/templates")

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

