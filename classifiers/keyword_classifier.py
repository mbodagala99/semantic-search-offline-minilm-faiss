"""
Enhanced Keyword-Based Healthcare Classifier

Advanced keyword-based classification using ratio-based analysis and external keyword sources.
"""

import time
import json
import os
from typing import Dict, Any, List, Set
from .base_classifier import BaseHealthcareClassifier, ClassificationResult


class KeywordClassifier(BaseHealthcareClassifier):
    """Enhanced keyword-based healthcare classifier with ratio-based analysis"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        
        # Load external keyword lists
        self.healthcare_keywords = self._load_healthcare_keywords()
        self.non_healthcare_keywords = self._load_non_healthcare_keywords()
        
        # Enhanced classification parameters
        self.ratio_threshold = config.get('ratio_threshold', 0.1)  # Minimum ratio difference
        self.min_confidence = config.get('min_confidence', 0.3)    # Minimum confidence for classification
        self.use_ratio_based = config.get('use_ratio_based', True) # Enable ratio-based classification
        self.fallback_to_count = config.get('fallback_to_count', True)  # Fallback to count-based if ratio fails
        
        print(f"Enhanced Keyword Classifier initialized:")
        print(f"  Healthcare keywords: {len(self.healthcare_keywords)}")
        print(f"  Non-healthcare keywords: {len(self.non_healthcare_keywords)}")
        print(f"  Ratio-based classification: {self.use_ratio_based}")
    
    def _load_healthcare_keywords(self) -> Set[str]:
        """Load healthcare keywords from external source"""
        try:
            # Try to load from external file first
            keywords_file = 'data/keywords/healthcare_keywords.json'
            if os.path.exists(keywords_file):
                with open(keywords_file, 'r') as f:
                    data = json.load(f)
                    keywords = set(data['keywords'])
                    print(f"✅ Loaded {len(keywords)} healthcare keywords from external source")
                    return keywords
        except Exception as e:
            print(f"⚠️  Could not load external healthcare keywords: {e}")
        
        # Fallback to built-in keywords from file
        try:
            builtin_file = 'data/keywords/builtin_healthcare_keywords.json'
            if os.path.exists(builtin_file):
                with open(builtin_file, 'r') as f:
                    data = json.load(f)
                    keywords = set(data['keywords'])
                    print(f"✅ Loaded {len(keywords)} built-in healthcare keywords from file")
                    return keywords
        except Exception as e:
            print(f"⚠️  Could not load built-in healthcare keywords file: {e}")
        
        # Final fallback - minimal set
        minimal_keywords = {
            'healthcare', 'medical', 'patient', 'doctor', 'hospital', 'clinic',
            'insurance', 'claim', 'provider', 'member', 'procedure', 'treatment'
        }
        print(f"⚠️  Using {len(minimal_keywords)} minimal healthcare keywords")
        return minimal_keywords
    
    def _load_non_healthcare_keywords(self) -> Set[str]:
        """Load non-healthcare keywords from external source"""
        try:
            # Try to load from external file first
            keywords_file = 'data/keywords/non_healthcare_keywords.json'
            if os.path.exists(keywords_file):
                with open(keywords_file, 'r') as f:
                    data = json.load(f)
                    keywords = set(data['keywords'])
                    print(f"✅ Loaded {len(keywords)} non-healthcare keywords from external source")
                    return keywords
        except Exception as e:
            print(f"⚠️  Could not load external non-healthcare keywords: {e}")
        
        # Fallback to built-in keywords from file
        try:
            builtin_file = 'data/keywords/builtin_non_healthcare_keywords.json'
            if os.path.exists(builtin_file):
                with open(builtin_file, 'r') as f:
                    data = json.load(f)
                    keywords = set(data['keywords'])
                    print(f"✅ Loaded {len(keywords)} built-in non-healthcare keywords from file")
                    return keywords
        except Exception as e:
            print(f"⚠️  Could not load built-in non-healthcare keywords file: {e}")
        
        # Final fallback - minimal set
        minimal_keywords = {
            'food', 'cooking', 'weather', 'car', 'movie', 'music', 'sports',
            'travel', 'phone', 'computer', 'shopping', 'restaurant'
        }
        print(f"⚠️  Using {len(minimal_keywords)} minimal non-healthcare keywords")
        return minimal_keywords
    
    def classify(self, query: str) -> ClassificationResult:
        """Classify query using enhanced keyword matching with ratio-based analysis"""
        start_time = time.time()
        
        query_lower = query.lower()
        
        # Extract words from query (simple tokenization)
        words = self._extract_words(query_lower)
        total_words = len(words)
        
        # Count healthcare and non-healthcare keywords
        healthcare_count = sum(1 for keyword in self.healthcare_keywords if keyword in query_lower)
        non_healthcare_count = sum(1 for keyword in self.non_healthcare_keywords if keyword in query_lower)
        
        processing_time = (time.time() - start_time) * 1000
        
        # Use ratio-based classification if enabled
        if self.use_ratio_based and total_words > 0:
            result = self._ratio_based_classification(
                healthcare_count, non_healthcare_count, total_words, query_lower
            )
        else:
            result = self._count_based_classification(
                healthcare_count, non_healthcare_count, query_lower
            )
        
        result.processing_time_ms = processing_time
        return result
    
    def _extract_words(self, text: str) -> List[str]:
        """Extract words from text (simple tokenization)"""
        import re
        # Remove punctuation and split into words
        words = re.findall(r'\b\w+\b', text.lower())
        return words
    
    def _ratio_based_classification(self, healthcare_count: int, non_healthcare_count: int, 
                                  total_words: int, query_lower: str) -> ClassificationResult:
        """Enhanced ratio-based classification"""
        
        # Calculate ratios
        healthcare_ratio = healthcare_count / total_words if total_words > 0 else 0
        non_healthcare_ratio = non_healthcare_count / total_words if total_words > 0 else 0
        
        # Calculate ratio difference
        ratio_difference = abs(healthcare_ratio - non_healthcare_ratio)
        
        # Determine classification based on ratios
        if healthcare_ratio > non_healthcare_ratio:
            is_healthcare = True
            confidence = self._calculate_confidence(healthcare_ratio, non_healthcare_ratio, ratio_difference)
        elif non_healthcare_ratio > healthcare_ratio:
            is_healthcare = False
            confidence = self._calculate_confidence(non_healthcare_ratio, healthcare_ratio, ratio_difference)
        else:
            # Tie in ratios - use fallback strategy
            if self.fallback_to_count:
                return self._count_based_classification(healthcare_count, non_healthcare_count, query_lower)
            else:
                # Default to healthcare for ambiguous cases
                is_healthcare = True
                confidence = self.min_confidence
        
        # Check if confidence meets minimum threshold
        if confidence < self.min_confidence:
            # Low confidence - use fallback if enabled
            if self.fallback_to_count:
                return self._count_based_classification(healthcare_count, non_healthcare_count, query_lower)
        
        return ClassificationResult(
            is_healthcare=is_healthcare,
            confidence=confidence,
            model_name=self.model_name,
            processing_time_ms=0.0,  # Will be set by caller
            raw_response={
                "method": "ratio_based_classification",
                "healthcare_count": healthcare_count,
                "non_healthcare_count": non_healthcare_count,
                "total_words": total_words,
                "healthcare_ratio": healthcare_ratio,
                "non_healthcare_ratio": non_healthcare_ratio,
                "ratio_difference": ratio_difference,
                "confidence_calculation": "ratio_based"
            }
        )
    
    def _count_based_classification(self, healthcare_count: int, non_healthcare_count: int, 
                                  query_lower: str) -> ClassificationResult:
        """Traditional count-based classification (fallback)"""
        
        # Determine classification
        if healthcare_count > non_healthcare_count:
            is_healthcare = True
            confidence = min(0.9, 0.5 + (healthcare_count * 0.1))
        elif non_healthcare_count > healthcare_count:
            is_healthcare = False
            confidence = min(0.9, 0.5 + (non_healthcare_count * 0.1))
        else:
            # Tie or no keywords - default to healthcare for ambiguous cases
            is_healthcare = True
            confidence = self.min_confidence
        
        return ClassificationResult(
            is_healthcare=is_healthcare,
            confidence=confidence,
            model_name=self.model_name,
            processing_time_ms=0.0,  # Will be set by caller
            raw_response={
                "method": "count_based_classification",
                "healthcare_count": healthcare_count,
                "non_healthcare_count": non_healthcare_count,
                "confidence_calculation": "count_based"
            }
        )
    
    def _calculate_confidence(self, primary_ratio: float, secondary_ratio: float, 
                            ratio_difference: float) -> float:
        """Calculate confidence based on ratio analysis"""
        
        # Base confidence from primary ratio
        base_confidence = min(0.9, 0.3 + (primary_ratio * 2.0))
        
        # Boost confidence based on ratio difference
        if ratio_difference > self.ratio_threshold:
            confidence_boost = min(0.2, ratio_difference * 2.0)
            base_confidence += confidence_boost
        
        # Penalty for low primary ratio
        if primary_ratio < 0.1:
            base_confidence *= 0.8
        
        # Ensure confidence is within bounds
        return max(self.min_confidence, min(0.95, base_confidence))
    
    def is_available(self) -> bool:
        """Keyword classifier is always available"""
        return True
