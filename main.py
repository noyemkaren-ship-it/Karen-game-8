from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from router.game_router import router
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from fastapi import UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import shutil
import os
from datetime import datetime
import uuid

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="Project", docs_url="/s123sdw31123sawd23123sda3esaw3ds123wasdw13ds13wdssdxcadwdasdwad213wsd1413edsaawewdadjanjnciuoadijaslbdidu")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

templates = Jinja2Templates(directory="templates")
app.include_router(router)

@app.get("/")
@limiter.limit("10/minute")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload/", tags=["new game"])
@limiter.limit("5/minute")
async def upload_file(request: Request, file: UploadFile = File(...)):
    try:
        ext = file.filename.split('.')[-1] if '.' in file.filename else ''
        unique_name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}.{ext}" if ext else f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"

        file_path = f"static/{unique_name}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return JSONResponse({
            "success": True,
            "filename": unique_name,
            "url": f"/static/{unique_name}"
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload-multiple/")
@limiter.limit("5/minute")
async def upload_multiple_files(request: Request, files: list[UploadFile] = File(...)):
    uploaded = []
    for file in files:
        try:
            ext = file.filename.split('.')[-1] if '.' in file.filename else ''
            unique_name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}.{ext}" if ext else f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
            
            file_path = f"static/{unique_name}"
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            uploaded.append({
                "original": file.filename,
                "saved_as": unique_name,
                "url": f"/static/{unique_name}"
            })
        except Exception as e:
            uploaded.append({
                "original": file.filename,
                "error": str(e)
            })
    
    return JSONResponse({"uploaded": uploaded})


@app.get("/list-files/")
@limiter.limit("10/minute")
async def list_files(request: Request):
    try:
        files = []
        for filename in os.listdir("static"):
            file_path = os.path.join("static", filename)
            if os.path.isfile(file_path):
                stat = os.stat(file_path)
                files.append({
                    "name": filename,
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                })
        files.sort(key=lambda x: x["modified"], reverse=True)
        return JSONResponse({"files": files})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@app.get("/upload-page/")
@limiter.limit("10/minute")
async def upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

app.mount("/static", StaticFiles(directory="static"), name="static")
