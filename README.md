# Document Q\&A Assistant with OCR + LLM + Vector Search

A modular, Document Intelligence App built with LangChain, Streamlit, and FAISS, supporting OCR-based image extraction from both PDF and image files. All content is embedded into a local FAISS vector DB and queried via LLMs (LLaMA3 via Ollama).

---

##  Features

* Ask questions to your documents in natural language
* Upload any files **PDF, DOCX, TXT, Images (JPG, PNG)**
* Extract & embed **text from images** using **Tesseract OCR**
* Use **LLaMA3** via **Ollama** for local language generation
* Multi-project setup with persistent vectorstores per project
* Modular design for embeddings, UI, OCR, and LLM prompts
* Progress bars for chunking, embedding, and OCR operations

---

## Tech Stack

* `Python`, `LangChain`, `Streamlit`
* `FAISS` for local vector search
* `PyMuPDF` + `pytesseract` for PDF OCR
* `Ollama` + `LLaMA3` for LLM responses
* 'nomic-embed-text' for embedding a text
* `dotenv` + `os` for project configuration

---

## ⚙️ Setup Instructions

1. **Clone repo**

2. **Install dependencies**
   `pip install -r requirements.txt`

3. **Setup `.env` file**

```
OLLAMA_BASE_URL=http://localhost:11434
EMBEDDING_MODEL=nomic-embed-text
LLM_MODEL=llama3
USER_AGENT=DocumentQA/1.0
```

4. **Install Tesseract OCR**

   * Windows: [https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)
   * Add to PATH

5. **Run App**

```
streamlit run main_app.py
```

---

![image](https://github.com/user-attachments/assets/58a4dcfd-1e90-4828-ad5b-5ddc0f5abd15)


---

## 📬 Contact

Feel free to reach out on www.linkedin.com/in/karthikeyan-athirajan-487b53199 or contribute to this repo!

---
