"""
translator.py
-------------
Core offline neural machine translation engine using Argos Translate.
Decoupled from Streamlit, handles paragraph/sentence preserving chunking,
local language detection, and English pivot routes.
"""

import re
from typing import Optional, Tuple
from language_routes import RouteRegistry, REQUESTED_LANGUAGES


class TranslationError(Exception):
    """Custom exception raised for invalid inputs or missing translation routes."""
    pass


class OfflineTranslator:
    def __init__(self):
        self.registry = RouteRegistry()

    def detect_language(self, text: str) -> Optional[str]:
        """
        Detects language locally without internet access.
        Returns ISO code if recognized and confident, else None.
        """
        clean_text = text.strip()
        if len(clean_text) < 4:
            return None
        try:
            from langdetect import detect, DetectorFactory
            DetectorFactory.seed = 0
            detected_code = detect(clean_text)
            # Map Chinese variants
            if detected_code.startswith("zh"):
                detected_code = "zh"
            return detected_code if detected_code in REQUESTED_LANGUAGES else None
        except Exception:
            return None

    def _split_into_chunks(self, text: str, max_chars: int = 400) -> list[str]:
        """
        Splits text preserving paragraphs and sentence boundaries.
        Avoids cutting mid-sentence.
        """
        paragraphs = text.split("\n")
        chunks = []

        for para in paragraphs:
            if not para.strip():
                chunks.append("")
                continue

            # Split sentences by punctuation (. ? ! । followed by space or end)
            sentences = re.split(r'(?<=[.?!।\n])\s+', para)
            current_chunk = ""

            for sentence in sentences:
                if len(current_chunk) + len(sentence) + 1 <= max_chars:
                    current_chunk = f"{current_chunk} {sentence}".strip() if current_chunk else sentence
                else:
                    if current_chunk:
                        chunks.append(current_chunk)
                    current_chunk = sentence

            if current_chunk:
                chunks.append(current_chunk)

            # Delimiter indicating newline between paragraphs
            chunks.append("\n__PARA_BREAK__\n")

        # Clean trailing paragraph break
        if chunks and chunks[-1] == "\n__PARA_BREAK__\n":
            chunks.pop()

        return chunks

    def _translate_direct(self, text: str, from_code: str, to_code: str) -> str:
        """Translates a single segment using an installed direct Argos model."""
        import argostranslate.translate

        installed_langs = argostranslate.translate.get_installed_languages()
        from_lang = next((l for l in installed_langs if l.code == from_code), None)
        to_lang = next((l for l in installed_langs if l.code == to_code), None)

        if not from_lang or not to_lang:
            raise TranslationError(f"Model files for {from_code} or {to_code} are not loaded.")

        translation = from_lang.get_translation(to_lang)
        if not translation:
            raise TranslationError(f"No direct translation model found for {from_code} → {to_code}.")

        return translation.translate(text)

    def translate(self, text: str, from_code: str, to_code: str) -> Tuple[str, str]:
        """
        Translates text between supported language codes.
        
        Returns:
            Tuple[str, str]: (translated_text, route_type)
        """
        if not text or not text.strip():
            raise TranslationError("Input text is empty or contains only whitespace.")

        if from_code == to_code:
            return text, "same"

        # Refresh registry state to capture newly installed models
        self.registry.refresh()
        route_type = self.registry.check_route(from_code, to_code)
        
        if route_type == "unsupported":
            from_name = REQUESTED_LANGUAGES.get(from_code, from_code)
            to_name = REQUESTED_LANGUAGES.get(to_code, to_code)
            raise TranslationError(
                f"No offline translation route available from {from_name} ({from_code}) to {to_name} ({to_code}). "
                "Please run 'python setup_models.py' to install the required model."
            )

        chunks = self._split_into_chunks(text)
        translated_parts = []

        for chunk in chunks:
            if chunk == "\n__PARA_BREAK__\n":
                translated_parts.append("\n")
                continue
            if not chunk.strip():
                continue

            if route_type == "direct":
                part = self._translate_direct(chunk, from_code, to_code)
            elif route_type == "pivot":
                # Translate through English pivot
                mid_text = self._translate_direct(chunk, from_code, "en")
                part = self._translate_direct(mid_text, "en", to_code)
            else:
                raise TranslationError(f"Unknown route type: {route_type}")

            translated_parts.append(part)

        # Reassemble preserving paragraphs
        result = " ".join(translated_parts).replace(" \n ", "\n").replace("\n ", "\n").strip()
        return result, route_type

