from qa_engine import answer_question


# ==========================================
# TEST 1: ANSWERABLE QUESTION
# ==========================================

question_1 = "What is a database?"

result_1 = answer_question(question_1)


print("\n========================================")
print("TEST 1 - ANSWERABLE QUESTION")
print("========================================")

print("Question:", question_1)
print("Status:", result_1["status"])
print("Answer:", result_1["answer"])

print("\nSources:")

for source in result_1["sources"]:
    print(
        f'{source["source"]} | '
        f'Page/Slide: {source["page"]} | '
        f'Score: {source["score"]}'
    )


# ==========================================
# TEST 2: UNANSWERABLE QUESTION
# ==========================================

question_2 = "What is the capital of Japan?"

result_2 = answer_question(question_2)


print("\n========================================")
print("TEST 2 - UNCOVERED QUESTION")
print("========================================")

print("Question:", question_2)
print("Status:", result_2["status"])
print("Answer:", result_2["answer"])

print("\nSources:")

if result_2["sources"]:
    for source in result_2["sources"]:
        print(
            f'{source["source"]} | '
            f'Page/Slide: {source["page"]} | '
            f'Score: {source["score"]}'
        )
else:
    print("No supporting sources found.")