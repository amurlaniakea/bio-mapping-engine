import re
import uuid

# Internal anatomical dictionary for first-pass zone detection
# In a real production environment, this would be a much larger, 
# potentially externalized ontology.
ANATOMICAL_KEYWORDS = {
    "estómago": ["estómago", "gástrico", "digestivo", "vientre", "panza"],
    "piel": ["piel", "dermis", "cutáneo", "epidermis", "acné", "psoriasis", "manchas"],
    "cara": ["cara", "rostro", "facial", "ojos", "boca", "labios", "mejillas", "lengua"],
    "espalda": ["espalda", "dorsal", "lumbar", "vertebra", "columna", "raquis"],
    "cuello": ["cuello", "cervical", "garganta", "faringe"],
    "pecho": ["pecho", "tórax", "pulmón", "respiratorio"],
    "extremidades": ["brazo", "pierna", "mano", "pie", "dedos", "extremidad"],
    "cerebro": ["cerebro", "mental", "intelecto", "mente", "cognitivo"]
}

# Authors found in the document
AUTHORS = ["Louise L. Hay", "Lisa Bourbeau", "Jacques Martel", "Enric Corbera", "Salomon Sellam"]

def map_segment(segment: dict) -> dict:
    """
    Transforms a raw segment (header + content) into a structured dictionary.
    """
    header = segment["header"].strip().upper()
    content = segment["content"]
    
    # Initialize the structured object
    mapped_item = {
        "id": str(uuid.uuid4()),
        "sintoma_canonico": header,
        "zonas_detectadas": [],
        "sistema_padre": "Desconocido", # Will be inferred or left as placeholder
        "interpretaciones": [],
        "keywords": []
    }

    # 1. Detect Zones (Anatomical Mapping)
    content_lower = content.lower()
    for zone, keywords in ANATOMICAL_KEYWORDS.items():
        if any(kw in content_lower for kw in keywords) or any(kw in header.lower() for kw in keywords):
            if zone not in mapped_item["zonas_detectadas"]:
                mapped_item["zonas_detectadas"].append(zone)

    # 2. Split content by Author to create multiple interpretations
    # We look for author names followed by a colon or just the name on a line.
    # This is a heuristic approach.
    
    # Pattern to split by author: "Author Name :" or "Author Name" at start of line
    author_pattern = r'(' + '|'.join([re.escape(a) for a in AUTHORS]) + r')[\s:]+'
    
    # We split the content by the author pattern, but we need to keep the author name.
    # re.split with a capturing group returns the matched delimiters in the list.
    parts = re.split(author_pattern, content)
    
    # parts[0] is text before the first author
    # parts[1] is the first author name
    # parts[2] is the content for that author... and so on.
    
    if len(parts) > 1:
        for i in range(1, len(parts), 2):
            author_name = parts[i].strip()
            author_content = parts[i+1] if i+1 < len(parts) else ""
            
            interpretation = {
                "autor": author_name,
                "conflicto_emocional": extract_field(author_content, [r"Conflicto\s*:", r"Causa probable:", r"Bloqueo Emocional\s*:", r"Resentir:"]),
                "modelo_mental": extract_field(author_content, [r"Nuevo modelo mental:", r"Bloqueo Mental\s*:", r"Bloqueo Espiritual\s*:"]),
                "etapa_biologica": extract_field(author_content, [r"(\d+[ªº] Etapa.*)"])
            }
            mapped_item["interpretaciones"].append(interpretation)
    else:
        # If no specific author is found, treat the whole block as a generic interpretation
        mapped_item["interpretaciones"].append({
            "autor": "General/No especificado",
            "conflicto_emocional": extract_field(content, [r"Conflicto\s*:", r"Causa probable:", r"Bloqueo Emocional\s*:", r"Resentir:"]),
            "modelo_mental": extract_field(content, [r"Nuevo modelo mental:", r"Bloqueo Mental\s*:", r"Bloqueo Espiritual\s*:"]),
            "etapa_biologica": extract_field(content, [r"(\d+[ªº] Etapa.*)"])
        })

    # 3. Keywords (Simple heuristic: words in header and first few words of content)
    mapped_item["keywords"] = list(set(header.lower().split()))

    return mapped_item

def extract_field(text: str, patterns: list[str]) -> str:
    """
    Helper to extract text following specific patterns.
    """
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if match:
            # Return the part after the pattern, up to the end of line or next major break
            start = match.end()
            remaining = text[start:].split('\n')[0].strip()
            return remaining
    return ""

if __name__ == "__main__":
    # Quick test
    test_segment = {
        "header": "ACNÉ",
        "content": "Louise L. Hay: Causa probable: No aceptación de uno mismo. Nuevo modelo mental: Soy divina. \nLisa Bourbeau: Bloqueo Emocional: Deseo de no acercarse."
    }
    print(map_segment(test_segment))
