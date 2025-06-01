# === file: prompt_templates.py ===
from langchain.prompts import PromptTemplate

stuff_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""Use only the context below to answer the question. Before answering it just analyze the context and then answer the question to make sure to provide relevant response.
If the answer cannot be found in the context, say \"I don't know.\"

Context:
{context}

Question: {question}
Answer:"""
)

custom_prompt = PromptTemplate(
    input_variables=["context_str", "question"],
    template="""Use only the context below to answer the question. Before answering it just analyze the context and then answer the question to make sure to provide relevant response.
If the answer cannot be found in the context, say \"I don't know.\"

Context:
{context_str}

Question: {question}
Answer:"""
)

refine_prompt = PromptTemplate(
    input_variables=["question", "existing_answer", "context_str"],
    template="""You have provided an existing answer and new context.
Refine the original answer to better answer the question using the new context.

Original Question: {question}
Existing Answer: {existing_answer}
New Context:
{context_str}

Refined Answer:"""
)

map_reduce_question_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""Use the following context to answer the question. Before answering it just analyze the context and then answer the question to make sure to provide relevant response.
Context:
{context}

Question: {question}
Answer:"""
)

map_reduce_combine_prompt = PromptTemplate(
    input_variables=["summaries", "question"],
    template="""You have received multiple answers to the same question from different parts of the documents.

Context:
{summaries}

Question: {question}
Combined Answer:"""
)