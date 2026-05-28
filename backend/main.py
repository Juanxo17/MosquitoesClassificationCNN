from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
from backend.model import predict
from backend.risk import evaluate_risk
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os

app = FastAPI(title="Sistema de Vigilancia Entomológica")

# Montar la carpeta estática para poder servir el index.html
static_path = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/")
def read_root():
    # Cuando abran el link principal, los redirige automáticamente a la página
    return RedirectResponse(url="/static/index.html")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
async def predict_endpoint(file: UploadFile = File(...)):
    if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        raise HTTPException(status_code=400, detail="Solo se aceptan imágenes JPG o PNG.")
    
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
    except Exception:
        raise HTTPException(status_code=400, detail="No se pudo abrir la imagen.")
    
    prediction = predict(image)
    risk = evaluate_risk(prediction['species'], prediction['confidence'])
    
    return risk

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


@app.post("/predict-lote")
async def predict_lote(files: list[UploadFile] = File(...)):
    resultados = []
    for file in files:
        if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
            resultados.append({
                "archivo": file.filename,
                "error": "Formato no soportado"
            })
            continue
        try:
            contents = await file.read()
            image = Image.open(io.BytesIO(contents))
            prediction = predict(image)
            risk = evaluate_risk(prediction['species'], prediction['confidence'])
            risk["archivo"] = file.filename
            resultados.append(risk)
        except Exception:
            resultados.append({
                "archivo": file.filename,
                "error": "No se pudo procesar la imagen"
            })
    return {"resultados": resultados}

