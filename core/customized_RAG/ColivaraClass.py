import os
from colivara_py import ColiVara

rag_client = ColiVara(
    # this is the default and can be omitted
    api_key=os.environ.get("COLIVARA_API_KEY"),
    # this is the default and can be omitted
    base_url="https://api.colivara.com"
)

# Upload a document to the default collection
document = rag_client.upsert_document(
    name="attention is all you need",
    url="https://arxiv.org/abs/1706.03762",
    metadata={"published_year": "2017"}
)