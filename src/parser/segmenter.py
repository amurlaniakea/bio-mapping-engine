import re

def segment_symptoms(text):
    header_pattern = re.compile(r"^[A-ZÁÉÍÓÚÑ ]+$")
    AUTHORS = [
        "Louise L. Hay",
        "Lisa Bourbeau",
        "Jacques Martel",
        "Enric Corbera",
        "Salomon Sellam",
    ]

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
            continue

        if is_header and not is_author:
            # Normalize for comparison (e.g., "EL PERITONEO" vs "PERITONEO")
            norm_new = re.sub(r"^(EL|LA|LOS|LAS)\s+", "", stripped_line, flags=re.IGNORECASE)
            
            if current_header:
                norm_curr = re.sub(r"^(EL|LA|LOS|LAS)\s+", "", current_header, flags=re.IGNORECASE)
                
                if norm_new.upper() == norm_curr.upper():
                    # MERGE: The new header is a duplicate. 
                    # We skip adding it as a new header and just continue to add its content.
                    # Note: Since headers themselves don't have content, this effectively
                    # merges the lines following the duplicate header into the current segment.
                    pass
                else:
                    # New unique header: close previous
                    segments.append({
                        "header": current_header,
                        "content": "\n".join(current_content).strip(),
                    })
                    current_header = stripped_line
                    current_content = []
            else:
                current_header = stripped_line
                current_content = []
        elif is_author:
            if current_header:
                current_content.append(line)
        else:
            if current_header:
                current_content.append(line)
            else:
                # Avoid creating UNKNOWN segments if possible, but for robustness:
                current_header = "UNKNOWN"
                current_content.append(line)

    if current_header:
        segments.append({
            "header": current_header,
            "content": "\n".join(current_content).strip(),
        })

    return segments
