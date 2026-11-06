import re

# Three synthetic documents, each between 150 and 250 whitespace words.
DOCS = {
    "handbook": """The student handbook explains how learners submit coursework and request support during a semester. Students should read the instructions before preparing files because different courses may use different assessment portals. Every submitted document must show the student's course code, task number, and full name. The normal submission rule is that coursework must arrive before the published deadline. An exception applies when a student is seriously ill and provides medical evidence before the deadline. The course coordinator reviews the evidence and confirms whether an extension is approved. A request alone does not guarantee extra time, and students should keep the confirmation message. Files should be uploaded in PDF format unless the teacher gives another written format. Students should check that the uploaded file opens correctly after submission. A damaged or empty file may be treated as an incomplete submission. The portal displays a receipt after a successful upload, and students should save that receipt. If the portal is unavailable, take a screenshot of the error and contact the course office. Do not send passwords or private recovery codes in an email. The course office can explain the approved alternative submission route. Late penalties depend on the published course instructions and are not removed automatically. Students should ask questions early rather than waiting until the final hour. These examples describe a synthetic teaching policy and are not an actual university rule.""",
    "it_support": """This synthetic IT guide describes safe steps for students who cannot access a learning account. First, check that the device has an internet connection and that the correct username was entered. The normal account rule is that a password reset must use the official recovery link. An exception applies when the account is locked after repeated failed attempts; the help desk must unlock it first. Students should never share a password, one-time code, or recovery code with another person. After opening the recovery page, follow the instructions sent to the registered email address. If the message does not arrive, check the spam folder and confirm that the email address is current. Do not repeatedly submit reset requests because this can create additional security checks. A successful reset should be followed by signing out of old sessions. Use a unique password that is not used on another website. If a device displays an unfamiliar security warning, stop and contact support. The help desk may ask for a student number to locate the account, but it will not ask for the password. Keep the ticket reference so that the support team can follow the problem. During a service outage, wait for the official status notice instead of installing unknown repair tools. These instructions are fictional examples prepared for a chunking exercise.""",
    "returns_guide": """This synthetic returns guide explains how a customer should report a damaged parcel. Check the outer packaging before throwing it away because photographs may be needed for a claim. The normal reporting rule is that a damaged parcel must be reported within 48 hours of delivery. An exception applies when the delivery tracking page shows a delayed delivery scan; the reporting window begins from the corrected delivery time. Take clear photographs of the item, the shipping label, and all sides of the packaging. Contact the support team through the official help form and include the order reference. Do not post personal address details in a public discussion forum. The support team reviews the photographs and may request one additional image. Keep the damaged item until the claim has been reviewed. A refund or replacement is not automatic and depends on the review outcome. If the parcel contains several products, identify which item is damaged. For an item that is missing rather than damaged, use the missing-item form instead. The support team normally sends a case number after the form is received. If no case number arrives, check the email address entered in the form. Never pay an unofficial person to speed up a claim. This guide is fictional practice material and does not describe a real retailer's policy."""
}

# Evidence is the exact combined rule and exception that should be inspected.
EVIDENCE = {
    "handbook": "The normal submission rule is that coursework must arrive before the published deadline. An exception applies when a student is seriously ill and provides medical evidence before the deadline.",
    "it_support": "The normal account rule is that a password reset must use the official recovery link. An exception applies when the account is locked after repeated failed attempts; the help desk must unlock it first.",
    "returns_guide": "The normal reporting rule is that a damaged parcel must be reported within 48 hours of delivery. An exception applies when the delivery tracking page shows a delayed delivery scan; the reporting window begins from the corrected delivery time."
}

def sentence_chunks(text, size=40):
    if size <= 0:
        raise ValueError("Size must be positive")

    if not text.strip():
        return []

    sentences = re.finditer(r'[^.!?]+[.!?]?', text)
    chunks = []
    current_start = None
    current_end = None
    current_words = 0

    for sentence in sentences:
        start = sentence.start()
        end = sentence.end()

        while start < end and text[start].isspace():
            start += 1

        while end > start and text[end - 1].isspace():
            end -= 1

        if start == end:
            continue

        words = list(re.finditer(r'\S+', text[start:end]))
        count = len(words)

        if count > size:
            if current_start is not None:
                chunks.append((current_start, current_end))
                current_start = None
                current_words = 0

            for i in range(0, count, size):
                first = words[i]
                last = words[min(i + size, count) - 1]
                chunks.append((
                    start + first.start(),
                    start + last.end()
                ))
            continue

        if current_start is None:
            current_start = start
            current_end = end
            current_words = count

        elif current_words + count <= size:
            current_end = end
            current_words += count

        else:
            chunks.append((current_start, current_end))
            current_start = start
            current_end = end
            current_words = count

    if current_start is not None:
        chunks.append((current_start, current_end))

    return chunks

def make_chunks(docs, strategy):
    """Return traceable chunk dictionaries for strategy '0', '10', or 'sentence'."""
    result = []
    for doc_id, text in docs.items():
        if strategy == "sentence":
            spans = sentence_chunks(text, size=40)
        elif strategy in {"0", "10"}:
            spans = windows(text, size=40, overlap=int(strategy))
        else:
            raise ValueError("Strategy must be '0', '10', or 'sentence'")

        for index, (start, end) in enumerate(spans):
            result.append({
                "id": f"{doc_id}:{strategy}:{index}",
                "doc": doc_id,
                "source": f"{doc_id}.txt",
                "start": start,
                "end": end,
                "text": text[start:end]
            })
    return result


def count_words(text):
    return len(text.split())

def word_spans(text):
    """Return character positions of words."""
    return [(m.start(), m.end()) for m in re.finditer(r"\S+", text)]


def windows(text, size=40, overlap=10, offset=0):
    if size <= 0 or not 0 <= overlap < size:
        raise ValueError("Require size > 0 and 0 <= overlap < size")

    spans = word_spans(text)
    chunks = []
    step = size - overlap

    for i in range(0, len(spans), step):
        j = min(i + size, len(spans))
        chunks.append((offset + spans[i][0], offset + spans[j - 1][1]))
        if j == len(spans):
            break

    return chunks

def run_tests():
    assert windows("") == []
    assert windows("short text") == [(0, 10)]
    try:
        windows("a b", size=2, overlap=2)
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid overlap was accepted")

    # The simple punctuation splitter can mistake an abbreviation for a sentence end.
    abbreviation_example = "Dr. Ali submitted the form. The office replied."
    abbreviation_parts = [abbreviation_example[a:b].strip() for a, b in zip(
        [0] + [m.end() for m in re.finditer(r"[.!?](?:\s+|$)", abbreviation_example)],
        [m.end() for m in re.finditer(r"[.!?](?:\s+|$)", abbreviation_example)] + [len(abbreviation_example)]) if abbreviation_example[a:b].strip()]
    assert abbreviation_parts[0] == "Dr."

    long_sentence = " ".join(["word"] * 95) + "."
    long_spans = sentence_chunks(long_sentence, size=40)
    assert len(long_spans) == 3
    assert all(count_words(long_sentence[a:b]) <= 40 for a, b in long_spans)

    for strategy in ("0", "10", "sentence"):
        for chunk in make_chunks(DOCS, strategy):
            original = DOCS[chunk["doc"]]
            assert chunk["text"] == original[chunk["start"]:chunk["end"]]
            assert 0 <= chunk["start"] < chunk["end"] <= len(original)
            assert count_words(chunk["text"]) <= 40


def main():
    run_tests()
    print("TASK 2 CHUNKING COMPARISON")
    print("All documents are synthetic teaching data.")
    print("Document word counts:")
    for doc_id, text in DOCS.items():
        n = count_words(text)
        print(f"  {doc_id}: {n} words")
        assert 150 <= n <= 250, f"{doc_id} must contain 150-250 words (got {n})"

    original_total = sum(count_words(t) for t in DOCS.values())
    for strategy in ("0", "10", "sentence"):
        chunks = make_chunks(DOCS, strategy)
        sizes = [count_words(c["text"]) for c in chunks]
        emitted_total = sum(sizes)
        repeated = emitted_total - original_total
        print(f"\nStrategy: {strategy} ({'sentence-aware' if strategy == 'sentence' else '40-word windows, overlap ' + strategy})")
        print(f"  chunks={len(chunks)}; min_words={min(sizes)}; max_words={max(sizes)}; average_words={sum(sizes)/len(sizes):.1f}")
        print(f"  repeated_word_units={repeated}")
        for doc_id, evidence in EVIDENCE.items():
            containing = [c["id"] for c in chunks if c["doc"] == doc_id and evidence in c["text"]]
            print(f"  full_rule_and_exception_in_one_chunk [{doc_id}]: {'YES ' + ', '.join(containing) if containing else 'NO'}")
        for c in chunks:
            print(f"  {c['id']} | source={c['source']} | offsets={c['start']}:{c['end']} | words={count_words(c['text'])}")
            print(f"    {c['text']}")

    print("\nEDGE-CASE TESTS")
    print("  empty text: PASS")
    print("  short document: PASS")
    print("  invalid overlap: PASS (ValueError raised)")
    print("  95-word sentence fallback: PASS (split into 3 chunks)")
    print("  abbreviation limitation: CONFIRMED (\"Dr.\" is split incorrectly)")
    print("  source offsets reproduce exact text: PASS")
    print("\nAll Task 2 chunking tests passed.")


if __name__ == "__main__":
    main()
    
