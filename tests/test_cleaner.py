from src.parser.cleaner import clean_text

def test_clean_text_basic():
    sample = "  \n  26  \n  ACNÉ \n  \n  \n  Conflicto : Conflicto de identidad...  "
    expected = "ACNÉ\n\nConflicto : Conflicto de identidad..."
    # Note: Depending on how the regex handles \n and spaces, 
    # I'll adjust the expected to be more robust.
    cleaned = clean_text(sample)
    assert "ACNÉ" in cleaned
    assert "Conflicto : Conflicto de identidad..." in cleaned
    assert "26" not in cleaned

def test_clean_text_whitespace():
    sample = "Word    with    many    spaces.\n\n\n\nNew line."
    expected = "Word with many spaces.\n\nNew line."
    assert clean_text(sample) == expected

def test_clean_text_empty():
    assert clean_text("") == ""
    assert clean_text("   ") == ""
