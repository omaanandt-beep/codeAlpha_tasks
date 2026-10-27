"""
TechAssist FAQ Chatbot - Core Matching Engine
Implements TF-IDF vectorization and Cosine Similarity matching over verified FAQ entries.
"""

import json
import logging
import os
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from nlp_preprocessing import TextPreprocessor, preprocess_text

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

DEFAULT_SIMILARITY_THRESHOLD = 0.25
DEFAULT_FAQ_PATH = os.path.join(os.path.dirname(__file__), "data", "faqs.json")


class FAQValidationError(Exception):
    """Raised when the FAQ dataset contains structural or semantic errors."""
    pass


class FAQChatbot:
    """Intelligent FAQ retrieval chatbot powered by TF-IDF vectorization and Cosine Similarity."""

    def __init__(
        self,
        dataset_path: str = DEFAULT_FAQ_PATH,
        similarity_threshold: float = DEFAULT_SIMILARITY_THRESHOLD,
        preprocessor: Optional[TextPreprocessor] = None,
    ):
        self.dataset_path = dataset_path
        self.similarity_threshold = float(similarity_threshold)
        self.preprocessor = preprocessor or TextPreprocessor()

        # Storage structures
        self.faqs: List[Dict[str, Any]] = []
        self.faq_by_id: Dict[str, Dict[str, Any]] = {}
        self.categories: List[str] = []

        # Vectorization indexing structures
        self.indexed_variants: List[str] = []          # Raw text of question variants
        self.preprocessed_variants: List[str] = []   # Preprocessed text of variants
        self.variant_to_faq_id: List[str] = []        # Maps variant index to parent FAQ ID

        self.vectorizer: Optional[TfidfVectorizer] = None
        self.tfidf_matrix: Optional[np.ndarray] = None

        # Load and index dataset
        self.load_dataset()

    def validate_faq_records(self, raw_data: Any) -> Tuple[List[Dict[str, Any]], List[str]]:
        """
        Validates raw dataset entries.
        Returns valid records and a list of diagnostic error messages.
        """
        if not isinstance(raw_data, list):
            raise FAQValidationError(f"FAQ dataset root must be a JSON array, got {type(raw_data).__name__}")

        if len(raw_data) == 0:
            raise FAQValidationError("FAQ dataset is empty. At least one FAQ record is required.")

        valid_records: List[Dict[str, Any]] = []
        errors: List[str] = []
        seen_ids = set()

        for idx, item in enumerate(raw_data):
            if not isinstance(item, dict):
                errors.append(f"Record at index {idx} is not a JSON object.")
                continue

            # Verify required fields
            req_fields = ["id", "category", "question", "alternatives", "answer"]
            missing = [f for f in req_fields if f not in item]
            if missing:
                errors.append(f"Record at index {idx} is missing required fields: {', '.join(missing)}")
                continue

            faq_id = str(item.get("id", "")).strip()
            category = str(item.get("category", "")).strip()
            question = str(item.get("question", "")).strip()
            answer = str(item.get("answer", "")).strip()
            alternatives = item.get("alternatives", [])

            if not faq_id:
                errors.append(f"Record at index {idx} has an empty 'id'.")
                continue

            if faq_id in seen_ids:
                errors.append(f"Duplicate FAQ ID found: '{faq_id}' at index {idx}.")
                continue

            if not category:
                errors.append(f"Record '{faq_id}' has an empty 'category'.")
                continue

            if not question:
                errors.append(f"Record '{faq_id}' has an empty canonical 'question'.")
                continue

            if not answer:
                errors.append(f"Record '{faq_id}' has an empty 'answer'.")
                continue

            if not isinstance(alternatives, list):
                errors.append(f"Record '{faq_id}' 'alternatives' must be a list of strings.")
                continue

            clean_alternatives = [str(alt).strip() for alt in alternatives if str(alt).strip()]

            clean_record = {
                "id": faq_id,
                "category": category,
                "question": question,
                "alternatives": clean_alternatives,
                "answer": answer,
            }

            seen_ids.add(faq_id)
            valid_records.append(clean_record)

        return valid_records, errors

    def load_dataset(self) -> None:
        """Loads, validates, and builds the TF-IDF index for the FAQ dataset."""
        if not os.path.exists(self.dataset_path):
            raise FileNotFoundError(f"FAQ dataset file not found at: {self.dataset_path}")

        with open(self.dataset_path, "r", encoding="utf-8") as f:
            try:
                raw_data = json.load(f)
            except json.JSONDecodeError as e:
                raise FAQValidationError(f"Invalid JSON format in {self.dataset_path}: {e}")

        valid_records, validation_errors = self.validate_faq_records(raw_data)
        if validation_errors:
            error_summary = "\n - " + "\n - ".join(validation_errors)
            logger.warning("FAQ validation diagnostics:%s", error_summary)
            if not valid_records:
                raise FAQValidationError(f"No valid records could be extracted due to errors:{error_summary}")

        self.faqs = valid_records
        self.faq_by_id = {faq["id"]: faq for faq in valid_records}
        self.categories = sorted(list({faq["category"] for faq in valid_records}))

        self._build_index()
        logger.info(
            "FAQChatbot initialized successfully with %d FAQs, %d total indexed question variants across %d categories.",
            len(self.faqs),
            len(self.indexed_variants),
            len(self.categories),
        )

    def _build_index(self) -> None:
        """Constructs the TF-IDF vector matrix over all canonical and alternative questions."""
        self.indexed_variants = []
        self.preprocessed_variants = []
        self.variant_to_faq_id = []

        for faq in self.faqs:
            faq_id = faq["id"]
            # Index canonical question
            canonical_q = faq["question"]
            prep_canonical = self.preprocessor.preprocess(canonical_q)
            self.indexed_variants.append(canonical_q)
            self.preprocessed_variants.append(prep_canonical)
            self.variant_to_faq_id.append(faq_id)

            # Index all alternative phrasings
            for alt_q in faq["alternatives"]:
                prep_alt = self.preprocessor.preprocess(alt_q)
                self.indexed_variants.append(alt_q)
                self.preprocessed_variants.append(prep_alt)
                self.variant_to_faq_id.append(faq_id)

        # Fit TF-IDF Vectorizer with unigrams and bigrams
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            token_pattern=r"(?u)\b\w+\b",
            sublinear_tf=True,
            norm="l2",
        )
        self.tfidf_matrix = self.vectorizer.fit_transform(self.preprocessed_variants)

    def match_query(self, user_query: str) -> Dict[str, Any]:
        """
        Matches incoming user query against indexed FAQ variants.
        Returns a rich response dictionary with answer, similarity score, and diagnostic metadata.
        """
        # Handle empty or non-string input
        if not user_query or not isinstance(user_query, str) or not user_query.strip():
            return {
                "matched": False,
                "is_fallback": True,
                "score": 0.0,
                "confidence": "None",
                "question": None,
                "matched_variant": None,
                "faq_id": None,
                "category": None,
                "answer": "Please enter a question so I can assist you with technical troubleshooting.",
                "fallback_message": "Please enter a valid technical question.",
                "suggested_questions": self.get_suggested_questions(count=3),
            }

        clean_query = user_query.strip()
        preprocessed_query = self.preprocessor.preprocess(clean_query)

        # Handle queries that collapse to empty tokens (e.g. pure punctuation or rare stop words)
        if not preprocessed_query.strip():
            return {
                "matched": False,
                "is_fallback": True,
                "score": 0.0,
                "confidence": "None",
                "question": None,
                "matched_variant": None,
                "faq_id": None,
                "category": None,
                "answer": (
                    "I couldn't detect any recognized technical keywords in your question. "
                    "Please try rephrasing with specific details, such as 'slow laptop', 'Wi-Fi disconnected', or 'blue screen error'."
                ),
                "fallback_message": "No recognizable keywords found in query.",
                "suggested_questions": self.get_suggested_questions(count=3),
            }

        # Vectorize incoming query
        query_vector = self.vectorizer.transform([preprocessed_query])

        # Compute cosine similarities across all variants
        raw_cosine_scores = cosine_similarity(query_vector, self.tfidf_matrix).flatten()

        # Apply intelligent false-positive guard without penalizing natural conversational sentences
        query_tokens = set(preprocessed_query.split())
        adjusted_scores = np.zeros_like(raw_cosine_scores)

        for idx, raw_score in enumerate(raw_cosine_scores):
            if raw_score <= 0.0:
                continue
            variant_tokens = set(self.preprocessed_variants[idx].split())
            overlap = len(query_tokens.intersection(variant_tokens))

            # When 2+ key technical terms match, maintain full raw cosine confidence and boost if significant
            if overlap >= 2:
                adjusted_scores[idx] = max(raw_score, 0.42) if raw_score >= 0.20 else raw_score
            elif overlap == 1 and len(query_tokens) >= 2:
                # Penalize single-word overlaps in multi-word queries (e.g. 'how to make pizza' matching 'make admin')
                adjusted_scores[idx] = raw_score * 0.40
            else:
                adjusted_scores[idx] = raw_score

        # Find best candidate variant
        best_variant_idx = int(np.argmax(adjusted_scores))
        best_score = float(adjusted_scores[best_variant_idx])

        # Collect top unique parent FAQ candidates
        top_candidates = self._rank_candidate_faqs(adjusted_scores)

        # Check threshold
        if best_score < self.similarity_threshold:
            fallback_text = (
                "I'm sorry, I couldn't find a sufficiently relevant answer in my FAQ database. "
                "Please try rephrasing your question or check the suggestions below."
            )
            return {
                "matched": False,
                "is_fallback": True,
                "score": round(best_score, 4),
                "confidence": "Low",
                "question": None,
                "matched_variant": self.indexed_variants[best_variant_idx] if best_score > 0 else None,
                "faq_id": None,
                "category": None,
                "answer": fallback_text,
                "fallback_message": fallback_text,
                "suggested_questions": [cand["question"] for cand in top_candidates[:3]],
            }

        # Map to parent FAQ
        parent_faq_id = self.variant_to_faq_id[best_variant_idx]
        parent_faq = self.faq_by_id[parent_faq_id]

        confidence_level = "High" if best_score >= 0.55 else "Medium"

        return {
            "matched": True,
            "is_fallback": False,
            "score": round(best_score, 4),
            "confidence": confidence_level,
            "faq_id": parent_faq["id"],
            "category": parent_faq["category"],
            "question": parent_faq["question"],
            "matched_variant": self.indexed_variants[best_variant_idx],
            "answer": parent_faq["answer"],
            "suggested_questions": [
                cand["question"] for cand in top_candidates if cand["faq_id"] != parent_faq_id
            ][:2],
        }

    def _rank_candidate_faqs(self, cosine_scores: np.ndarray, top_n: int = 5) -> List[Dict[str, Any]]:
        """Ranks unique parent FAQs by their highest scoring variant."""
        faq_max_scores: Dict[str, Tuple[float, str]] = {}

        for idx, score in enumerate(cosine_scores):
            if score <= 0.05:
                continue
            faq_id = self.variant_to_faq_id[idx]
            variant_text = self.indexed_variants[idx]
            if faq_id not in faq_max_scores or score > faq_max_scores[faq_id][0]:
                faq_max_scores[faq_id] = (float(score), variant_text)

        ranked = sorted(faq_max_scores.items(), key=lambda x: x[1][0], reverse=True)

        results = []
        for faq_id, (score, variant) in ranked[:top_n]:
            faq = self.faq_by_id[faq_id]
            results.append({
                "faq_id": faq_id,
                "score": round(score, 4),
                "question": faq["question"],
                "category": faq["category"],
                "variant": variant,
            })
        return results

    def get_suggested_questions(self, count: int = 4) -> List[str]:
        """Returns representative questions from genuine FAQ entries for welcome cards and suggestions."""
        if not self.faqs:
            return []
        # Select evenly distributed representative questions across distinct categories
        suggestions = []
        seen_cats = set()
        for faq in self.faqs:
            if faq["category"] not in seen_cats:
                suggestions.append(faq["question"])
                seen_cats.add(faq["category"])
                if len(suggestions) >= count:
                    break

        # If more are needed, backfill
        if len(suggestions) < count:
            for faq in self.faqs:
                if faq["question"] not in suggestions:
                    suggestions.append(faq["question"])
                if len(suggestions) >= count:
                    break

        return suggestions[:count]

    def search_faqs(self, query: str = "", category: str = "All") -> List[Dict[str, Any]]:
        """Searches stored FAQs by keyword and category for the FAQ explorer view."""
        results = []
        q_norm = query.strip().lower()

        for faq in self.faqs:
            # Category filter
            if category != "All" and faq["category"] != category:
                continue

            # Query filter
            if not q_norm:
                results.append(faq)
                continue

            # Search canonical question, category, answer, and alternatives
            in_question = q_norm in faq["question"].lower()
            in_category = q_norm in faq["category"].lower()
            in_answer = q_norm in faq["answer"].lower()
            in_alts = any(q_norm in alt.lower() for alt in faq["alternatives"])

            if in_question or in_category or in_answer or in_alts:
                results.append(faq)

        return results

    def get_categories(self) -> List[str]:
        """Returns sorted list of all unique FAQ categories."""
        return list(self.categories)

    def get_total_count(self) -> int:
        """Returns the total number of FAQ records."""
        return len(self.faqs)
