"""
Unit tests for NLP Preprocessing module.
Tests lowercase normalization, punctuation handling, tokenization,
negation preservation, lemmatization/stemming, unicode normalization, and edge cases.
"""

import pytest
from nlp_preprocessing import TextPreprocessor, preprocess_text


@pytest.fixture
def preprocessor():
    return TextPreprocessor()


def test_normalize_lowercase(preprocessor):
    text = "HOW DO I FIX A SLOW LAPTOP?"
    normalized = preprocessor.normalize_text(text)
    assert "how do i fix a slow laptop" == normalized


def test_whitespace_normalization(preprocessor):
    text = "  Laptop   is \t freezing \n\n badly  "
    normalized = preprocessor.normalize_text(text)
    assert normalized == "laptop is freezing badly"


def test_punctuation_handling(preprocessor):
    text = "Why is my Wi-Fi not working??? Help me, please!"
    normalized = preprocessor.normalize_text(text)
    # wi-fi is normalized to wifi and punctuation stripped
    assert "wifi" in normalized
    assert "?" not in normalized
    assert "!" not in normalized


def test_negation_preservation(preprocessor):
    """Critical test: verify negations are NOT stripped as stopwords."""
    text = "Laptop will not turn on and can't charge"
    preprocessed = preprocessor.preprocess(text)
    tokens = preprocessed.split()
    assert "not" in tokens
    # "can't" expands to "cannot" or "not", ensuring negative intent is preserved
    assert any(neg in tokens for neg in ["not", "cannot"])


def test_tech_keywords_protection(preprocessor):
    """Verify technical abbreviations are preserved."""
    text = "How to fix BSOD error and check IP address with CMD?"
    preprocessed = preprocessor.preprocess(text)
    assert "bsod" in preprocessed
    assert "ip" in preprocessed
    assert "cmd" in preprocessed


def test_unicode_normalization(preprocessor):
    """Verify smart quotes and accented characters normalize cleanly."""
    text = "Why won’t my Café’s Wi-Fi work?"
    preprocessed = preprocessor.preprocess(text)
    assert "wifi" in preprocessed
    assert "not" in preprocessed


def test_empty_and_whitespace_input(preprocessor):
    assert preprocessor.preprocess("") == ""
    assert preprocessor.preprocess("   ") == ""
    assert preprocessor.preprocess(None) == ""


def test_short_and_pure_punctuation(preprocessor):
    assert preprocessor.preprocess("???") == ""
    assert preprocessor.preprocess("!@#$%^&*()") == ""
    assert preprocessor.preprocess("a") == ""


def test_convenience_function():
    result = preprocess_text("How do I update Windows?")
    assert "update" in result
    assert "window" in result  # lemmatized from windows

