"""
app.py
This is the chat interface. Run it AFTER you've run ingest.py at least once.

Run it from the terminal like this:
    streamlit run app.py
"""

import streamlit as st
from rag_utils import get_client, embed_texts, get_collection, GENERATION_MODEL

st.set_page_config(page_title="DocMind AI", page_icon="📄")
st.title("📄 DocMind AI — Chat With Your Documents")
st.caption("A Retrieval-Augmented Generation (RAG) system powered by Gemini + ChromaDB")

client = get_client()
collection = get_collection()

# Keep chat history across messages in this session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Redraw all previous messages every time the app reruns
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


def retrieve_context(question, top_k=4):
    """Turn the question into an embedding, then fetch the most similar chunks."""
    query_embedding = embed_texts(client, [question], task_type="RETRIEVAL_QUERY")[0]
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )
    chunks = results["documents"][0]
    sources = [meta["source"] for meta in results["metadatas"][0]]
    return chunks, sources


def generate_answer(question, chunks):
    """Build a prompt that includes the retrieved chunks, then ask Gemini to answer."""
    context_text = "\n\n---\n\n".join(chunks)

    prompt = f"""You are a helpful assistant that answers questions using ONLY the context provided below.
If the answer is not contained in the context, say "I couldn't find that in the documents provided."

Context:
{context_text}

Question: {question}

Answer:"""

    response = client.models.generate_content(
        model=GENERATION_MODEL,
        contents=prompt,
    )
    return response.text


question = st.chat_input("Ask a question about your documents...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching documents and generating answer..."):
            chunks, sources = retrieve_context(question)
            answer = generate_answer(question, chunks)
            st.markdown(answer)
            with st.expander("Sources used"):
                for src in set(sources):
                    st.write(f"- {src}")

    st.session_state.messages.append({"role": "assistant", "content": answer})
