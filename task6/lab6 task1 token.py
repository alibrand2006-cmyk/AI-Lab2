import re

SAMPLES = [
    "AI, search!",
    "I can't log in.",
    "help@example.com",
    "CS4944 version 2.1",
    "",
    "یہ ایک مثال ہے",
]

def compare_tokens(text):
    whitespace = text.split()
    word_like = re.findall(r"\b\w+\b", text, flags=re.UNICODE)
    return whitespace, word_like

def optional_model_tokenizer(texts):
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2", device="cpu"
        )
        print("\n[Model tokenizer: all-MiniLM-L6-v2]")
        for text in texts:
            tokens = model.tokenizer.tokenize(text)
            print(f"Text: {text!r}")
            print(f"Subword tokens: {tokens}")
            print(f"Count: {len(tokens)}")
    except ImportError:
        print("\n[Optional model tokenizer skipped]")
        print("Install with: pip install sentence-transformers")
    except Exception as exc:
        print("\n[Optional model tokenizer unavailable]")
        print(f"Reason: {type(exc).__name__}: {exc}")

def main():
    print("LAB 6 - TASK 1: TOKENIZATION")
    for i, text in enumerate(SAMPLES, 1):
        ws, words = compare_tokens(text)
        print(f"\nInput {i}: {text!r}")
        print(f"Whitespace tokens: {ws}")
        print(f"Whitespace count: {len(ws)}")
        print(f"Unicode word-like tokens: {words}")
        print(f"Word-like count: {len(words)}")
    optional_model_tokenizer(SAMPLES[:2])

if __name__ == "__main__":
    main()
