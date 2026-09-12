import re

from search_engine import search


# ==========================================
# TEXT CLEANING
# ==========================================

def clean_text(text):
    """
    Clean extracted course-material text.
    """

    if not text:
        return ""

    # Remove weird / non-printable characters
    text = re.sub(
        r"[^\x09\x0A\x0D\x20-\x7E]",
        " ",
        text
    )

    # Remove excessive spaces
    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    # Remove excessive blank lines
    text = re.sub(
        r"\n\s*\n+",
        "\n\n",
        text
    )

    return text.strip()


# ==========================================
# REFUSAL RESPONSE
# ==========================================

def refusal_response():
    """
    Standard response when the course material
    does not provide sufficient evidence.
    """

    return {
        "status": "NOT COVERED",
        "answer": (
            "The provided course material does not contain "
            "enough evidence to answer this question."
        ),
        "sources": []
    }


# ==========================================
# CREATE ANSWER
# ==========================================

def make_answer(question, sources):
    """
    Generate an answer only from retrieved
    course-material evidence.
    """

    if not sources:
        return (
            "The provided course material does not contain "
            "enough evidence to answer this question."
        )

    evidence = []

    for source in sources:

        text = clean_text(
            source.get("text", "")
        )

        if text:
            evidence.append(text)

    if not evidence:
        return (
            "The provided course material does not contain "
            "enough evidence to answer this question."
        )

    combined = "\n\n".join(evidence)

    # ======================================
    # SPLIT INTO SENTENCES
    # ======================================

    sentences = re.split(
        r"(?<=[.!?])\s+",
        combined
    )

    # ======================================
    # QUESTION KEYWORDS
    # ======================================

    question_words = set(
        re.findall(
            r"[a-zA-Z]+",
            question.lower()
        )
    )

    stop_words = {
        "what",
        "is",
        "are",
        "was",
        "were",
        "the",
        "a",
        "an",
        "of",
        "in",
        "on",
        "to",
        "for",
        "and",
        "or",
        "how",
        "why",
        "does",
        "do",
        "according",
        "from",
        "this",
        "that",
        "these",
        "those"
    }

    question_words -= stop_words

    # ======================================
    # SCORE SENTENCES
    # ======================================

    scored_sentences = []

    for sentence in sentences:

        sentence = sentence.strip()

        if len(sentence) < 30:
            continue

        words = set(
            re.findall(
                r"[a-zA-Z]+",
                sentence.lower()
            )
        )

        overlap = len(
            question_words.intersection(words)
        )

        scored_sentences.append(
            (
                overlap,
                len(sentence),
                sentence
            )
        )

    # ======================================
    # SORT BY RELEVANCE
    # ======================================

    scored_sentences.sort(
        key=lambda item: (
            item[0],
            -item[1]
        ),
        reverse=True
    )

    # ======================================
    # SELECT RELEVANT SENTENCES
    # ======================================

    selected = []

    for overlap, _, sentence in scored_sentences:

        if overlap == 0:
            continue

        if sentence not in selected:
            selected.append(sentence)

        if len(selected) >= 5:
            break

    # ======================================
    # FALLBACK
    # ======================================

    if not selected:

        fallback = clean_text(
            sources[0].get(
                "text",
                ""
            )
        )

        selected = [
            fallback[:1000]
        ]

    answer = " ".join(selected)

    # ======================================
    # LIMIT ANSWER LENGTH
    # ======================================

    if len(answer) > 1600:

        answer = (
            answer[:1600]
            .rsplit(" ", 1)[0]
            + "..."
        )

    return answer


# ==========================================
# MAIN QUESTION ANSWER FUNCTION
# ==========================================

def answer_question(question):

    # ======================================
    # VALIDATE QUESTION
    # ======================================

    if not question or not question.strip():

        return refusal_response()

    # ======================================
    # SEARCH COURSE MATERIAL
    # ======================================

    results = search(
        question,
        top_k=5
    )

    if not results:

        return refusal_response()

    # ======================================
    # GET BEST SCORES
    # ======================================

    best_score = float(
        results[0].get(
            "score",
            0.0
        )
    )

    semantic_score = float(
        results[0].get(
            "semantic_score",
            0.0
        )
    )

    lexical_score = float(
        results[0].get(
            "lexical_score",
            0.0
        )
    )

    # ======================================
    # REFUSAL RULE 1
    # ======================================
    # Higher threshold prevents unrelated
    # questions from being answered.

    if best_score < 0.40:

        return refusal_response()

    # ======================================
    # REFUSAL RULE 2
    # ======================================
    # Weak semantic + weak lexical evidence
    # means insufficient course evidence.

    if (
        semantic_score < 0.35
        and lexical_score < 0.20
    ):

        return refusal_response()

    # ======================================
    # CREATE ANSWER
    # ======================================

    answer = make_answer(
        question,
        results[:3]
    )

    # ======================================
    # CREATE CITATIONS
    # ======================================

    sources = []

    for result in results[:3]:

        sources.append({

            "source": result.get(
                "source",
                "unknown"
            ),

            "page": result.get(
                "page",
                None
            ),

            "score": round(
                float(
                    result.get(
                        "score",
                        0.0
                    )
                ),
                4
            )
        })

    # ======================================
    # FINAL RESPONSE
    # ======================================

    return {
        "status": "ANSWERED",
        "answer": answer,
        "sources": sources
    }