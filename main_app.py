# === file: main_app.py ===
import asyncio
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

import streamlit as st
import os
from datetime import datetime
from PIL import Image
import pytesseract
from langchain.chains import RetrievalQA
from langchain_ollama import OllamaLLM as Ollama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from config import LLM_MODEL
from embeddings import OllamaNomicEmbeddings
from loaders import load_file
from prompt_templates import *
from utils import *
from langchain.schema import Document
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

st.set_page_config(page_title="Multi-Project Q&A App")
st.title("Document Q&A")

st.sidebar.header("Project Setup")
all_projects = get_all_projects()
project_choice = st.sidebar.selectbox("Choose existing project or type to create new one:", all_projects + ["Create new"], index=0)

if project_choice == " Create new":
    project_name = st.sidebar.text_input("New project name:", "")
    if project_name:
        st.sidebar.success(f"Project '{project_name}' ready.")
else:
    project_name = project_choice

if not project_name:
    st.stop()

paths = get_project_paths(project_name)

chain_type = st.sidebar.selectbox("Chain Type", ["stuff", "refine", "map_reduce"])
top_k = st.sidebar.slider("Chunks to Retrieve (k)", 1, 10, 4)
if st.sidebar.button(" Reset Vectorstore"):
    delete_vectorstore(paths["vectorstore"], paths["hashes"])
    st.sidebar.success("Vectorstore reset for this project.")

uploaded_files = st.file_uploader(
    " Upload documents (PDF, DOCX, images, etc.)",
    type=["pdf", "txt", "json", "xml", "csv", "xls", "xlsx", "doc", "docx", "ppt", "pptx", "png", "jpg", "jpeg"],
    accept_multiple_files=True
)

embeddings = OllamaNomicEmbeddings()
hashes = load_hashes(paths["hashes"])

if os.path.exists(os.path.join(paths["vectorstore"], "index.faiss")):
    vectorstore = FAISS.load_local(paths["vectorstore"], embeddings, allow_dangerous_deserialization=True)
    retriever = vectorstore.as_retriever(search_kwargs={"k": top_k})
else:
    vectorstore, retriever = None, None

if uploaded_files:
    new_docs, new_hashes = [], hashes.copy()
    progress = st.progress(0, text=" Processing uploaded files...")

    for i, file in enumerate(uploaded_files):
        file_hash = compute_sha256(file)
        file_name = file.name
        save_path = os.path.join(paths["docs"], file_name)

        if file_name not in hashes or hashes[file_name]["hash"] != file_hash:
            with open(save_path, "wb") as f:
                f.write(file.getvalue())

            ext = file_name.split(".")[-1].lower()
            if ext in ["png", "jpg", "jpeg"]:
                st.image(save_path, caption=f"Screenshot: {file_name}", use_column_width=True)
                text = pytesseract.image_to_string(Image.open(save_path))
                if text.strip():
                    new_docs.append(Document(page_content=text, metadata={"source": file_name}))
            else:
                new_docs.extend(load_file(save_path))

            new_hashes[file_name] = {"hash": file_hash, "timestamp": datetime.now().isoformat()}
        else:
            st.write(f"Skipped (no change): {file_name}")

        progress.progress((i + 1) / len(uploaded_files))

    if new_docs:
        st.info("Splitting and embedding documents...")
        splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
        split_docs = splitter.split_documents(new_docs)

        if not vectorstore:
            vectorstore = FAISS.from_documents(split_docs, embeddings)
        else:
            vectorstore.add_documents(split_docs)

        vectorstore.save_local(paths["vectorstore"])
        retriever = vectorstore.as_retriever(search_kwargs={"k": top_k})
        save_hashes(new_hashes, paths["hashes"])
        st.success("Vectorstore updated with embedded content including images.")

# === Ask a Question ===
query = st.text_input("Ask a question:")
if query and retriever:
    llm = Ollama(model=LLM_MODEL)
    chain_type_kwargs = {
        "stuff": {"prompt": stuff_prompt},
        "refine": {"question_prompt": custom_prompt, "refine_prompt": refine_prompt},
        "map_reduce": {"question_prompt": map_reduce_question_prompt, "combine_prompt": map_reduce_combine_prompt}
    }.get(chain_type, {})

    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, chain_type=chain_type, chain_type_kwargs=chain_type_kwargs, return_source_documents=True)
    result = qa_chain.invoke(query)
    answer = result["result"]
    sources = list({os.path.basename(doc.metadata.get("source", "unknown")) for doc in result["source_documents"]})

    st.markdown("### Answer:")
    st.write(answer)
    st.markdown("### Sources:")
    st.write(sources)
    log_answer(query, answer, sources, paths["log_csv"], paths["log_txt"])

# === Log Download ===
st.sidebar.header("Export Logs")
if os.path.exists(paths["log_txt"]):
    with open(paths["log_txt"], "rb") as f:
        st.sidebar.download_button("TXT Log", f, file_name=f"{project_name}_qa_history.txt")
if os.path.exists(paths["log_csv"]):
    with open(paths["log_csv"], "rb") as f:
        st.sidebar.download_button("CSV Log", f, file_name=f"{project_name}_qa_history.csv")
