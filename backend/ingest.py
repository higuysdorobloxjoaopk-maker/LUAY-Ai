import zipfile, os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

DATA_DIR = "../data"
EXTRACT_DIR = "../extracted"
DB_DIR = "../db"

os.makedirs(EXTRACT_DIR, exist_ok=True)

print("📦 Extraindo bibliotecas...")
for file in os.listdir(DATA_DIR):
    if file.lower().endswith(".zip") and ("lua" in file.lower() or "luau" in file.lower()):
        with zipfile.ZipFile(os.path.join(DATA_DIR, file)) as z:
            z.extractall(EXTRACT_DIR)

texts = []
for root, _, files in os.walk(EXTRACT_DIR):
    for f in files:
        if f.endswith(".txt"):
            with open(os.path.join(root, f), encoding="utf-8") as file:
                texts.append(file.read())

print(f"📚 {len(texts)} arquivos carregados")

splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)
docs = splitter.create_documents(texts)

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = Chroma.from_documents(docs, embeddings, persist_directory=DB_DIR)
db.persist()

print("✅ Base Lua/Luau indexada com sucesso.")
