# from typing import Optional, List
from os import getcwd # , remove
# from os.path import basename, isfile
from fastapi import FastAPI #, Request, File, UploadFile, Form, HTTPException
# from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
# from shutil import copyfileobj
# from fastai.vision import load_learner, open_image
# from pickle import load
# import requests
# from urllib.parse import urlparse
# import numpy as np
# from torch import save

app = FastAPI()

app.mount("/static", StaticFiles(directory="project/static"), name="static")

templates = Jinja2Templates(directory="project/templates")

cwd = getcwd()
cwd=cwd+'\\project'
print(f'cwd => {cwd}')

from project.views import main, classify, segment
