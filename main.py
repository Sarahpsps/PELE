from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from analisador import analisar_ingredientes
from ocr import processar_foto_rotulo

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="frontend"), name="static")

class AnalisarRequest(BaseModel):
    ingredientes: str
    tipo_pele: str

@app.get("/")
def index():
    return FileResponse("frontend/index.html")

@app.post("/analisar")
def analisar(body: AnalisarRequest):
    lista = [i.strip() for i in body.ingredientes.split(",") if i.strip()]
    resultado = analisar_ingredientes(lista, body.tipo_pele)
    return resultado

@app.post("/ocr")
async def ocr(file: UploadFile = File(...)):
    imagem_bytes = await file.read()
    resultado = processar_foto_rotulo(imagem_bytes)
    return resultado