import json
import re

import numpy as np
from sentence_transformers import SentenceTransformer


# ==========================================
# LOAD PROCESSED CHUNKS
# ==========================================

with open(
    "data/processed/chunks.json",
    "r",
    encoding="utf-8"
) as file:
    chunks = json.load(file)


# ==========================================
# LOAD SAVED EMBEDDINGS
# ==========================================

embeddings = np.load(
    "data/processed/embeddings.npy"
)

print("Loaded embeddings:", embeddings.shape)


# ==========================================
# LAZY LOAD EMBEDDING MODEL
# ==========================================

model = None


def get_model():

    global model

    if model is None:

        print("Loading embedding model...")

        model = SentenceTransformer(
            "all-MiniLM-L6-v2",
            device="cpu"
        )

    return model


# ==========================================
# TEXT NORMALIZATION
# ==========================================

def normalize_text(text):

    if not text:
        return ""

    text = text.lower()

    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ==========================================
# GET WORDS
# ==========================================

def get_words(text):

    return set(
        normalize_text(text).split()
    )


# ==========================================
# LEXICAL SCORE
# ==========================================

def lexical_score(query, text):

    query_words = get_words(query)
    text_words = get_words(text)

    if not query_words:
        return 0.0

    matched_words = (
        query_words.intersection(text_words)
    )

    return (
        len(matched_words)
        / len(query_words)
    )


# ==========================================
# PHRASE SCORE
# ==========================================

def phrase_score(query, text):

    query_normalized = normalize_text(query)
    text_normalized = normalize_text(text)

    if not query_normalized or not text_normalized:
        return 0.0

    # Exact complete phrase
    if query_normalized in text_normalized:
        return 1.0

    query_words = query_normalized.split()

    if len(query_words) < 2:
        return 0.0

    pair_matches = 0
    total_pairs = len(query_words) - 1

    for i in range(total_pairs):

        pair = (
            query_words[i]
            + " "
            + query_words[i + 1]
        )

        if pair in text_normalized:
            pair_matches += 1

    if total_pairs == 0:
        return 0.0

    return (
        pair_matches
        / total_pairs
    )


# ==========================================
# HANDWRITTEN BOOST
# ==========================================

def handwritten_boost(chunk):

    if chunk.get("type") == "handwritten":
        return 0.12

    return 0.0


# ==========================================
# SEARCH FUNCTION
# ==========================================

def search(query, top_k=5):

    # --------------------------------------
    # Encode query only
    # --------------------------------------

    query_embedding = get_model().encode(
        [query],
        convert_to_numpy=True
    )[0]

    query_embedding = (
        query_embedding
        / max(
            np.linalg.norm(query_embedding),
            1e-12
        )
    )

    # --------------------------------------
    # Semantic similarity
    # --------------------------------------

    semantic_scores = (
        embeddings @ query_embedding
    )

    # --------------------------------------
    # Calculate final scores
    # --------------------------------------

    scored_results = []

    for index, chunk in enumerate(chunks):

        text = chunk.get(
            "text",
            ""
        )

        semantic = float(
            semantic_scores[index]
        )

        lexical = lexical_score(
            query,
            text
        )

        phrase = phrase_score(
            query,
            text
        )

        handwritten = handwritten_boost(
            chunk
        )

        final_score = (
            0.60 * semantic
            + 0.25 * lexical
            + 0.15 * phrase
            + handwritten
        )

        scored_results.append(
            {
                "index": index,
                "score": final_score,
                "semantic_score": semantic,
                "lexical_score": lexical,
                "phrase_score": phrase
            }
        )

    # --------------------------------------
    # Sort by relevance
    # --------------------------------------

    scored_results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    # --------------------------------------
    # Build results
    # --------------------------------------

    results = []

    for item in scored_results[:top_k]:

        index = item["index"]
        chunk = chunks[index]

        results.append(
            {
                "score": round(
                    float(item["score"]),
                    6
                ),

                "semantic_score": round(
                    float(item["semantic_score"]),
                    6
                ),

                "lexical_score": round(
                    float(item["lexical_score"]),
                    6
                ),

                "phrase_score": round(
                    float(item["phrase_score"]),
                    6
                ),

                "text": chunk.get(
                    "text",
                    ""
                ),

                "page": chunk.get(
                    "page",
                    None
                ),

                "source": chunk.get(
                    "source",
                    "unknown"
                ),

                "type": chunk.get(
                    "type",
                    "unknown"
                )
            }
        )

    return results