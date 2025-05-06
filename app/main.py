from fastapi import FastAPI
from fastapi.responses import JSONResponse
import config


app = FastAPI()


@app.get("/")
def read_root():
    return JSONResponse(content={"msg": "Hello from HF !"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.RELOAD)
