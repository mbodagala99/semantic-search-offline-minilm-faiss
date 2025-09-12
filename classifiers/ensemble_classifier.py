"""
Ensemble Healthcare Classifier

Combines BART and keyword classifiers for improved healthcare classification.
Uses voting mechanism and confidence weighting for optimal results.
"""

import time
from typing import Dict, Any, List
from .base_classifier import BaseHealthcareClassifier, ClassificationResult
from .bart_zero_shot_classifier import BARTZeroShotClassifier
from .keyword_classifier import KeywordClassifier


class EnsembleClassifier(BaseHealthcareClassifier):
    """Ensemble classifier combining BART and keyword approaches"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        
        # Initialize individual classifiers
        self.bart_classifier = None
        self.keyword_classifier = None
        
        # Ensemble configuration
        self.voting_strategy = config.get('voting_strategy', 'weighted')  # 'majority', 'weighted', 'confidence'
        self.bart_weight = config.get('bart_weight', 0.6)
        self.keyword_weight = config.get('keyword_weight', 0.4)
        self.min_confidence_threshold = config.get('min_confidence_threshold', 0.3)
        
        # Performance tracking
        self.bart_available = False
        self.keyword_available = False
        
        self._initialize_classifiers()
    
    def _initialize_classifiers(self):
        """Initialize both BART and keyword classifiers"""
        try:
            # Initialize BART classifier
            bart_config = {
                'model_name': self.config.get('bart_model', 'facebook/bart-large-mnli'),
                'confidence_threshold': self.confidence_threshold,
                'device': self.config.get('device', -1)
            }
            self.bart_classifier = BARTZeroShotClassifier(bart_config)
            self.bart_available = self.bart_classifier.is_available()
            
            # Initialize keyword classifier
            keyword_config = {
                'confidence_threshold': self.confidence_threshold
            }
            self.keyword_classifier = KeywordClassifier(keyword_config)
            self.keyword_available = self.keyword_classifier.is_available()
            
            print(f"Ensemble Classifier initialized:")
            print(f"  BART Available: {self.bart_available}")
            print(f"  Keyword Available: {self.keyword_available}")
            
        except Exception as e:
            print(f"Error initializing ensemble classifiers: {e}")
    
    def classify(self, query: str) -> ClassificationResult:
        """Classify query using ensemble of BART and keyword classifiers"""
        start_time = time.time()
        
        if not self.is_available():
            return ClassificationResult(
                is_healthcare=False,
                confidence=0.0,
                model_name=self.model_name,
                processing_time_ms=0.0,
                raw_response={"error": "No classifiers available"}
            )
        
        try:
            # Get predictions from both classifiers
            bart_result = None
            keyword_result = None
            
            if self.bart_available:
                bart_result = self.bart_classifier.classify(query)
            
            if self.keyword_available:
                keyword_result = self.keyword_classifier.classify(query)
            
            # Combine results based on voting strategy
            ensemble_result = self._combine_results(bart_result, keyword_result, query)
            
            processing_time = (time.time() - start_time) * 1000
            ensemble_result.processing_time_ms = processing_time
            
            return ensemble_result
            
        except Exception as e:
            processing_time = (time.time() - start_time) * 1000
            return ClassificationResult(
                is_healthcare=False,
                confidence=0.0,
                model_name=self.model_name,
                processing_time_ms=processing_time,
                raw_response={"error": str(e)}
            )
    
    def _combine_results(self, bart_result: ClassificationResult, keyword_result: ClassificationResult, query: str) -> ClassificationResult:
        """Combine results from both classifiers using ensemble strategy"""
        
        # If only one classifier is available, use its result
        if bart_result is None and keyword_result is None:
            return ClassificationResult(
                is_healthcare=False,
                confidence=0.0,
                model_name=self.model_name,
                processing_time_ms=0.0,
                raw_response={"error": "No classifier results available"}
            )
        
        if bart_result is None:
            return keyword_result
        
        if keyword_result is None:
            return bart_result
        
        # Both classifiers available - use ensemble strategy
        if self.voting_strategy == 'majority':
            return self._majority_voting(bart_result, keyword_result)
        elif self.voting_strategy == 'weighted':
            return self._weighted_voting(bart_result, keyword_result)
        elif self.voting_strategy == 'confidence':
            return self._confidence_based_voting(bart_result, keyword_result)
        else:
            # Default to weighted voting
            return self._weighted_voting(bart_result, keyword_result)
    
    def _majority_voting(self, bart_result: ClassificationResult, keyword_result: ClassificationResult) -> ClassificationResult:
        """Simple majority voting between classifiers"""
        bart_vote = 1 if bart_result.is_healthcare else 0
        keyword_vote = 1 if keyword_result.is_healthcare else 0
        
        # Majority vote
        is_healthcare = (bart_vote + keyword_vote) >= 1
        
        # Average confidence
        avg_confidence = (bart_result.confidence + keyword_result.confidence) / 2
        
        return ClassificationResult(
            is_healthcare=is_healthcare,
            confidence=avg_confidence,
            model_name=f"ensemble_{self.model_name}",
            processing_time_ms=0.0,  # Will be set by caller
            raw_response={
                "method": "majority_voting",
                "bart_result": {
                    "is_healthcare": bart_result.is_healthcare,
                    "confidence": bart_result.confidence
                },
                "keyword_result": {
                    "is_healthcare": keyword_result.is_healthcare,
                    "confidence": keyword_result.confidence
                }
            }
        )
    
    def _weighted_voting(self, bart_result: ClassificationResult, keyword_result: ClassificationResult) -> ClassificationResult:
        """Weighted voting based on configured weights"""
        # Calculate weighted scores
        bart_score = bart_result.confidence * self.bart_weight if bart_result.is_healthcare else (1 - bart_result.confidence) * self.bart_weight
        keyword_score = keyword_result.confidence * self.keyword_weight if keyword_result.is_healthcare else (1 - keyword_result.confidence) * self.keyword_weight
        
        # Determine classification
        is_healthcare = bart_score + keyword_score > 0.5
        
        # Calculate ensemble confidence
        if is_healthcare:
            ensemble_confidence = bart_score + keyword_score
        else:
            ensemble_confidence = 1 - (bart_score + keyword_score)
        
        return ClassificationResult(
            is_healthcare=is_healthcare,
            confidence=ensemble_confidence,
            model_name=f"ensemble_{self.model_name}",
            processing_time_ms=0.0,  # Will be set by caller
            raw_response={
                "method": "weighted_voting",
                "bart_weight": self.bart_weight,
                "keyword_weight": self.keyword_weight,
                "bart_score": bart_score,
                "keyword_score": keyword_score,
                "bart_result": {
                    "is_healthcare": bart_result.is_healthcare,
                    "confidence": bart_result.confidence
                },
                "keyword_result": {
                    "is_healthcare": keyword_result.is_healthcare,
                    "confidence": keyword_result.confidence
                }
            }
        )
    
    def _confidence_based_voting(self, bart_result: ClassificationResult, keyword_result: ClassificationResult) -> ClassificationResult:
        """Use the classifier with higher confidence"""
        if bart_result.confidence > keyword_result.confidence:
            return ClassificationResult(
                is_healthcare=bart_result.is_healthcare,
                confidence=bart_result.confidence,
                model_name=f"ensemble_{self.model_name}",
                processing_time_ms=0.0,  # Will be set by caller
                raw_response={
                    "method": "confidence_based",
                    "selected_classifier": "bart",
                    "bart_result": {
                        "is_healthcare": bart_result.is_healthcare,
                        "confidence": bart_result.confidence
                    },
                    "keyword_result": {
                        "is_healthcare": keyword_result.is_healthcare,
                        "confidence": keyword_result.confidence
                    }
                }
            )
        else:
            return ClassificationResult(
                is_healthcare=keyword_result.is_healthcare,
                confidence=keyword_result.confidence,
                model_name=f"ensemble_{self.model_name}",
                processing_time_ms=0.0,  # Will be set by caller
                raw_response={
                    "method": "confidence_based",
                    "selected_classifier": "keyword",
                    "bart_result": {
                        "is_healthcare": bart_result.is_healthcare,
                        "confidence": bart_result.confidence
                    },
                    "keyword_result": {
                        "is_healthcare": keyword_result.is_healthcare,
                        "confidence": keyword_result.confidence
                    }
                }
            )
    
    def is_available(self) -> bool:
        """Check if at least one classifier is available"""
        return self.bart_available or self.keyword_available
    
    def get_ensemble_info(self) -> Dict[str, Any]:
        """Get information about the ensemble configuration"""
        return {
            "type": "Ensemble Classifier",
            "voting_strategy": self.voting_strategy,
            "bart_weight": self.bart_weight,
            "keyword_weight": self.keyword_weight,
            "bart_available": self.bart_available,
            "keyword_available": self.keyword_available,
            "min_confidence_threshold": self.min_confidence_threshold
        }
