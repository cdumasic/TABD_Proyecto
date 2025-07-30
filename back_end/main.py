from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer

CHROMA_DIR = "../chroma_db"
COLECCION_NOMBRE = "propuestas_politicas"
MODELO = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
TOP_K = 10

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === MODELO Y COLECCIÓN ===
print("📦 Cargando modelo de embeddings...")
model = SentenceTransformer(MODELO)

print("📂 Conectando a ChromaDB...")
client = PersistentClient(path=CHROMA_DIR)
collection = client.get_collection(name=COLECCION_NOMBRE)

# === MODELO DE RESPUESTA ===
class Resultado(BaseModel):
    titulo: str
    partido: str
    texto: str
    similitud: float

# === ENDPOINT ===
@app.get("/search", response_model=list[Resultado])
def buscar(q: str = Query(..., description="Texto de búsqueda del usuario")):
    embedding = model.encode(q).tolist()

    resultados = collection.query(
        query_embeddings=[embedding],
        n_results=TOP_K
    )

    respuesta = []
    for i in range(len(resultados["ids"][0])):
        doc = resultados["documents"][0][i]
        meta = resultados["metadatas"][0][i]
        score = resultados["distances"][0][i]

        respuesta.append(Resultado(
            titulo=meta.get("titulo", f"Documento {i+1}"),
            partido=meta.get("partido", "Desconocido"),
            texto=doc,
            similitud=round(1 - score, 3)
        ))
    
    return respuesta
