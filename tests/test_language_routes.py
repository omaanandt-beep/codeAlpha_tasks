"""
tests/test_language_routes.py
-----------------------------
Unit tests for RouteRegistry, requested language inventory, and pivot routing.
"""

import pytest
from language_routes import RouteRegistry, REQUESTED_LANGUAGES


def test_requested_languages_count():
    """Verify that all 15 target languages are defined."""
    assert len(REQUESTED_LANGUAGES) >= 15
    assert "en" in REQUESTED_LANGUAGES
    assert "hi" in REQUESTED_LANGUAGES
    assert "es" in REQUESTED_LANGUAGES
    assert "ja" in REQUESTED_LANGUAGES
    assert "zh" in REQUESTED_LANGUAGES
    assert "ar" in REQUESTED_LANGUAGES
    assert "bn" in REQUESTED_LANGUAGES
    assert "ur" in REQUESTED_LANGUAGES


def test_same_language_route():
    """Translating from a language to itself should return 'same'."""
    registry = RouteRegistry()
    assert registry.check_route("en", "en") == "same"
    assert registry.check_route("hi", "hi") == "same"
    assert registry.check_route("es", "es") == "same"


def test_route_badge_descriptions():
    """Verify badge output descriptions."""
    registry = RouteRegistry()
    label, desc = registry.get_route_description("en", "en")
    assert label == "Identical Language"
    assert "identical" in desc.lower()


def test_unsupported_route_handling():
    """Verify that uninstalled models report as unsupported or missing."""
    registry = RouteRegistry()
    # Check dummy code
    status = registry.check_route("xx", "yy")
    assert status == "unsupported"
    label, desc = registry.get_route_description("xx", "yy")
    assert "Missing" in label

