"""
TechAssist FAQ Chatbot - NLP Preprocessing Module
Implements robust, meaning-preserving text preprocessing:
- Unicode normalization
- Lowercase normalization
- Negation-preserving stopword filtering
- Lemmatization with stemming fallback
- Safe handling of empty/whitespace/short inputs
"""

import re
import unicodedata
from typing import List, Set

# Attempt to load NLTK resources with graceful fallbacks
try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer, PorterStemmer
    from nltk.tokenize import word_tokenize
    
    _HAS_NLTK = True
except ImportError:
    _HAS_NLTK = False

# Negation and critical context words that MUST be preserved to maintain question intent
NEGATION_AND_KEY_WORDS: Set[str] = {
    "not", "no", "nor", "cannot", "cant", "can't", "wont", "won't",
    "dont", "don't", "isnt", "isn't", "arent", "aren't", "wasnt", "wasn't",
    "werent", "weren't", "hasnt", "hasn't", "havent", "haven't", "hadnt", "hadn't",
    "doesnt", "doesn't", "didnt", "didn't", "shouldnt", "shouldn't",
    "wouldnt", "wouldn't", "couldnt", "couldn't", "never", "without", "against"
}

# Technical terms and acronyms that should be preserved without over-stemming
TECH_KEYWORDS: Set[str] = {
    "wifi", "wi-fi", "bsod", "dns", "ip", "usb", "ram", "cpu", "gpu", "ssd", "hdd",
    "hdmi", "os", "pc", "cmd", "sfc", "dism", "vpn", "2fa", "mfa", "pin", "zip",
    "bios", "chrome", "edge", "teams", "zoom", "office", "word", "excel", "python", "pip",
    "bluetooth", "battery", "flicker", "microphone", "mic", "printer", "bitlocker"
}

# Common bilingual / colloquial technical mappings to English concepts
COLLOQUIAL_MAPPINGS = {
    r"\bgaram\b": "overheat",
    r"\bheating\b": "overheat",
    r"\baawaz\b": "sound",
    r"\bawaaz\b": "sound",
    r"\bdheere\b": "slow",
    r"\bbhool\b": "forgot",
    r"\bnahi\b": "not",
    r"\bnhi\b": "not",
    r"\bshutdown\b": "shut down",
    r"\bturnoff\b": "turn off",
    r"\bpoweroff\b": "power off",
    r"\bheats?\s+up\b": "overheat",
    r"\bgetting\s+hot\b": "overheat",
    r"\bdropping\b": "disconnect",
}


class TextPreprocessor:
    """Configurable and fault-tolerant NLP preprocessor for FAQ queries and records."""

    def __init__(self, use_lemmatizer: bool = True, preserve_negations: bool = True):
        self.use_lemmatizer = use_lemmatizer
        self.preserve_negations = preserve_negations
        
        self.lemmatizer = None
        self.stemmer = None
        self.stop_words: Set[str] = set()

        self._initialize_nlp_tools()

    def _initialize_nlp_tools(self) -> None:
        """Initializes NLTK tools with safe fallback defaults if NLTK data is unavailable."""
        if _HAS_NLTK:
            try:
                self.lemmatizer = WordNetLemmatizer()
                # Test lemmatizer to ensure data is downloaded
                self.lemmatizer.lemmatize("testing")
            except Exception:
                self.lemmatizer = None

            try:
                self.stemmer = PorterStemmer()
            except Exception:
                self.stemmer = None

            try:
                base_stops = set(stopwords.words("english"))
            except Exception:
                # Built-in fallback common stop words
                base_stops = {
                    "a", "an", "the", "and", "or", "in", "on", "at", "to", "for",
                    "of", "with", "by", "from", "is", "are", "was", "were", "be",
                    "been", "being", "have", "has", "had", "do", "does", "did",
                    "i", "you", "he", "she", "it", "we", "they", "my", "your",
                    "his", "her", "their", "this", "that", "these", "those"
                }
        else:
            base_stops = {
                "a", "an", "the", "and", "or", "in", "on", "at", "to", "for",
                "of", "with", "by", "from", "is", "are", "was", "were", "be",
                "been", "being", "have", "has", "had", "do", "does", "did",
                "i", "you", "he", "she", "it", "we", "they", "my", "your",
                "his", "her", "their", "this", "that", "these", "those"
            }

        if self.preserve_negations:
            # Crucial: Keep negations like 'not', 'cannot' so 'not charging' != 'charging'
            self.stop_words = base_stops - NEGATION_AND_KEY_WORDS
        else:
            self.stop_words = base_stops

    def normalize_text(self, text: str) -> str:
        """Applies Unicode normalization, lowercasing, and whitespace cleanup."""
        if not text or not isinstance(text, str):
            return ""

        # Unicode NFKD normalization
        text = unicodedata.normalize("NFKD", text)
        
        # Lowercase
        text = text.lower()

        # Normalize contractions and common colloquialisms
        text = re.sub(r"won['’]t", "will not", text)
        text = re.sub(r"can['’]t", "cannot", text)
        text = re.sub(r"n['’]t", " not", text)
        text = re.sub(r"['’]re", " are", text)
        text = re.sub(r"['’]s", " is", text)
        text = re.sub(r"['’]d", " would", text)
        text = re.sub(r"['’]ll", " will", text)
        text = re.sub(r"['’]ve", " have", text)
        text = re.sub(r"['’]m", " am", text)

        # Normalize hyphens in wi-fi
        text = re.sub(r"\bwi\s*-\s*fi\b", "wifi", text)

        # Apply colloquial and bilingual technical mappings
        for pattern, replacement in COLLOQUIAL_MAPPINGS.items():
            text = re.sub(pattern, replacement, text)

        # Replace non-alphanumeric punctuation with spaces, keeping essential alphanumerics
        text = re.sub(r"[^\w\s]", " ", text)

        # Normalize whitespace (multiple spaces, tabs, newlines to single space)
        text = re.sub(r"\s+", " ", text).strip()

        return text

    def tokenize(self, text: str) -> List[str]:
        """Tokenizes pre-normalized text using NLTK word_tokenize or regex fallback."""
        if not text:
            return []

        if _HAS_NLTK:
            try:
                return word_tokenize(text)
            except Exception:
                pass

        # Robust regex tokenization fallback
        return re.findall(r"\b\w+\b", text)

    def filter_and_stem(self, tokens: List[str]) -> List[str]:
        """Filters stopwords while protecting negations and applies lemmatization or stemming."""
        processed = []
        for token in tokens:
            if not token:
                continue

            # Remove single letters except 'a' or 'i' (which are already in stopwords)
            if len(token) <= 1 and token not in {"c"}:  # allow C drive
                continue

            # Filter out non-negation stop words
            if token in self.stop_words and token not in NEGATION_AND_KEY_WORDS:
                continue

            # Lemmatize or stem, unless it is a recognized tech keyword or negation
            if token in TECH_KEYWORDS or token in NEGATION_AND_KEY_WORDS:
                processed.append(token)
                continue

            term = token
            if self.use_lemmatizer and self.lemmatizer:
                try:
                    # Lemmatize noun first, then verb
                    term = self.lemmatizer.lemmatize(term, pos="n")
                    term = self.lemmatizer.lemmatize(term, pos="v")
                except Exception:
                    if self.stemmer:
                        term = self.stemmer.stem(term)
            elif self.stemmer:
                try:
                    term = self.stemmer.stem(term)
                except Exception:
                    pass

            processed.append(term)

        return processed

    def preprocess(self, text: str) -> str:
        """Full pipeline returning a preprocessed clean string ready for TF-IDF vectorization."""
        normalized = self.normalize_text(text)
        if not normalized:
            return ""

        tokens = self.tokenize(normalized)
        cleaned_tokens = self.filter_and_stem(tokens)
        return " ".join(cleaned_tokens)


# Shared default singleton preprocessor instance
_default_preprocessor = TextPreprocessor()


def preprocess_text(text: str) -> str:
    """Convenience function using the default shared preprocessor."""
    return _default_preprocessor.preprocess(text)

