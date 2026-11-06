"""Compare three paraphrased queries with TF-IDF and real CPU embeddings."""
from lab6_task2_chunks import DOCS, make_chunks
from lab6_task2_search import Retriever, show_hits

QUERIES = [
    "I became sick; can I hand in my coursework later?",
    "I cannot get into my account; how can I get access again?",
    "My package arrived damaged; how long do I have to report it?"
]


def main():
    records = make_chunks(DOCS, "sentence")
    print("TASK 2 SEMANTIC SUGGESTIONS")
    print("Using sentence-aware chunks; evidence remains original source text.")
    for backend in ("tfidf", "embedding"):
        print(f"\nBACKEND: {backend}")
        try:
            engine = Retriever(records, backend=backend)
        except (ImportError, OSError, RuntimeError) as error:
            print(f"SKIPPED: real embedding model unavailable: {error}")
            if backend == "embedding":
                print("Install sentence-transformers and run again; no fake vectors are used.")
            continue
        for query in QUERIES:
            print(f"\nQuery: {query}")
            show_hits(engine.search(query, k=3))


if __name__ == "__main__":
    main()
