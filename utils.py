# === file: utils.py ===
import os
import json
import hashlib
import pandas as pd
from datetime import datetime
from config import BASE_PROJECTS_DIR

def get_all_projects():
    return [d for d in os.listdir(BASE_PROJECTS_DIR) if os.path.isdir(os.path.join(BASE_PROJECTS_DIR, d))]

def get_project_paths(project_name):
    base = os.path.join(BASE_PROJECTS_DIR, project_name)
    paths = {
        "base": base,
        "vectorstore": os.path.join(base, "vectorstore"),
        "hashes": os.path.join(base, "hashes.json"),
        "log_csv": os.path.join(base, "answer_history.csv"),
        "log_txt": os.path.join(base, "answer_history.txt"),
        "docs": os.path.join(base, "docs"),
        "config": os.path.join(base, "config.json")
    }
    for p in paths.values():
        if not os.path.splitext(p)[1]:
            os.makedirs(p, exist_ok=True)
    return paths

def save_project_config(project_path, data):
    with open(project_path["config"], "w") as f:
        json.dump(data, f, indent=2)

def load_project_config(project_path):
    if os.path.exists(project_path["config"]):
        with open(project_path["config"], "r") as f:
            return json.load(f)
    return {}

def compute_sha256(file):
    return hashlib.sha256(file.getvalue()).hexdigest()

def load_hashes(hash_path):
    if os.path.exists(hash_path):
        with open(hash_path, "r") as f:
            return json.load(f)
    return {}

def save_hashes(hashes, hash_path):
    with open(hash_path, "w") as f:
        json.dump(hashes, f, indent=2)

def log_answer(question, answer, sources, log_csv, log_txt):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = {"Time": timestamp, "Question": question, "Answer": answer, "Sources": "; ".join(sources)}
    pd.DataFrame([row]).to_csv(log_csv, mode='a', header=not os.path.exists(log_csv), index=False, encoding="utf-8")
    with open(log_txt, "a", encoding="utf-8") as f:
        f.write(f"\n[{timestamp}]\nQ: {question}\nA: {answer}\nSources: {', '.join(sources)}\n" + "-"*50 + "\n")

def delete_vectorstore(vectorstore_dir, hash_path):
    if os.path.exists(vectorstore_dir):
        for f in os.listdir(vectorstore_dir):
            os.remove(os.path.join(vectorstore_dir, f))
    if os.path.exists(hash_path):
        os.remove(hash_path)