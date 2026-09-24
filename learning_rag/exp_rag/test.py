'''from utils import get_embeddings_from_gcp

embedding = get_embeddings_from_gcp()

print("Embedding...")

vector = embedding.embed_query("Hello")

print("Done")
print(len(vector))'''

from utils import get_embeddings_from_gcp

embeddings = get_embeddings_from_gcp()

result = embeddings.embed_query("Hello world")

print(result[:5])