# === file: loaders.py ===
import os
import pandas as pd
from pathlib import Path
from langchain_community.document_loaders import *
from langchain.schema import Document

def load_file(file_path):
    ext = Path(file_path).suffix.lower()
    try:
        if ext == ".pdf":
            return PyPDFLoader(file_path).load()[:10]  # Load only first 10 pages for performance
        elif ext == ".txt":
            return TextLoader(file_path).load()
        elif ext == ".json":
            return JSONLoader(file_path).load()
        elif ext == ".xml":
            return UnstructuredFileLoader(file_path).load()
        elif ext == ".csv":
            return CSVLoader(file_path).load()
        elif ext in [".xls", ".xlsx"]:
            return load_excel_all_sheets(file_path)
        elif ext in [".doc", ".docx"]:
            return UnstructuredWordDocumentLoader(file_path).load()
        elif ext in [".ppt", ".pptx"]:
            return UnstructuredPowerPointLoader(file_path).load()
        else:
            return []
    except Exception:
        return []

def load_excel_all_sheets(file_path):
    dfs = pd.read_excel(file_path, sheet_name=None, header=None)
    documents = []
    file_name = os.path.basename(file_path)
    for sheet_name, df in dfs.items():
        for index, row in df.iterrows():
            row_text = " | ".join([str(cell) for cell in row if pd.notna(cell)])
            if row_text.strip():
                content = f"Sheet: {sheet_name}, Row {index}: {row_text}"
                documents.append(Document(page_content=content, metadata={"source": file_name}))
    return documents