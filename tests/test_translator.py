"""
tests/test_translator.py
------------------------
Unit tests for OfflineTranslator logic, validation, chunking, and language detection.
"""

import pytest
from translator import OfflineTranslator, TranslationError


@pytest.fixture
def translator():
    return OfflineTranslator()


def test_empty_or_whitespace_input(translator):
    """Empty or whitespace-only inputs should raise TranslationError gracefully."""
    with pytest.raises(TranslationError, match="empty or contains only whitespace"):
        translator.translate("", "en", "hi")

    with pytest.raises(TranslationError, match="empty or contains only whitespace"):
        translator.translate("   \n\t  ", "en", "hi")


def test_identical_source_and_target(translator):
    """Translating identical source and target should return original text without error."""
    text = "Hello world! This is a test."
    result, route = translator.translate(text, "en", "en")
    assert result == text
    assert route == "same"


def test_chunking_preserves_paragraphs(translator):
    """Ensure chunking retains paragraph breaks."""
    text = "First paragraph here.\n\nSecond paragraph here."
    chunks = translator._split_into_chunks(text, max_chars=100)
    assert any(c == "\n__PARA_BREAK__\n" for c in chunks)


def test_local_language_detection(translator):
    """Test offline language detection for distinct scripts."""
    # Hindi in Devanagari script
    detected_hi = translator.detect_language("यह एक परीक्षण वाक्य है जो भाषा का पता लगाता है।")
    assert detected_hi == "hi"

    # Spanish sentence
    detected_es = translator.detect_language("Este es un texto en idioma español para verificar.")
    assert detected_es == "es"

    # Extremely short string should return None (avoid false guessing)
    assert translator.detect_language("hi") is None

