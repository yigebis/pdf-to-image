from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from pdf2image import convert_from_bytes
from io import BytesIO

app = FastAPI()

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    pdf_bytes = await file.read()
    # pages = convert_from_bytes(pdf_bytes, dpi=300, poppler_path="C:/Program Files (x86)/poppler-25.07.0/Library/bin")
    pages = convert_from_bytes(pdf_bytes, dpi=300)

    if not pages:
        raise HTTPException(status_code=400, detail="No pages found in PDF")
    
    # Convert first page to PNG in memory
    buf = BytesIO()
    pages[0].save(buf, format="PNG")
    buf.seek(0)
    
    return StreamingResponse(buf, media_type="image/png")
