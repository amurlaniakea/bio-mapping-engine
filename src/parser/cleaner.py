import re


class CleanText:
    """
    A utility class to clean raw text extracted from the PDF.
    """

    def clean(self, text: str) -> str:
        """
        Removes page numbers, extra whitespace, and standardizes newlines.
        """
        if not text:
            return ""

        # 1. Remove page markers if they exist (e.g., "--- PAGE 26 ---")
        text = re.sub(r"--- PAGE \d+ ---", "", text)

        # 2. Remove standalone page numbers (lines that only contain digits)
        text = re.sub(r"^\s*\d+\s*$", "", text, flags=re.MULTILINE)

        # 3. Normalize whitespace: replace multiple spaces/tabs with a single space
        text = re.sub(r"[ \t]+", " ", text)

        # 4. Normalize newlines: replace 3+ newlines with just 2
        text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)

        # 5. Strip leading/trailing whitespace from the whole document
        return text.strip()


if __name__ == "__main__":
    # Quick test
    cleaner = CleanText()
    sample = "  \n  26  \n  ACNÉ \n  \n  \n  Conflicto : Conflicto de identidad...  "
    print(f"Original: '{sample}'")
    print(f"Cleaned:  '{cleaner.clean(sample)}'")
