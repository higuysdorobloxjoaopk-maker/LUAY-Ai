from flask import Flask, request, jsonify
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import HuggingFacePipeline
from langchain.chains import RetrievalQA
from transformers import pipeline

app = Flask(__name__)

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = Chroma(persist_directory="../db", embedding_function=embeddings)

generator = pipeline("text-generation", model="gpt2", max_new_tokens=250)
llm = HuggingFacePipeline(pipeline=generator)

qa = RetrievalQA.from_chain_type(llm=llm, retriever=db.as_retriever())

@app.route("/ask", methods=["POST"])
def ask():
    q = request.json["question"]
    if "lua" not in q.lower() and "luau" not in q.lower():
        return jsonify({"answer": "🤖 Essa IA responde apenas perguntas sobre Lua e Luau."})
    res = qa.run(q)
    return jsonify({"answer": res})

app.run(host="0.0.0.0", port=8000)
