import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from web.routes import router as web_router 
app = FastAPI()
app.mount("/static", StaticFiles(directory="web/static"), name="static")
templates = Jinja2Templates(directory="web/templates")
app.include_router(web_router)
if __name__ == "__main__":
   import uvicorn
   print("Starting the FastAPI server...")
   uvicorn.run(app, host="127.0.0.1", port=8000)
