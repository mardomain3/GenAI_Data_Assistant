import os
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.query_services import run_query, get_columns


from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
# ==========================================
# FASTAPI APP
# ==========================================

app = FastAPI(
    title="GenAI Query Assistant",
    description="Upload an Excel dataset and ask natural language questions",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return FileResponse("static/index.html")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# ==========================================
# STORE UPLOADED FILE PATHS
# ==========================================

file_store = {}  # { file_id: file_path }

# ==========================================
# UPLOAD ENDPOINT
# ==========================================

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    if not file.filename.endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="Only .xlsx files are supported")

    file_id = str(uuid.uuid4())
    save_path = f"data/{file_id}_{file.filename}"

    os.makedirs("data", exist_ok=True)

    with open(save_path, "wb") as f:
        content = await file.read()
        f.write(content)

    file_store[file_id] = save_path

    return {
        "message": "File uploaded successfully",
        "file_id": file_id,
        "filename": file.filename
    }

# ==========================================
# GET COLUMNS ENDPOINT
# ==========================================

@app.get("/columns/{file_id}")
def columns(file_id: str):

    if file_id not in file_store:
        raise HTTPException(status_code=404, detail="File not found")

    cols = get_columns(file_store[file_id])

    return {
        "file_id": file_id,
        "columns": cols
    }

# ==========================================
# QUERY ENDPOINT
# ==========================================

class QueryRequest(BaseModel):
    file_id: str
    question: str

@app.post("/query")
def query(request: QueryRequest):

    if request.file_id not in file_store:
        raise HTTPException(status_code=404, detail="File not found. Upload first.")

    result = run_query(file_store[request.file_id], request.question)

    return result