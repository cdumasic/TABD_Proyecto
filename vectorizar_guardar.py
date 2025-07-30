import json
import os
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from pathlib import Path

# === CONFIGURACIÓN GENERAL ===
OUTPUT_DIR = Path(__file__).resolve().parent / "output"
CHROMA_DIR = str(Path(__file__).resolve().parent / "chroma_db")
COLECCION_NOMBRE = "propuestas_politicas"
MODELO = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

def cargar_bloques(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def inicializar_chroma(directorio, coleccion_nombre):
    client = chromadb.PersistentClient(path=directorio)
    try:
        collection = client.get_collection(coleccion_nombre)
    except chromadb.errors.NotFoundError:
        collection = client.create_collection(name=coleccion_nombre)
    return client, collection

def vectorizar_y_guardar():
    print("📦 Cargando modelo de embeddings...")
    model = SentenceTransformer(MODELO)

    print("💾 Inicializando ChromaDB con persistencia...")
    client, collection = inicializar_chroma(CHROMA_DIR, COLECCION_NOMBRE)

    total_bloques = 0

    print("🔍 Buscando bloques revisados en todas las carpetas de partidos...")
    for partido_folder in OUTPUT_DIR.iterdir():
        if partido_folder.is_dir():
            json_path = partido_folder / "bloques_revisados.json"
            if json_path.exists():
                print(f"📂 Procesando: {partido_folder.name}")

                bloques = cargar_bloques(json_path)

                for bloque in bloques:
                    texto = bloque["bloque"]
                    emb = model.encode(texto).tolist()

                    collection.add(
                        ids=[bloque["id"]],
                        documents=[texto],
                        embeddings=[emb],
                        metadatas=[{
                            "partido": bloque["partido"],
                            "tipo_fuente": bloque["tipo_fuente"]
                        }]
                    )

                total_bloques += len(bloques)
            else:
                print(f"⚠️  No se encontró 'bloques_revisados.json' en {partido_folder.name}")

    print(f"✅ {total_bloques} bloques indexados en total en: {CHROMA_DIR}")

# === EJECUCIÓN ===
if __name__ == "__main__":
    vectorizar_y_guardar()