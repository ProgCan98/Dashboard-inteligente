from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_upload_invalid_extension():
    files = {"file": ("archivo.txt", b"hola", "text/plain")}
    response = client.post("/upload", files=files)
    assert response.status_code == 400
    
def test_upload_empty_file():
    files = {"file": ("vacio.csv", b"", "text/csv")}
    response = client.post("/upload", files=files)
    assert response.status_code == 400


def test_upload_csv_without_numeric_columns():
    csv_data = b"mes,categoria\nero,alta\nfebrero,baja\n"
    files = {"file": ("sin_numericas.csv", csv_data, "text/csv")}
    response = client.post("/upload", files=files)
    assert response.status_code == 400
    assert "columna numerica" in response.json()["detail"].lower()


def test_upload_valid_csv():
    csv_data = b"mes,ventas\nero,100\nfebrero,200\n"
    files = {"file": ("ventas.csv", csv_data, "text/csv")}
    response = client.post("/upload", files=files)
    assert response.status_code == 200
    payload = response.json()
    assert payload["rows"] == 2
    assert payload["columns"] == 2
    assert "column_types" in payload
    assert "nulls_by_column" in payload

def test_analyze_valid_csv():
    csv_data = b"mes,ventas,costo\nero,100,60\nfebrero,200,120\n"
    files = {"file": ("ok.csv", csv_data, "text/csv")}
    response = client.post("/analyze", files=files)
    assert response.status_code == 200

    payload = response.json()
    assert payload["analysis"]["stats"]["total"]["ventas"] == 300.0
    assert payload["analysis"]["stats"]["promedio"]["ventas"] == 150.0
    assert payload["analysis"]["stats"]["minimo"]["ventas"] == 100.0
    assert payload["analysis"]["stats"]["maximo"]["ventas"] == 200.0

def test_analyze_without_numeric_columns():
    csv_data = b"mes,categoria\nero,alta\nfebrero,baja\n"
    files = {"file": ("sin_numericas.csv", csv_data, "text/csv")}
    response = client.post("/analyze", files=files)
    assert response.status_code == 400
    assert "columnas numericas" in response.json()["detail"].lower()