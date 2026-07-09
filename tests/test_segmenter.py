from src.parser.segmenter import segment_symptoms


def test_segment_symptoms_basic():
    sample = "ACNÉ\nConflicto: Identidad\n\nACROMEGALIA\nEtapa: Supervivencia"
    segments = segment_symptoms(sample)
    assert len(segments) == 2
    assert segments[0]["header"] == "ACNÉ"
    assert "Conflicto: Identidad" in segments[0]["content"]
    assert segments[1]["header"] == "ACROMEGALIA"
    assert "Etapa: Supervivencia" in segments[1]["content"]


def test_segment_symptoms_ignore_index_entries():
    # Lines like 'ABSCESO 22' should be ignored and not create segments
    sample = "INTRODUCCION\nTexto inicial.\n\nABSCESO 22\nContenido del absceso.\n\nACNÉ\nConflicto: Identidad"
    segments = segment_symptoms(sample)
    # Should have: 1. INTRODUCCION, 2. ACNÉ.
    # 'ABSCESO 22' should be skipped.
    assert len(segments) == 2
    assert segments[0]["header"] == "INTRODUCCION"
    assert segments[1]["header"] == "ACNÉ"


def test_segment_symptoms_with_accents():
    sample = "ACNÉ\nConflicto\n\nÁRBOL\nContenido"
    segments = segment_symptoms(sample)
    assert len(segments) == 2
    assert segments[0]["header"] == "ACNÉ"
    assert segments[1]["header"] == "ÁRBOL"


def test_segment_symptoms_empty():
    assert segment_symptoms("") == []


def test_segment_symptoms_no_header():
    # If no valid header is found, it should treat the text as a single segment with header UNKNOWN
    sample = "Solo texto sin encabezados claros."
    segments = segment_symptoms(sample)
    assert len(segments) == 1
    assert segments[0]["header"] == "UNKNOWN"
    assert segments[0]["content"] == "Solo texto sin encabezados claros."
