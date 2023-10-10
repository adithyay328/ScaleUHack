import pinecone

pinecone.init(api_key="8883fec9-aceb-4516-a1c1-4ae80bb6afbc", environment="gcp-starter")

print(pinecone.list_indexes())
index = pinecone.Index("nodes")