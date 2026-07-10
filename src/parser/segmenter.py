import re

# Pre-compiled patterns
HEADER_PATTERN = re.compile(r"^[A-ZÁÉÍÓÚÑ ]+$")
ARTICLE_PREFIX = re.compile(r"^(EL|LA|LOS|LAS)\s+", re.IGNORECASE)
INDEX_ENTRY_SUFFIX = tuple(str(i) for i in range(10))

AUTHORS = [
    "Louise L. Hay",
    "Lisa Bourbeau",
    "Jacques Martel",
    "Enric Corbera",
    "Salomon Sellam",
]


def _normalize_header(header: str) -> str:
    """Normalize header by removing Spanish article prefixes."""
    return ARTICLE_PREFIX.sub("", header).upper()


def _is_header(line: str) -> bool:
    """Check if line is a valid header (uppercase, not an author)."""
    return bool(HEADER_PATTERN.match(line)) and not _is_author(line)


def _is_author(line: str) -> bool:
    """Check if line matches any known author."""
    line_upper = line.upper()
    return any(line_upper == auth.upper() for auth in AUTHORS)


def _is_index_entry(line: str) -> bool:
    """Check if line is an index entry (ends with digit)."""
    return line.endswith(INDEX_ENTRY_SUFFIX) and bool(
        re.search(r"\s+\d+$", line)
    )


def _close_segment(segments: list, header: str | None, content: list) -> None:
    """Close current segment and add to segments list."""
    if header:
        segments.append(
            {"header": header, "content": "\n".join(content).strip()}
        )


def segment_symptoms(text: str) -> list[dict]:
    """Parse text into symptom segments by headers and authors."""
    lines = text.split("\n")
    segments = []
    current_header = None
    current_content = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        if _is_index_entry(stripped):
            continue

        if _is_header(stripped):
            norm_new = _normalize_header(stripped)

            if current_header:
                norm_curr = _normalize_header(current_header)
                if norm_new == norm_curr:
                    # Duplicate header - merge content, continue
                    pass
                else:
                    _close_segment(segments, current_header, current_content)
                    current_header = stripped
                    current_content = []
            else:
                current_header = stripped
                current_content = []

        elif _is_author(stripped):
            if current_header:
                current_content.append(line)

        else:
            if current_header:
                current_content.append(line)
            else:
                current_header = "UNKNOWN"
                current_content.append(line)

    _close_segment(segments, current_header, current_content)
    return segments
