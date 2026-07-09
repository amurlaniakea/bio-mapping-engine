import re

AUTHORS = [
    "Louise L. Hay",
    "Lisa Bourbeau",
    "Jacques Martel",
    "Enric Corbera",
    "Salomon Sellam",
]


def segment_symptoms(text):
    header_pattern = re.compile(r"^[A-ZÁÉÍÓÚÑ ]+$")

    lines = text.split("\n")
    segments = []
    current_header = None
    current_content = []

    for line in lines:
        stripped_line = line.strip()
        if not stripped_line:
            continue

        is_header = bool(header_pattern.match(stripped_line))
        is_author = any(stripped_line.upper() == auth.upper() for auth in AUTHORS)
        is_index_entry = bool(re.search(r"\s+\d+$", stripped_line))

        if is_index_entry:
            # Ignore the index line and its potential content by not changing the header
            continue

        if is_header and not is_author:
            if current_header:
                segments.append(
                    {
                        "header": current_header,
                        "content": "\n".join(current_content).strip(),
                    }
                )
            current_header = stripped_line
            current_content = []
        else:
            if current_header:
                current_content.append(line)
            else:
                # If we find content before any header, we treat it as UNKNOWN
                current_header = "UNKNOWN"
                current_content.append(line)

    # Finalize last segment
    if current_header:
        segments.append(
            {"header": current_header, "content": "\n".join(current_content).strip()}
        )

    return segments
