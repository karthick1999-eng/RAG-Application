# === file: embeddings.py ===
import requests
import os
from dotenv import load_dotenv
from langchain_core.embeddings import Embeddings


load_dotenv()

class OllamaNomicEmbeddings(Embeddings):
    def __init__(self):
        self.endpoint_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434") + "/api/embeddings"
        self.model = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")

    def embed_documents(self, texts):
        embeddings = []
        for text in texts:
            response = requests.post(
                self.endpoint_url,
                json={"model": self.model, "prompt": text}
            )
            data = response.json()
            if "embedding" not in data:
                raise ValueError(f"Unexpected response format: {data}")
            embeddings.append(data["embedding"])
        return embeddings

    def embed_query(self, text):
        return self.embed_documents([text])[0]

    def __call__(self, text):
        return self.embed_query(text)
