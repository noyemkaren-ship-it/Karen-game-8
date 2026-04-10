from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from router.game_router import router
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded

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
app.mount("/static", StaticFiles(directory="static"), name="static")
