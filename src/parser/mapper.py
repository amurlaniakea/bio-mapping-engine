import re
import uuid

# Expanded anatomical dictionary
ANATOMICAL_KEYWORDS = {
    "estómago": [
        "estómago",
        "gástrico",
        "digestivo",
        "vientre",
        "panza",
        "gastritis",
        "duodeno",
        "páncreas",
        "hígado",
        "riñón",
        "vesícula",
        "biliar",
    ],
    "piel": [
        "piel",
        "dermis",
        "cutáneo",
        "epidermis",
        "acné",
        "psoriasis",
        "manchas",
        "poros",
        "vello",
    ],
    "cara": [
        "cara",
        "rostro",
        "facial",
        "ojos",
        "boca",
        "labios",
        "mejillas",
        "lengua",
        "nariz",
        "oídos",
        "oído",
        "ojos",
    ],
    "espalda": ["espalda", "dorsal", "lumbar", "vertebra", "columna", "raquis"],
    "cuello": ["cuello", "cervical", "garganta", "faringe"],
    "pecho": [
        "pecho",
        "tórax",
        "pulmón",
        "respiratorio",
        "tráquea",
        "bronquio",
        "respiración",
        "aire",
    ],
    "extremidades": [
        "brazo",
        "pierna",
        "mano",
        "pie",
        "dedos",
        "extremidad",
        "rodilla",
        "tobillo",
        "codo",
        "cadera",
        "fémur",
        "articulación",
        "hueso",
        "músculo",
        "tendón",
    ],
    "cerebro": [
        "cerebro",
        "mental",
        "intelecto",
        "mente",
        "cognitivo",
        "neurona",
        "cráneo",
        "cabeza",
        "neurológico",
    ],
    "circulatorio": [
        "corazón",
        "arteria",
        "vena",
        "sangre",
        "pulso",
        "circulación",
        "cardíaco",
    ],
    "otros": ["órgano", "glándula", "hormona", "sistema"],
}

# Authors found in the document
AUTHORS = [
    "Louise L. Hay",
    "Lisa Bourbeau",
    "Jacques Martel",
    "Enric Corbera",
    "Salomon Sellam",
]


def extract_field(text: str, patterns: list[str]) -> str:
    """
    Helper to extract text following specific patterns.
    """
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if match:
            start = match.end()
            lines = text[start:].split("\n")
            if len(lines) > 1 and lines[1].strip():
                field_markers = [
                    "conflicto",
                    "causa",
                    "modelo",
                    "bloqueo",
                    "etapa",
                    "resentir",
                ]
                if not any(marker in lines[1].lower() for marker in field_markers):
                    return (lines[0].strip() + " " + lines[1].strip()).strip()
            return lines[0].strip()
    return ""


def map_segment(segment: dict) -> dict:
    """
    Transforms a raw segment (header + content) into a structured dictionary.
    """
    header = segment["header"].strip().upper()
    content = segment["content"]

    # Filter out navigation/noise segments
    BLACKLIST = {
        "DE",
        "A",
        "EL",
        "LA",
        "LOS",
        "LAS",
        "DICCIONARIO",
        "INDICE",
        "ÍNDICE",
        "PÁGINA",
        "PAGINA",
        "BIODESCODIFICACIÓN",
        "BIODESCODIFICACION",
    }
    if len(header) < 3 or header in BLACKLIST:
        return None

    # Initialize the structured object
    mapped_item = {
        "id": str(uuid.uuid4()),
        "sintoma_canonico": header,
        "zonas_detectadas": [],
        "sistema_padre": "Desconocido",
        "interpretaciones": [],
        "keywords": [],
    }

    # 1. Detect Zones (Anatomical Mapping)
    content_lower = content.lower()
    for zone, keywords in ANATOMICAL_KEYWORDS.items():
        if any(kw in content_lower for kw in keywords) or any(
            kw in header.lower() for kw in keywords
        ):
            if zone not in mapped_item["zonas_detectadas"]:
                mapped_item["zonas_detectadas"].append(zone)

    # 2. Split content by Author to create multiple interpretations
    author_pattern = r"(" + "|".join([re.escape(a) for a in AUTHORS]) + r")[\s:]+"
    parts = re.split(author_pattern, content, flags=re.IGNORECASE)

    if len(parts) > 1:
        for i in range(1, len(parts), 2):
            raw_author_name = parts[i].strip()
            auth_map = {a.upper(): a for a in AUTHORS}
            author_name = auth_map.get(raw_author_name.upper(), raw_author_name)

            author_content = parts[i + 1] if i + 1 < len(parts) else ""

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

            # Fallback para autores sin prefijos o texto directo (ej. Jacques Martel o descripción pura)
            if (
                not interpretation["conflicto_emocional"]
                and not interpretation["modelo_mental"]
            ):
                clean_content = author_content.strip()
                if clean_content:
                    lines = clean_content.split("\n")
                    interpretation["conflicto_emocional"] = (
                        lines[0] + (" " + lines[1] if len(lines) > 1 else "")
                    ).strip()

            mapped_item["interpretaciones"].append(interpretation)
    else:
        mapped_item["interpretaciones"].append(
            {
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
            }
        )

    # 3. Keywords
    mapped_item["keywords"] = list(set(header.lower().split()))

    return mapped_item
