import re

MAX_WORDS = 20

CONNECTORS = [
    "and", "but", "because", "so",
    "which", "that", "who", "when", "while"
]

def split_into_sentences(text):
    # Tách câu theo dấu chấm, hỏi, cảm
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return sentences

def word_count(s):
    return len(s.split())

def split_long_sentence(sentence):
    parts = [sentence]

    # Ưu tiên tách theo dấu phẩy
    if "," in sentence:
        parts = [p.strip() for p in sentence.split(",")]

    results = []

    for part in parts:
        if word_count(part) <= MAX_WORDS:
            results.append(part)
        else:
            # Tách tiếp theo liên từ
            pattern = r'\b(' + '|'.join(CONNECTORS) + r')\b'
            sub_parts = re.split(pattern, part)

            temp = ""
            for sp in sub_parts:
                candidate = (temp + " " + sp).strip()
                if word_count(candidate) <= MAX_WORDS:
                    temp = candidate
                else:
                    if temp:
                        results.append(temp)
                    temp = sp

            if temp:
                results.append(temp)

    return results

def split_text(text):
    sentences = split_into_sentences(text)
    output = []

    for s in sentences:
        if word_count(s) <= MAX_WORDS:
            output.append(s)
        else:
            output.extend(split_long_sentence(s))

    return output
