import re
import uuid

# Internal anatomical dictionary for first-pass zone detection
ANATOMICAL_KEYWORDS = {
    "estómago": [
        "estómago", "gástrico", "digestivo", "vientre", "panza", "gastritis",
        "duodeno", "páncreas", "hígado", "riñón", "vesícula", "biliar"
    ],
    "piel": [
        "piel", "dermis", "cutáneo", "epidermis", "acné", "psoriasis",
        "manchas", "poros", "vello"
    ],
    "cara": [
        "cara", "rostro", "facial", "ojos", "boca", "labios", "mejillas",
        "lengua", "nariz", "oídos", "oído", "ojos"
    ],
    "espalda": ["espalda", "dorsal", "lumbar", "vertebra", "columna", "raquis"],
    "cuello": ["cuello", "cervical", "garganta", "faringe"],
    "pecho": [
        "pecho", "tórax", "pulmón", "respiratorio", "tráquea", "bronquio",
        "respiración", "aire"
    ],
    "extremidades": [
        "brazo", "pierna", "mano", "pie", "dedos", "extremidad", "rodilla",
        "tobillo", "codo", "cadera", "fémur", "articulación", "hueso",
        "músculo", "tendón"
    ],
    "cerebro": [
        "cerebro", "mental", "intelecto", "mente", "cognitivo", "neurona",
        "cráneo", "cabeza", "neurológico"
    ],
    "circulatorio": [
        "corazón", "arteria", "vena", "sangre", "pulso", "circulación", "cardíaco"
    ],
    "otros": ["órgano", "glándula", "hormona", "sistema"]
}

# Authors found in the document
AUTHORS = ["Louise L. Hay", "Lisa Bourbeau", "Jacques Martel", "Enric Corbera", "Salomon Sellam"]


def extract_field(text: str, patterns: list[str]) -> str:
    """
    Helper to extract text following specific patterns.
    """
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if match:
            start = match.end()
            lines = text[start:].split('\n')
            if len(lines) > 1 and lines[1].strip():
                field_markers = ["conflicto", "causa", "modelo", "bloqueo", "etapa", "resentir"]
                if not any(marker in lines[1].lower() for marker in field_markers):
                    return (lines[0].strip() + " " + lines[1].strip()).strip()
            return lines[0].strip()
    return ""


def _detect_zones(header: str, content: str) -> list[str]:
    """Detect anatomical zones from header and content."""
    zones = []
    content_lower = content.lower()
    header_lower = header.lower()
    for zone, keywords in ANATOMICAL_KEYWORDS.items():
        if any(kw in content_lower for kw in keywords) or any(
            kw in header_lower for kw in keywords
        ):
            if zone not in zones:
                zones.append(zone)
    return zones


def _get_interpretations(content: str) -> list[dict]:
    """Extract author-based interpretations."""
    author_pattern = r'(' + '|'.join([re.escape(a) for a in AUTHORS]) + r')[\s:]+'
    parts = re.split(author_pattern, content, flags=re.IGNORECASE)
    interpretations = []

    if len(parts) > 1:
        for i in range(1, len(parts), 2):
            raw_author_name = parts[i].strip()
            auth_map = {a.upper(): a for a in AUTHORS}
            author_name = auth_map.get(raw_author_name.upper(), raw_author_name)
            author_content = parts[i+1] if i+1 < len(parts) else ""

            interpretation = {
                "autor": author_name,
                "conflicto_emocional": extract_field(
                    author_content,
                    [
                        r"Conflicto[\s\-—:|]+",
                        r"Causa probable[\s\-—:|]+",
                        r"Bloqueo Emocional[\s\-—:|]+",
                        r"Resentir[\s\-—:|]+",
                    ],
                ),
                "modelo_mental": extract_field(
                    author_content,
                    [
                        r"Nuevo modelo mental[\s\-—:|]+",
                        r"Bloqueo Mental[\s\-—:|]+",
                        r"Bloqueo Espiritual[\s\-—:|]+",
                    ],
                ),
                "etapa_biologica": extract_field(
                    author_content, [r"(\d+[ªº]\s*Etapa.*)"]
                ),
            }

            # Fallback for authors without prefixes
            if not interpretation["conflicto_emocional"] and not interpretation["modelo_mental"]:
                clean_content = author_content.strip()
                if clean_content:
                    lines = clean_content.split("\n")
                    interpretation["conflicto_emocional"] = (
                        lines[0] + (" " + lines[1] if len(lines) > 1 else "")
                    ).strip()

            interpretations.append(interpretation)
    else:
        # General fallback
        interpretations.append({
            "autor": "General/No especificado",
            "conflicto_emocional": extract_field(
                content,
                [
                    r"Conflicto[\s\-—:|]+",
                    r"Causa probable[\s\-—:|]+",
                    r"Bloqueo Emocional[\s\-—:|]+",
                    r"Resentir[\s\-—:|]+",
                ],
            ),
            "modelo_mental": extract_field(
                content,
                [
                    r"Nuevo modelo mental[\s\-—:|]+",
                    r"Bloqueo Mental[\s\-—:|]+",
                    r"Bloqueo Espiritual[\s\-—:|]+",
                ],
            ),
            "etapa_biologica": extract_field(content, [r"(\d+[ªº]\s*Etapa.*)"]),
        })
    return interpretations


def _apply_global_fallback(mapped_item: dict, content: str) -> None:
    """Apply fallback if no author-based interpretations found."""
    for interp in mapped_item["interpretaciones"]:
        if not interp["conflicto_emocional"] and not interp["modelo_mental"]:
            if interp["autor"] == "General/No especificado":
                target_text = content
            else:
                try:
                    author_regex = re.compile(
                        re.escape(interp["autor"]) + r"[\s:]+", re.IGNORECASE
                    )
                    match = author_regex.search(content)
                    if match:
                        target_text = content[match.end():]
                        next_author_pattern = (
                            r"(" + "|".join([re.escape(a) for a in AUTHORS]) + r")[\s:]+"
                        )
                        next_match = re.search(next_author_pattern, target_text, re.IGNORECASE)
                        if next_match:
                            target_text = target_text[:next_match.start()]
                    else:
                        target_text = content
                except Exception:
                    target_text = content

            if target_text.strip():
                lines = target_text.strip().split("\n")
                interp["conflicto_emocional"] = (
                    lines[0] + (" " + lines[1] if len(lines) > 1 else "")
                ).strip()


def map_segment(segment: dict) -> dict:
    """
    Transforms a raw segment (header + content) into a structured dictionary.
    Refactored to reduce cognitive complexity and fix type-hinting issues.
    """
    header = segment.get("header", "").strip().upper()
    content = segment.get("content", "")

    # Filter out navigation/noise segments
    BLACKLIST = {
        "DE", "A", "EL", "LA", "LOS", "LAS", "DICCIONARIO",
        "INDICE", "ÍNDICE", "PÁGINA", "PAGINA"
    }

    if len(header) < 3 or header in BLACKLIST:
        return {"error": "Invalid segment structure"}

    mapped_item = {
        "id": str(uuid.uuid4()),
        "sintoma_canonico": header,
        "zonas_detectadas": _detect_zones(header, content),
        "sistema_padre": "Desconocido",
        "interpretaciones": _get_interpretations(content),
        "keywords": list(set(header.lower().split()))
    }

    _apply_global_fallback(mapped_item, content)

    return mapped_item
