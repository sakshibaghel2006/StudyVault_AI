import json
import numpy as np
from sentence_transformers import SentenceTransformer

# Load processed chunks
with open(
    "data/processed/chunks.json",
    "r",
    encoding="utf-8"
) as file:
    chunks = json.load(file)

# Load embedding model
print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

# Extract text
texts = [
    chunk.get("text", "")
    for chunk in chunks
]

# Create embeddings
print("Creating embeddings...")

embeddings = model.encode(
    texts,
    convert_to_numpy=True,
    show_progress_bar=True
)

# Normalize embeddings
norms = np.linalg.norm(
    embeddings,
    axis=1,
    keepdims=True
)

embeddings = embeddings / np.maximum(
    norms,
    1e-12
)

# Save embeddings
np.save(
    "data/processed/embeddings.npy",
    embeddings
)

print("Embeddings saved successfully!")
print("Shape:", embeddings.shape)