import tensorflow as tf
import tensorflow_hub as hub
import numpy as np


# Load the Universal Sentence Encoder model from TensorFlow Hub
model_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
embed = hub.load(model_url)

# Define a function to compute cosine similarity
def cosine_similarity(v1, v2):
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    return dot_product / (norm_v1 * norm_v2)

# Define the phrases
phrase1 = "How to compute semantic similarity between phrases?"
phrase2 = "Ways to measure similarity between sentences."

# Get embeddings for the phrases
embeddings = embed([phrase1, phrase2])

# Compute cosine similarity
similarity = cosine_similarity(embeddings[0], embeddings[1])

print(f"Semantic similarity: {similarity:.4f}")
