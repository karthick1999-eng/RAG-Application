# === file: config.py ===
import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
EMBED_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3.1")

BASE_PROJECTS_DIR = "projects"
os.makedirs(BASE_PROJECTS_DIR, exist_ok=True)