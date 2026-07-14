from io import BytesIO
import pandas as pd
from fastapi import FastAPI, UploadFile, File, HTTPException

app = FastAPI(title="Dashboard Inteligente API", version="0.1.0")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    filename = file.filename or ""
    ext = filename.lower().split(".")[-1] if "." in filename else ""
    
    if ext not in {"csv" , "xlsx", "xls"}:
        raise HTTPException(status_code=400, detail="Formato no permitido. Usa CSV o Excel.")
    
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Archivo vacío.")
    
    try:
        if ext == "csv":
            df = pd.read_csv(BytesIO(content))
        else:
            df = pd.read_excel(BytesIO(content))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"No se pudo leer el archivo: {str(e)}")
    
    if df.empty:
        raise HTTPException(status_code=400, detail="El archivo no contiene registros.")
    
    return {
        "filename": filename,
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_names": df.columns.tolist(),
    }