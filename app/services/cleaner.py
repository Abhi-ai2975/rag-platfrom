import re


def clean_text(text: str) -> str:
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Join words broken across PDF line wrapping.
    text = re.sub(r"-\n(?=\w)", "", text)

    # Convert remaining newlines to spaces.
    text = re.sub(r"\n+", " ", text)

    # Normalize whitespace.
    text = re.sub(r"\s+", " ", text)

    return text.strip()
