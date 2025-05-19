from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import config
from .api.points import list_courses, list_threads, dump_thread

# Create FastAPI app
app = FastAPI(
    title="MOOC-Group-2",
    description="MOOc description",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Mount static files from the templates folder
app.mount("/static", StaticFiles(directory="app/templates",
          html=True), name="static")

app.mount("/assets", StaticFiles(directory="app/templates/assets",
          html=True), name="assets")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/courses", tags=["ACCESS DATA"])
async def course(request: Request):
    return JSONResponse(content=list_courses())


@app.get("/courses/{course_id}", tags=["ACCESS DATA"])
async def threads(resquest: Request, course_id: str):
    return JSONResponse(content=list_threads(course_id=course_id))


@app.get("/courses/{course_id}/threads/{thread_id}", tags=["ACCESS DATA"])
async def messages(request: Request, course_id: str, thread_id: str):
    return JSONResponse(content=dump_thread(thread_id=thread_id))


@app.get("/", tags=["FRONT"])
async def home(request: Request):
    return FileResponse('app/templates/index.html')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.RELOAD)
