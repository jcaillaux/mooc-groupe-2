from fastapi import FastAPI, Request, HTTPException, Depends, status
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi.staticfiles import StaticFiles
from datetime import datetime, timedelta
import config
from .api.points import list_courses, list_threads, dump_thread, analyze_thread
from .services.text_embedding import get_text_embedding
from .services.nearest_pgvectors import get_nearest_messages
from urllib.parse import unquote


class LoginData(BaseModel):
    username: str = Field(max_length=16)
    password: str = Field(max_length=16)


class RagData(BaseModel):
    course_id: str = Field(max_length=128)
    prompt:    str = Field(max_length=512)

class Message(BaseModel):
    message:str = Field(max_length=4096)


SECRET_KEY = "your-secret-key-here"  # Change this!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

fake_users_db = {
    "admin": {
        "username": "admin",
        "hashed_password": pwd_context.hash("admin")  # Change this!
    }
}
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str):
    user = fake_users_db.get(username)
    if not user or not verify_password(password, user["hashed_password"]):
        return False
    return user

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def check_token(token:str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Create FastAPI app
app = FastAPI(
    title="MOOC-Group-2",
    description="MOOc description",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    redirect_slashes=False
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
    """ SPA Fontend access. """
    return FileResponse('app/templates/index.html')

@app.post("/api/login", tags=["LOGIN/OUT"])
async def login(request: Request, form: LoginData):
    """ Login """
    print(form)
    user = authenticate_user(form.username, form.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}
    #return JSONResponse(content={'status': 'success', 'message': 'Login Sucessful'})


@app.get("/api/logout", tags=["LOGIN/OUT"])
async def logout(request: Request):
    """ Logout """
    return JSONResponse(content={'msg': "Logged out!"})


@app.get("/api/courses", tags=["ACCESS DATA"])
async def course(request: Request, current_user: str = Depends(get_current_user)):
    """ Retreive the list of all available courses """
    print(current_user)
    return JSONResponse(content=list_courses())


@app.get("/api/courses/{course_id:path}", tags=["ACCESS DATA"])
async def threads(resquest: Request, course_id: str, current_user: str = Depends(get_current_user)):
    """ Retreive the list of threads within a course """
    print(current_user)
    return JSONResponse(content=list_threads(course_id=unquote(course_id)))

@app.get("/api/threads/{thread_id}", tags=["ACCESS DATA"])
async def messages(request: Request, thread_id: str, current_user: str = Depends(get_current_user)):
    print(current_user)
    """ Retreive all the messages within a given thread """
    return JSONResponse(content=dump_thread(thread_id=thread_id))

@app.post("/api/rag", tags=["RAG"])
async def rag(request: Request, payload: RagData, current_user: str = Depends(get_current_user)):
    """ Perform a query search among a given course using a rag base approach """
    nearest_messages = get_nearest_messages(prompt=payload.prompt)
    
    messages = [{'thread_title' : msg.body, 'thread_id' : msg.thread_id if msg.thread_id else msg.id} for msg in nearest_messages]
    
    return JSONResponse(content=messages)

@app.get("/api/analyzethreads/{thread_id}", tags=["ANALYSIS"])
async def messages(request: Request, thread_id: str, current_user: str = Depends(get_current_user)):
    """ Analyze the language and the sentiment of each message within a thread """
    return JSONResponse(content=analyze_thread(thread_id=thread_id))

@app.get("/api/topics", tags=["ANALYSIS"])
async def topics(request:Request, token:str):
    """ Fetch the topic modelling analysis of all the forum data """
    check_token(token)
    return FileResponse("app/plots/threads_topics.html")

@app.get("/api/users/{course_id:path}", tags=["ANALYSIS"])
async def users(request:Request, course_id:str,token:str):
    """ Fetch user clustering for a specific course or over all avaliable courses """
    check_token(token)
    if course_id == "all":
        return FileResponse("app/plots/clusters_kmeans_interactif.html")
    else :
        # perform clustering
        return FileResponse("app/plots/clusters_kmeans_interactif.html") 

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.RELOAD)
