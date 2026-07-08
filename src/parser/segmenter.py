import re

def segment_symptoms(text: str) -> list[dict]:
    """
    Segments clean text into logical blocks, where each block starts with a symptom header.
    Expected header format: A line consisting of uppercase letters (may include accents).
    """
    if not text:
        return []

    # Pattern for a header: A line that is mostly uppercase and stands alone.
    # We allow accents (A-Z and common Spanish accents).
    # We use a lookahead/lookbehind or just split by lines.
    
    lines = text.split('\n')
    segments = []
    current_header = None
    current_content = []

    # Regex for a header: Line with only Uppercase letters, accents, and maybe some spaces.
    # We avoid lines that are too long (likely paragraphs) or too short (likely page numbers, though cleaner should have removed them).
    header_pattern = re.compile(r'^[A-ZÁÉÍÓÚÑ ]+$')

    for line in lines:
        stripped_line = line.strip()
        
        if not stripped_line:
            if current_header:
                current_content.append(stripped_line)
            continue

        # Check if the line is a header
        # We add a length constraint to avoid matching short words like "Y" or "A" if they aren't headers, 
        # but headers in this PDF seem to be clear.
        if header_pattern.match(stripped_line) and len(stripped_line) > 2:
            # If we already have a header, save the previous segment
            if current_header:
                segments.append({
                    "header": current_header,
                    "content": "\n".join(current_content).strip()
                })
            
            # Start new segment
            current_header = stripped_line
            current_content = []
        else:
            # It's part of the content of the current header
            if current_header:
                current_content.append(stripped_line)
            else:
                # This handles text appearing before the first header
                if stripped_line:
                    current_content.append(stripped_line)

    # Add the last segment
    if current_header:
        segments.append({
            "header": current_header,
            "content": "\n".join(current_content).strip()
        })
    elif current_content:
        # If no header was ever found, treat the whole thing as one block
        segments.append({
            "header": "UNKNOWN",
            "content": "\n".join(current_content).strip()
        })

    return segments

if __name__ == "__main__":
    # Quick test
    sample = """
    ACNÉ
    2ª Etapa (Protección).
    Conflicto : Conflicto de identidad.
    
    ACROMEGALIA
    1ª Etapa (Supervivencia).
    Hormona TSH.
    """
    results = segment_symptoms(sample)
    for r in results:
        print(f"HEADER: {r['header']}")
        print(f"CONTENT: {r['content']}")
        print("-" * 10)
