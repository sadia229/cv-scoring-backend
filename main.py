from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
import os

app = FastAPI()

UPLOAD_DIR = "uploaded_files"  # Directory where PDFs are saved
os.makedirs(UPLOAD_DIR, exist_ok=True)  # Ensure the folder exists

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        
        # Save the uploaded PDF
        with open(file_path, "wb") as f:
            f.write(await file.read())

        return {"message": "PDF uploaded successfully", "filename": file.filename}
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=400)

@app.get("/get-pdf/{filename}")
async def get_pdf(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)

    # Check if the file exists
    if not os.path.exists(file_path):
        return JSONResponse(content={"message": "File not found"}, status_code=404)

    return FileResponse(file_path, media_type="application/pdf", filename=filename)

# http://127.0.0.1:8000/docs
