from fastapi import FastAPI
from router.product import router as productrouter
from router.user import router as userrouter
import  os
from fastapi.staticfiles import StaticFiles
import shutil

app = FastAPI()

app.include_router(productrouter)
app.include_router(userrouter)


@app.get("/")
async def home():
  return{
    "message":"Welcome to our home.."
  }



app.mount("/files",StaticFiles(directory="products"),name="files")