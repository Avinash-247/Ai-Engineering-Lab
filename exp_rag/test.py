from utils import get_embeddings_from_gcp

embedding = get_embeddings_from_gcp()

print("Embedding...")

vector = embedding.embed_query("Hello")

print("Done")
print(len(vector))