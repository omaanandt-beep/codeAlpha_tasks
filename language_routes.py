"""
language_routes.py
------------------
Manages supported languages, native script labels, and verifies
installed Argos Translate translation routes (Direct vs Pivot via English).
"""

from typing import Dict, List, Optional, Tuple, Set

# Target 15 languages requested with English name + Native script label
REQUESTED_LANGUAGES: Dict[str, str] = {
    "en": "English",
    "hi": "Hindi (हिन्दी)",
    "es": "Spanish (Español)",
    "fr": "French (Français)",
    "de": "German (Deutsch)",
    "it": "Italian (Italiano)",
    "pt": "Portuguese (Português)",
    "ru": "Russian (Русский)",
    "ar": "Arabic (العربية)",
    "zh": "Chinese Simplified (简体中文)",
    "ja": "Japanese (日本語)",
    "ko": "Korean (한국어)",
    "bn": "Bengali (বাংলা)",
    "ur": "Urdu (اردو)",
    "tr": "Turkish (Türkçe)",
}


class RouteRegistry:
    """Discovers and verifies available translation routes from installed models."""

    def __init__(self):
        self._installed_languages: Dict[str, any] = {}
        self._direct_pairs: Set[Tuple[str, str]] = set()
        self.refresh()

    def refresh(self):
        """Scans the local Argos Translate model repository."""
        self._installed_languages.clear()
        self._direct_pairs.clear()

        try:
            import argostranslate.translate
            installed_langs = argostranslate.translate.get_installed_languages()
            for lang in installed_langs:
                self._installed_languages[lang.code] = lang

            for source_code, source_lang in self._installed_languages.items():
                for trans in source_lang.translations_from:
                    target_code = getattr(trans.to_lang, "code", None)
                    if target_code:
                        self._direct_pairs.add((source_code, target_code))
        except Exception:
            pass

    def get_installed_codes(self) -> List[str]:
        """Returns ISO codes of languages currently installed."""
        return list(self._installed_languages.keys())

    def get_supported_sources(self) -> Dict[str, str]:
        """Returns requested languages that have at least one valid outbound route."""
        sources = {}
        for code, label in REQUESTED_LANGUAGES.items():
            if code in self._installed_languages:
                if any(src == code for src, _ in self._direct_pairs):
                    sources[code] = label
        return sources

    def get_supported_targets(self, source_code: Optional[str] = None) -> Dict[str, str]:
        """Returns requested languages that can be reached from the given source."""
        targets = {}
        for code, label in REQUESTED_LANGUAGES.items():
            if source_code and code == source_code:
                continue
            if not source_code:
                if code in self._installed_languages:
                    targets[code] = label
            else:
                route_type = self.check_route(source_code, code)
                if route_type in ("direct", "pivot"):
                    targets[code] = label
        return targets

    def check_route(self, from_code: str, to_code: str) -> str:
        """
        Determines translation route feasibility:
        - 'same': source and target are identical
        - 'direct': a direct local model exists
        - 'pivot': an intermediate route exists through English (from -> en -> to)
        - 'unsupported': no route exists with currently installed models
        """
        if from_code == to_code:
            return "same"

        if (from_code, to_code) in self._direct_pairs:
            return "direct"

        # Check pivot via English ('en')
        if from_code != "en" and to_code != "en":
            has_from_en = (from_code, "en") in self._direct_pairs
            has_en_to = ("en", to_code) in self._direct_pairs
            if has_from_en and has_en_to:
                return "pivot"

        return "unsupported"

    def get_route_description(self, from_code: str, to_code: str) -> Tuple[str, str]:
        """Returns a user-friendly badge status and explanation for the UI."""
        route_type = self.check_route(from_code, to_code)
        from_name = REQUESTED_LANGUAGES.get(from_code, from_code)
        to_name = REQUESTED_LANGUAGES.get(to_code, to_code)

        if route_type == "same":
            return "Identical Language", "Source and target languages are identical."
        elif route_type == "direct":
            return "Direct Offline Model", f"High-fidelity direct neural translation ({from_code.upper()} -> {to_code.upper()})."
        elif route_type == "pivot":
            return "Pivot Route via English", f"Translating via English bridge ({from_code.upper()} -> EN -> {to_code.upper()}). Nuance may slightly vary."
        else:
            return "Model Missing", f"No installed route from {from_name} to {to_name}. Run setup_models.py to install."
