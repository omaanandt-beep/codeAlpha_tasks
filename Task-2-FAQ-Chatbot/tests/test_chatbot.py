"""
Unit and integration tests for FAQChatbot matching engine.
Verifies dataset loading, schema validation, exact matching, paraphrasing,
threshold calibration, fallback behavior, search, and edge cases.
"""

import json
import os
import tempfile
import pytest

from chatbot import FAQChatbot, FAQValidationError, DEFAULT_SIMILARITY_THRESHOLD


@pytest.fixture
def chatbot():
    return FAQChatbot()


# --- Dataset and Validation Tests ---

def test_dataset_loaded_count(chatbot):
    """Verify that at least 60 FAQs are loaded."""
    assert chatbot.get_total_count() >= 60
    assert len(chatbot.categories) >= 8


def test_missing_dataset_file():
    with pytest.raises(FileNotFoundError):
        FAQChatbot(dataset_path="non_existent_directory/missing_faqs.json")


def test_invalid_json_file(tmp_path):
    bad_json = tmp_path / "bad.json"
    bad_json.write_text("{ this is not valid json }", encoding="utf-8")
    with pytest.raises(FAQValidationError):
        FAQChatbot(dataset_path=str(bad_json))


def test_empty_dataset_file(tmp_path):
    empty_json = tmp_path / "empty.json"
    empty_json.write_text("[]", encoding="utf-8")
    with pytest.raises(FAQValidationError):
        FAQChatbot(dataset_path=str(empty_json))


def test_validation_detects_missing_fields(chatbot):
    malformed_records = [
        {"id": "test-1", "question": "Q1", "answer": "A1"} # missing category & alternatives
    ]
    valid, errors = chatbot.validate_faq_records(malformed_records)
    assert len(valid) == 0
    assert any("missing required fields" in err for err in errors)


def test_validation_detects_duplicate_ids(chatbot):
    duplicate_records = [
        {
            "id": "dup-1",
            "category": "Cat A",
            "question": "First Q?",
            "alternatives": ["Alt 1"],
            "answer": "Ans 1",
        },
        {
            "id": "dup-1",
            "category": "Cat B",
            "question": "Second Q?",
            "alternatives": ["Alt 2"],
            "answer": "Ans 2",
        },
    ]
    valid, errors = chatbot.validate_faq_records(duplicate_records)
    assert len(valid) == 1
    assert any("Duplicate FAQ ID" in err for err in errors)


# --- Query Matching Tests ---

def test_empty_query(chatbot):
    result = chatbot.match_query("")
    assert result["matched"] is False
    assert result["is_fallback"] is True
    assert result["score"] == 0.0


def test_whitespace_and_punctuation_query(chatbot):
    result = chatbot.match_query("   ???   ")
    assert result["matched"] is False
    assert result["is_fallback"] is True


def test_exact_canonical_question_match(chatbot):
    query = "Why is my laptop running so slow and how can I speed it up?"
    result = chatbot.match_query(query)
    assert result["matched"] is True
    assert result["is_fallback"] is False
    assert result["faq_id"] == "hw-01"
    assert result["score"] > 0.85
    assert "Task Manager" in result["answer"]


def test_alternative_phrasing_match(chatbot):
    """Query matches an indexed alternative phrasing."""
    query = "PC running very slow and freezing"
    result = chatbot.match_query(query)
    assert result["matched"] is True
    assert result["faq_id"] == "hw-01"
    assert result["score"] > 0.70


def test_paraphrased_query_match(chatbot):
    """User asks question in realistic, conversational terms."""
    query = "how can i fix my noisy computer fan that is getting super hot"
    result = chatbot.match_query(query)
    assert result["matched"] is True
    assert result["faq_id"] == "hw-03"
    assert "fan" in result["answer"].lower()


def test_wifi_issue_matching(chatbot):
    query = "why does my internet say connected no internet"
    result = chatbot.match_query(query)
    assert result["matched"] is True
    assert result["faq_id"] == "net-01"
    assert "ipconfig /flushdns" in result["answer"]


def test_bsod_troubleshooting(chatbot):
    query = "Windows crashed with blue screen of death"
    result = chatbot.match_query(query)
    assert result["matched"] is True
    assert result["faq_id"] == "hw-04"
    assert "BSOD" in result["answer"] or "Blue Screen" in result["answer"]


def test_unrelated_query_rejection(chatbot):
    """Verify out-of-scope or irrelevant queries trigger fallback."""
    unrelated_queries = [
        "How do I bake a chocolate cake?",
        "What is the capital of Australia?",
        "Who won the 1994 FIFA World Cup?",
        "How do I plant tomatoes in my garden?",
    ]
    for q in unrelated_queries:
        res = chatbot.match_query(q)
        assert res["matched"] is False, f"Expected '{q}' to be rejected, but got score {res['score']}"
        assert res["is_fallback"] is True
        assert res["score"] < chatbot.similarity_threshold


def test_threshold_behavior(chatbot):
    """Test that similarity threshold strictly distinguishes relevant from weak matches."""
    strict_bot = FAQChatbot(similarity_threshold=0.99)
    result = strict_bot.match_query("laptop slow")
    # Score will be moderate (<0.99), so should fallback under strict threshold
    assert result["matched"] is False
    assert result["is_fallback"] is True


def test_unicode_query_matching(chatbot):
    query = "How to fix Café’s Wi-Fi connected no internet?"
    result = chatbot.match_query(query)
    assert result["matched"] is True
    assert result["faq_id"] == "net-01"


def test_suggested_questions(chatbot):
    suggestions = chatbot.get_suggested_questions(count=4)
    assert len(suggestions) == 4
    # Ensure they are valid questions from the dataset
    canonical_qs = {faq["question"] for faq in chatbot.faqs}
    for q in suggestions:
        assert q in canonical_qs


def test_search_faqs_by_keyword(chatbot):
    results = chatbot.search_faqs("safe mode", category="All")
    assert len(results) >= 1
    assert any("Safe Mode" in r["question"] for r in results)


def test_search_faqs_by_category(chatbot):
    category = "Internet and Wi-Fi Problems"
    results = chatbot.search_faqs("", category=category)
    assert len(results) >= 7
    for r in results:
        assert r["category"] == category

