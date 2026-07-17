from io import BytesIO
import pandas as pd
import re
import unicodedata
from fastapi import FastAPI, UploadFile, File, HTTPException

app = FastAPI(title="Dashboard Inteligente API", version="0.1.0")

def normalize_columns(columns):
    normalized = []
    for col in columns:
        name = str(col).strip().lower()
        name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
        name = re.sub(r"\s+", "", name)
        name = re.sub(r"[^a-z0-9]", "", name)
        name = re.sub(r"\+", "", name).strip("_")
        normalized.append(name)
    return normalized


def infer_column_type(series):
    if pd.api.types.is_numeric_dtype(series):
        return "numeric"
    if pd.api.types.is_datetime64_any_dtype(series):
        return "datetime"
    if pd.api.types.is_bool_dtype(series):
        return "boolean"
    return "text"

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
    
    original_columns = df.columns.tolist()
    df.columns = normalize_columns(df.columns)

    if any(col == "" or col == "nan" for col in df.columns):
        raise HTTPException(status_code=400, detail="Hay columnas con nombre vacio o invalido.")

    duplicated_cols = df.columns[df.columns.duplicated()].tolist()
    if duplicated_cols:
        raise HTTPException(
            status_code=400,
            detail=f"Hay columnas duplicadas despues de normalizar: {duplicated_cols}",
        )

    non_empty_rows = int(df.dropna(how="all").shape[0])
    if non_empty_rows == 0:
        raise HTTPException(status_code=400, detail="El archivo no tiene filas con datos utiles.")

    numeric_columns = df.select_dtypes(include="number").columns.tolist()
    if not numeric_columns:
        raise HTTPException(
            status_code=400,
            detail="Se requiere al menos una columna numerica para analisis.",
        )

    column_types = {col: infer_column_type(df[col]) for col in df.columns}
    nulls_by_column = {col: int(df[col].isna().sum()) for col in df.columns}

    warnings = []
    duplicate_rows = int(df.duplicated().sum())
    if duplicate_rows > 0:
        warnings.append(f"Se detectaron {duplicate_rows} filas duplicadas.")
    if any(v > 0 for v in nulls_by_column.values()):
        warnings.append("El dataset contiene valores nulos.")
    
    return {
        "filename": filename,
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_names": df.columns.tolist(),
        "original_column_names": original_columns,
        "numeric_columns": numeric_columns,
        "column_types": column_types,
        "nulls_by_column": nulls_by_column,
        "warnings": warnings,
    }

def to_python_number(value):
    if pd.isna(value):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    return float(value)

def build_descriptive_stats(df):
    numeric_df = df.select_dtypes(include="number")
    if numeric_df.empty:
        raise HTTPException(
            status_code=400,
            detail="No hay columnas numericas para calcular estadisticas."
        )

    totals = {}
    means = {}
    mins = {}
    maxs = {}

    for col in numeric_df.columns:
        totals[col] = to_python_number(numeric_df[col].sum())
        means[col] = to_python_number(numeric_df[col].mean())
        mins[col] = to_python_number(numeric_df[col].min())
        maxs[col] = to_python_number(numeric_df[col].max())

    nulls_by_column = {col: int(df[col].isna().sum()) for col in df.columns}
    total_rows = int(df.shape[0])

    null_percentage_by_column = {}
    columns_with_nulls = []
    for col, null_count in nulls_by_column.items():
        pct = round((null_count / total_rows) * 100, 2) if total_rows > 0 else 0.0
        null_percentage_by_column[col] = pct
        if null_count > 0:
            columns_with_nulls.append(col)

    null_rows_count = int(df.isna().any(axis=1).sum())

    duplicate_mask = df.duplicated(keep=False)
    duplicate_rows_count = int(duplicate_mask.sum())
    duplicate_groups_count = int(df.duplicated().sum())

    return {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "numeric_columns": numeric_df.columns.tolist(),
        "stats": {
            "total": totals,
            "promedio": means,
            "minimo": mins,
            "maximo": maxs,
        },
        "quality": {
            "nulls_by_column": nulls_by_column,
            "null_percentage_by_column": null_percentage_by_column,
            "columns_with_nulls": columns_with_nulls,
            "null_rows_count": null_rows_count,
            "duplicate_rows_count": duplicate_rows_count,
            "duplicate_groups_count": duplicate_groups_count,
        },
    }

@app.post("/analyze")
async def analyze_file(file: UploadFile = File(...)):
    filename = file.filename or ""
    ext = filename.lower().split(".")[-1] if "." in filename else ""

    if ext not in {"csv", "xlsx", "xls"}:
        raise HTTPException(status_code=400, detail="Formato no permitido. Usa CSV o Excel.")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Archivo vacio.")

    try:
        if ext == "csv":
            df = pd.read_csv(BytesIO(content))
        else:
            df = pd.read_excel(BytesIO(content))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"No se pudo leer el archivo: {str(e)}")

    if df.empty:
        raise HTTPException(status_code=400, detail="El archivo no contiene registros.")

    df.columns = normalize_columns(df.columns)

    if any(col == "" or col == "nan" for col in df.columns):
        raise HTTPException(status_code=400, detail="Hay columnas con nombre vacio o invalido.")

    duplicated_cols = df.columns[df.columns.duplicated()].tolist()
    if duplicated_cols:
        raise HTTPException(
            status_code=400,
            detail=f"Hay columnas duplicadas despues de normalizar: {duplicated_cols}",
        )

    analysis = build_descriptive_stats(df)

    return {
        "filename": filename,
        "analysis": analysis,
    }