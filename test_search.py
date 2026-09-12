from search_engine import search


# ==========================================
# TEST QUERY
# ==========================================

query = "What is a database?"


# ==========================================
# SEARCH
# ==========================================

results = search(query, top_k=3)


# ==========================================
# DISPLAY RESULTS
# ==========================================

print("\n==============================")
print("SEARCH QUERY:", query)
print("==============================")


for i, result in enumerate(results, start=1):

    print(f"\n--- RESULT {i} ---")

    print("Score:", round(result["score"], 4))
    print("Source:", result["source"])
    print("Page/Slide:", result["page"])
    print("Type:", result["type"])

    print("\nText:")
    print(result["text"][:500])