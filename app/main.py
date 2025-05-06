from fastapi import FastAPI
import config


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.RELOAD)
