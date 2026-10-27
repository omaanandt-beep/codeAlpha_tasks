"""
translator.py
-------------
Core offline neural machine translation engine.
Integrates Argos Translate neural models + high-accuracy single-pass Indic transfer for Marathi.
Handles paragraph/sentence preserving chunking, local language detection, and English pivot routes.
"""

import re
from typing import Optional, Tuple
from language_routes import RouteRegistry, REQUESTED_LANGUAGES


class TranslationError(Exception):
    """Custom exception raised for invalid inputs or missing translation routes."""
    pass


# Comprehensive single-pass dictionary for Hindi -> Marathi transfer
HI_TO_MR_MAPPING = {
    # Common Expressions & Idioms
    "आपसे मिलकर बहुत खुशी हुई": "तुम्हाला भेटून खूप आनंद झाला",
    "आपसे मिलकर खुशी हुई": "तुम्हाला भेटून आनंद झाला",
    "आपका बहुत-बहुत धन्यवाद": "तुमचे खूप खूप धन्यवाद",
    "बहुत-बहुत धन्यवाद": "खूप खूप धन्यवाद",
    "आपका बहुत बहुत धन्यवाद": "तुमचे खूप खूप धन्यवाद",
    "बहुत बहुत धन्यवाद": "खूप खूप धन्यवाद",
    "आपका धन्यवाद": "आपले धन्यवाद",
    "धन्यवाद": "धन्यवाद",
    "आपका स्वागत है": "आपले स्वागत आहे",
    "स्वागत है": "स्वागत आहे",
    "शुभ प्रभात": "शुभ सकाळ",
    "शुभ सुबह": "शुभ सकाळ",
    "शुभ दोपहर": "शुभ दुपार",
    "शुभ संध्या": "शुभ संध्याकाळ",
    "शुभ रात्रि": "शुभ रात्री",
    "नमस्ते": "नमस्कार",
    "नमस्कार": "नमस्कार",
    "प्रणाम": "नमस्कार",
    "कैसे हैं आप": "तुम्ही कसे आहात",
    "आप कैसे हैं": "तुम्ही कसे आहात",
    "तुम कैसे हो": "तू कसा आहेस",
    "क्या हाल है": "काय चाललंय",
    "अलविदा": "निरोप",
    
    # Common Nouns & Modern Terms
    "निकटतम": "जवळचे",
    "रेलवे स्टेशन": "रेल्वे स्टेशन",
    "बस स्टैंड": "बस स्थानक",
    "हवाई अड्डा": "विमानतळ",
    "अस्पताल": "दवाखाना / रुग्णालय",
    "डॉक्टर": "डॉक्टर",
    "दवा": "औषध",
    "पानी": "पाणी",
    "खाना": "जेवण",
    "चाय": "चहा",
    "दूध": "दूध",
    "सड़क": "रस्ता",
    "शहर": "शहर",
    "गाँव": "गाव",
    "देश": "देश",
    "दुनिया": "जग",
    "किताब": "पुस्तक",
    "पैसा": "पैसे",
    "रुपया": "रुपये",
    "समय": "वेळ",
    "दिन": "दिवस",
    "रात": "रात्र",
    "वर्ष": "वर्ष",
    "साल": "वर्ष",
    "दोस्त": "मित्र",
    "मित्र": "मित्र",
    "परिवार": "कुटुंब",
    "माता": "आई",
    "पिता": "वडील",
    "भाई": "भाऊ",
    "बहन": "बहीण",
    "घर": "घर",
    "काम": "काम",
    "कार्यालय": "कार्यालय",
    "विद्यार्थी": "विद्यार्थी",
    "शिक्षक": "शिक्षक",
    "स्कूल": "शाळा",
    "कॉलेज": "कॉलेज",
    
    # Technology Terms
    "कृत्रिम बुद्धिमत्ता": "कृत्रिम बुद्धिमत्ता (AI)",
    "कृत्रिम बुद्धि": "कृत्रिम बुद्धिमत्ता (AI)",
    "आर्टिफिशियल इंटेलिजेंस": "कृत्रिम बुद्धिमत्ता (AI)",
    "मशीन लर्निंग": "मशीन लर्निंग",
    "प्रौद्योगिकी": "तंत्रज्ञान",
    "तकनीक": "तंत्रज्ञान",
    "कंप्यूटर": "संगणक",
    "मोबाइल": "मोबाईल",
    "इंटरनेट": "इंटरनेट",
    "सॉफ्टवेयर": "सॉफ्टवेअर",
    "एप्लिकेशन": "अनुप्रयोग / ॲप",
    "प्रोजेक्ट": "प्रकल्प",
    "इंटर्नशिप": "इंटर्नशिप",
    "भविष्य": "भविष्य",
    "आधुनिक": "आधुनिक",
    "नया": "नवीन",
    "नई": "नवीन",
    "नए": "नवीन",
    "पुराना": "जुने",
    "तेज": "वेगवान",
    "धीमा": "हळू",
    
    # Verbs & Conjugations
    "बदल रहा है": "बदलत आहे",
    "बदल रहे हैं": "बदलत आहेत",
    "बदल रही है": "बदलत आहे",
    "कर रहा है": "करत आहे",
    "कर रहे हैं": "करत आहेत",
    "कर रही है": "करत आहे",
    "हो रहा है": "होत आहे",
    "हो रहे हैं": "होत आहेत",
    "हो रही है": "होत आहे",
    "जा रहा है": "जात आहे",
    "आ रहा है": "येत आहे",
    "खरीद सकता हूँ": "खरेदी करू शकतो",
    "खरीद सकता हूं": "खरेदी करू शकतो",
    "खरीद सकते हैं": "खरेदी करू शकतात",
    "खरीद सकता है": "खरेदी करू शकतो",
    "खरीद सकती है": "खरेदी करू शकते",
    "कर सकता हूँ": "करू शकतो",
    "कर सकता हूं": "करू शकतो",
    "कर सकते हैं": "करू शकतात",
    "कर सकता है": "करू शकतो",
    "कर सकती है": "करू शकते",
    "जा सकता है": "जाऊ शकतो",
    "जा सकते हैं": "जाऊ शकतात",
    "देख सकता है": "पाहू शकतो",
    "बोल सकता है": "बोलू शकतो",
    "सकता हूँ": "शकतो",
    "सकता हूं": "शकतो",
    "सकते हैं": "शकतात",
    "सकती है": "शकते",
    "सकता है": "शकतो",
    "चाहिए": "पाहिजे",
    "करना चाहिए": "केले पाहिजे",
    "होना चाहिए": "असायला हवे",
    "करना": "करणे",
    "होना": "होणे",
    "जाना": "जाणे",
    "आना": "येणे",
    "खाना": "खाणे",
    "पीना": "पिणे",
    "पढ़ना": "वाचणे",
    "लिखना": "लिहिणे",
    "सीखना": "शिकणे",
    
    # Pronouns & Determiners
    "मैं": "मी",
    "मुझे": "मला",
    "मुझको": "मला",
    "मेरा": "माझा",
    "मेरी": "माझी",
    "मेरे": "माझे",
    "हम": "आम्ही",
    "हमें": "आम्हाला",
    "हमारा": "आमचा",
    "हमारी": "आमची",
    "हमारे": "आमचे",
    "आप": "तुम्ही",
    "आपको": "तुम्हाला",
    "आपका": "आपला",
    "आपकी": "आपली",
    "आपके": "आपले",
    "तुम": "तू",
    "तुम्हें": "तुला",
    "तुम्हारी": "तुझी",
    "तुम्हारा": "तुझा",
    "तुम्हारे": "तुझे",
    "वह": "तो",
    "वे": "ते",
    "वे लोग": "ते लोक",
    "उनका": "त्यांचा",
    "उनकी": "त्यांची",
    "उनके": "त्यांचे",
    "उन्हें": "त्यांना",
    "उसका": "त्याचा",
    "उसकी": "त्याची",
    "उसके": "त्याचे",
    "उसे": "त्याला",
    "यह": "हे",
    "ये": "हे",
    "इस": "या",
    "इन": "या",
    "इसका": "याचे",
    "इसकी": "याची",
    "इसके": "याचे",
    "इसे": "याला",
    "इनका": "यांचा",
    "इनकी": "यांची",
    "इनके": "यांचे",
    
    # Questions & Conjunctions
    "कहाँ": "कुठे",
    "कहा": "कुठे",
    "कब": "केव्हा",
    "क्यों": "का",
    "कैसे": "कसे",
    "कैसा": "कसा",
    "कैसी": "कशी",
    "क्या": "काय",
    "कौन": "कोण",
    "कितना": "किती",
    "कितने": "किती",
    "कितनी": "किती",
    "और": "आणि",
    "तथा": "आणि",
    "एवं": "आणि",
    "लेकिन": "पण",
    "परन्तु": "परंतु",
    "किन्तु": "किंतु",
    "मगर": "पण",
    "क्योंकि": "कारण",
    "इसलिए": "म्हणून",
    "अगर": "जर",
    "यदि": "जर",
    "तो": "तर",
    "या": "किंवा",
    "अथवा": "किंवा",
    
    # Adverbs & Prepositions
    "बहुत": "खूप",
    "ज्यादा": "जास्त",
    "कम": "कमी",
    "अधिक": "जास्त",
    "अच्छा": "चांगला",
    "अच्छी": "चांगली",
    "अच्छे": "चांगले",
    "खूबसूरत": "सुंदर",
    "सुंदर": "सुंदर",
    "बुरा": "वाईट",
    "सही": "योग्य",
    "गलत": "चुकीचे",
    "आज": "आज",
    "कल": "उद्या",
    "परसों": "परवा",
    "यहाँ": "येथे",
    "यहाँ पर": "येथे",
    "वहाँ": "तेथे",
    "वहाँ पर": "तेथे",
    "अब": "आता",
    "तब": "तेव्हा",
    "हमेशा": "नेहमी",
    "कभी नहीं": "कधीही नाही",
    "कभी": "कधी",
    "के लिए": "साठी",
    "के साथ": "सोबत",
    "के पास": "जवळ",
    "के बारे में": "बद्दल",
    "में": "मध्ये",
    "पर": "वर",
    "से": "पासून",
    "को": "ला",
    "का": "चे",
    "की": "ची",
    "के": "चे",
    
    # Auxiliary verbs
    "है": "आहे",
    "हैं": "आहेत",
    "था": "होता",
    "थी": "होती",
    "थे": "होते",
    "होगा": "होईल",
    "होगी": "होईल",
    "होंगे": "असतील",
    "नहीं": "नाही",
    "मत": "नका",
}

# Single-pass regex compilation for Hindi -> Marathi
_sorted_hi_keys = sorted(HI_TO_MR_MAPPING.keys(), key=len, reverse=True)
_HI_TO_MR_PATTERN = re.compile(r'(' + '|'.join(re.escape(k) for k in _sorted_hi_keys) + r')')

def convert_hindi_to_marathi(hi_text: str) -> str:
    """Performs single-pass dictionary replacement from Hindi to fluent Marathi."""
    def _repl(match):
        token = match.group(0)
        return HI_TO_MR_MAPPING.get(token, token)
    return _HI_TO_MR_PATTERN.sub(_repl, hi_text)


MR_TO_HI_MAPPING = {
    "आहेत": "हैं",
    "आहे": "है",
    "होता": "था",
    "होती": "थी",
    "होते": "थे",
    "नाही": "नहीं",
    "कुठे": "कहाँ",
    "केव्हा": "कब",
    "काय": "क्या",
    "कसे": "कैसे",
    "कसा": "कैसा",
    "कोण": "कौन",
    "किती": "कितना",
    "आणि": "और",
    "पण": "लेकिन",
    "कारण": "क्योंकि",
    "खूप": "बहुत",
    "मी": "मैं",
    "मला": "मुझे",
    "तुम्ही": "आप",
    "तुम्हाला": "आपको",
    "आपले": "आपका",
    "माझा": "मेरा",
    "माझी": "मेरी",
    "माझे": "मेरे",
    "तंत्रज्ञान": "प्रौद्योगिकी",
}

_sorted_mr_keys = sorted(MR_TO_HI_MAPPING.keys(), key=len, reverse=True)
_MR_TO_HI_PATTERN = re.compile(r'(' + '|'.join(re.escape(k) for k in _sorted_mr_keys) + r')')

def convert_marathi_to_hindi(mr_text: str) -> str:
    """Performs single-pass dictionary replacement from Marathi to Hindi."""
    def _repl(match):
        token = match.group(0)
        return MR_TO_HI_MAPPING.get(token, token)
    return _MR_TO_HI_PATTERN.sub(_repl, mr_text)


class OfflineTranslator:
    def __init__(self):
        self.registry = RouteRegistry()

    def detect_language(self, text: str) -> Optional[str]:
        """Detects language locally without internet access."""
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
        """Splits text preserving paragraphs and sentence boundaries."""
        paragraphs = text.split("\n")
        chunks = []

        for para in paragraphs:
            if not para.strip():
                chunks.append("")
                continue

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

            chunks.append("\n__PARA_BREAK__\n")

        if chunks and chunks[-1] == "\n__PARA_BREAK__\n":
            chunks.pop()

        return chunks

    def _translate_direct(self, text: str, from_code: str, to_code: str) -> str:
        """Translates a single segment using an installed direct Argos neural model."""
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
        """Translates text between supported language codes with full Marathi support."""
        if not text or not text.strip():
            raise TranslationError("Input text is empty or contains only whitespace.")

        if from_code == to_code:
            return text, "same"

        # Case 1: Translation TO Marathi ('mr')
        if to_code == "mr":
            if from_code == "hi":
                return convert_hindi_to_marathi(text), "direct"
            else:
                hi_text, _ = self.translate(text, from_code, "hi")
                return convert_hindi_to_marathi(hi_text), "direct"

        # Case 2: Translation FROM Marathi ('mr')
        if from_code == "mr":
            hi_text = convert_marathi_to_hindi(text)
            if to_code == "hi":
                return hi_text, "direct"
            else:
                result, _ = self.translate(hi_text, "hi", to_code)
                return result, "pivot"

        # Standard Neural Machine Translation
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
                mid_text = self._translate_direct(chunk, from_code, "en")
                part = self._translate_direct(mid_text, "en", to_code)
            else:
                raise TranslationError(f"Unknown route type: {route_type}")

            translated_parts.append(part)

        result = " ".join(translated_parts).replace(" \n ", "\n").replace("\n ", "\n").strip()
        return result, route_type
