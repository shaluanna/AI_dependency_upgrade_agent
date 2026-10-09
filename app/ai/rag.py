from pathlib import Path
from typing import List

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_documents(knowledge_base_path: Path):
    documents = []

    if not knowledge_base_path.exists():
        return documents

    for file_path in knowledge_base_path.rglob("*"):
        if file_path.suffix.lower() not in {".md", ".txt"}:
            continue

        try:
            text = file_path.read_text(
                encoding="utf-8",
                errors="ignore"
            )

            if text.strip():
                documents.append(
                    {
                        "path": str(file_path),
                        "text": text
                    }
                )

        except OSError:
            continue

    return documents


def retrieve_documents(
    query: str,
    knowledge_base_path: Path,
    top_k: int = 3
) -> List[str]:
    documents = load_documents(knowledge_base_path)

    if not documents:
        return []

    texts = [
        document["text"]
        for document in documents
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    try:
        matrix = vectorizer.fit_transform(
            texts + [query]
        )
    except ValueError:
        return []

    query_vector = matrix[-1]
    document_vectors = matrix[:-1]

    similarities = cosine_similarity(
        query_vector,
        document_vectors
    )[0]

    ranked = similarities.argsort()[::-1]

    matches = []

    for index in ranked[:top_k]:
        if similarities[index] <= 0:
            continue

        matches.append(
            documents[index]["text"]
        )

    return matches