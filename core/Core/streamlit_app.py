# streamlit_app.py
import streamlit as st
from chromadb import HttpClient
from chromadb.config import Settings

# Connect to ChromaDB
client = HttpClient(
    host="chromadb",  # Docker service name
    port=8000,
    settings=Settings(allow_reset=True, anonymized_telemetry=False)
)

# Streamlit UI
st.title("ChromaDB GUI")

# List collections
collections = client.list_collections()
st.subheader("Collections")
for col in collections:
    st.write(f"- **{col.name}** (Count: {col.count()})")

# Query embeddings in a selected collection
selected_collection = st.selectbox("Select a collection", [col.name for col in collections])
if selected_collection:
    collection = client.get_collection(selected_collection)
    items = collection.get(include=["documents", "metadatas"])
    
    st.subheader(f"Items in {selected_collection}")
    for id, doc, meta in zip(items["ids"], items["documents"], items["metadatas"]):
        st.write(f"**ID**: {id}")
        st.write(f"**Document**: {doc}")
        st.write(f"**Metadata**: {meta}")
        st.divider()