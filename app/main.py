from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import config

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
