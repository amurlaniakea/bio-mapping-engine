import re


def clean_text(text: str) -> str:
    """
    Cleans raw text extracted from the PDF.
    Removes page numbers, extra whitespace, and standardizes newlines.
    """
    if not text:
        return ""

    # 1. Remove page markers if they exist (e.g., "--- PAGE 26 ---")
    text = re.sub(r"--- PAGE \d+ ---", "", text)

    # 2. Remove standalone page numbers (lines that only contain digits)
    # This handles the "26", "27", etc. seen in the text
    text = re.sub(r"^\s*\d+\s*$", "", text, flags=re.MULTILINE)

    # 3. Normalize whitespace: replace multiple spaces/tabs with a single space
    text = re.sub(r"[ \t]+", " ", text)

    # 4. Normalize newlines: replace 3+ newlines with just 2 (to keep paragraph breaks but remove excessive gaps)
    text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)

    # 5. Strip leading/trailing whitespace from the whole document
    text = text.strip()

    return text


if __name__ == "__main__":
    # Quick test
    sample = "  \n  26  \n  ACNÉ \n  \n  \n  Conflicto : Conflicto de identidad...  "
    print(f"Original: '{sample}'")
    print(f"Cleaned:  '{clean_text(sample)}'")
