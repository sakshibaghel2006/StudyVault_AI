import json
from qa_engine import answer_question


QUESTIONS = [

    # =========================
    # 10 ANSWERABLE QUESTIONS
    # =========================

    {
        "question": "What is data in a database system?",
        "expected": "ANSWERED"
    },

    {
        "question": "What is information?",
        "expected": "ANSWERED"
    },

    {
        "question": "What is knowledge?",
        "expected": "ANSWERED"
    },

    {
        "question": "What is a database?",
        "expected": "ANSWERED"
    },

    {
        "question": "What is a DBMS?",
        "expected": "ANSWERED"
    },

    {
        "question": "What is data abstraction?",
        "expected": "ANSWERED"
    },

    {
        "question": "What are the levels of data abstraction?",
        "expected": "ANSWERED"
    },

    {
        "question": "What is the physical level of abstraction?",
        "expected": "ANSWERED"
    },

    {
        "question": "What is the logical level of abstraction?",
        "expected": "ANSWERED"
    },

    {
        "question": "What is the view level of abstraction?",
        "expected": "ANSWERED"
    },

    {
        "question": "What are database languages?",
        "expected": "ANSWERED"
    },

    {
        "question": "What is DDL?",
        "expected": "ANSWERED"
    },

    {
        "question": "What is DML?",
        "expected": "ANSWERED"
    },

    {
        "question": "What is an ER model?",
        "expected": "ANSWERED"
    },

    {
        "question": "What is a relational model?",
        "expected": "ANSWERED"
    },

    {
        "question": "What is SQL?",
        "expected": "ANSWERED"
    },

    {
        "question": "What are the advantages of a DBMS?",
        "expected": "ANSWERED"
    },

    {
        "question": "What are the problems with a file-oriented system?",
        "expected": "ANSWERED"
    },

    {
        "question": "What is a database schema?",
        "expected": "ANSWERED"
    },

    {
        "question": "What is a database instance?",
        "expected": "ANSWERED"
    },


    # =========================
    # 10 UNCOVERED QUESTIONS
    # =========================

    {
        "question": "What is the capital of Japan?",
        "expected": "NOT COVERED"
    },

    {
        "question": "Who is the Prime Minister of India?",
        "expected": "NOT COVERED"
    },

    {
        "question": "What is the population of India?",
        "expected": "NOT COVERED"
    },

    {
        "question": "What is artificial intelligence?",
        "expected": "NOT COVERED"
    },

    {
        "question": "What is machine learning?",
        "expected": "NOT COVERED"
    },

    {
        "question": "What is the weather today?",
        "expected": "NOT COVERED"
    },

    {
        "question": "Who invented the computer?",
        "expected": "NOT COVERED"
    },

    {
        "question": "What is the largest country in the world?",
        "expected": "NOT COVERED"
    },

    {
        "question": "What is Python programming?",
        "expected": "NOT COVERED"
    },

    {
        "question": "What is blockchain technology?",
        "expected": "NOT COVERED"
    }
]


def run_evaluation():

    results = []

    correct = 0

    print("\n===================================")
    print("      STUDYVAULT AI EVALUATION")
    print("===================================\n")

    for index, item in enumerate(QUESTIONS, start=1):

        question = item["question"]
        expected = item["expected"]

        result = answer_question(question)

        actual = result["status"]

        if actual == expected:
            correct += 1

        results.append({
            "id": index,
            "question": question,
            "expected": expected,
            "actual": actual,
            "correct": actual == expected,
            "sources": result["sources"]
        })

        print(f"{index}. {question}")
        print(f"   Expected : {expected}")
        print(f"   Actual   : {actual}")
        print(
            f"   Result   : "
            f"{'PASS' if actual == expected else 'FAIL'}"
        )
        print()


    accuracy = (correct / len(QUESTIONS)) * 100

    print("===================================")
    print("EVALUATION COMPLETE")
    print("===================================")

    print(f"Total Questions : {len(QUESTIONS)}")
    print(f"Correct        : {correct}")
    print(f"Accuracy       : {accuracy:.2f}%")

    with open(
        "evaluation_results.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            {
                "total_questions": len(QUESTIONS),
                "correct": correct,
                "accuracy": accuracy,
                "results": results
            },
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\nResults saved to:")
    print("evaluation_results.json")


if __name__ == "__main__":
    run_evaluation()