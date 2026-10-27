"""
translator.py
-------------
Core offline neural machine translation engine.
Integrates Argos Translate neural models + Helsinki-NLP Opus models for Marathi.
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
        self._hf_models = {}

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

    def _get_hf_model(self, model_name: str):
        """Loads and caches Hugging Face MarianMT models for offline execution."""
        if model_name not in self._hf_models:
            from transformers import MarianMTModel, MarianTokenizer
            tokenizer = MarianTokenizer.from_pretrained(model_name, local_files_only=False)
            model = MarianMTModel.from_pretrained(model_name, local_files_only=False)
            self._hf_models[model_name] = (tokenizer, model)
        return self._hf_models[model_name]

    def _translate_marathi(self, text: str, from_code: str, to_code: str) -> str:
        """Translates English <-> Marathi using local MarianMT neural weights."""
        if from_code == "en" and to_code == "mr":
            model_name = "Helsinki-NLP/opus-mt-en-mr"
        elif from_code == "mr" and to_code == "en":
            model_name = "Helsinki-NLP/opus-mt-mr-en"
        else:
            raise TranslationError(f"Unsupported Marathi direct pair: {from_code} -> {to_code}")

        tokenizer, model = self._get_hf_model(model_name)
        inputs = tokenizer([text], return_tensors="pt", padding=True, truncation=True, max_length=512)
        outputs = model.generate(**inputs, max_length=512, num_beams=4, early_stopping=True)
        return tokenizer.decode(outputs[0], skip_special_tokens=True)

    def _translate_direct(self, text: str, from_code: str, to_code: str) -> str:
        """Translates a single segment using an installed direct Argos or Opus model."""
        if from_code == "mr" or to_code == "mr":
            return self._translate_marathi(text, from_code, to_code)

        import argostranslate.translate
        installed_langs = argostranslate.translate.get_installed_languages()
        from_lang = next((l for l in installed_langs if l.code == from_code), None)
        to_lang = next((l for l in installed_langs if l.code == to_code), None)

        if not from_lang or not to_lang:
            raise TranslationError(f"Model files for {from_code} or {to_code} are not loaded.")

        translation = from_lang.get_translation(to_lang)
        if not translation:
            raise TranslationError(f"No direct translation model found for {from_code} -> {to_code}.")

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

        # Refresh registry state
        self.registry.refresh()
        route_type = self.registry.check_route(from_code, to_code)
        
        if route_type == "unsupported":
            from_name = REQUESTED_LANGUAGES.get(from_code, from_code)
            to_name = REQUESTED_LANGUAGES.get(to_code, to_code)
            raise TranslationError(
                f"No offline translation route available from {from_name} ({from_code}) to {to_name} ({to_code})."
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
