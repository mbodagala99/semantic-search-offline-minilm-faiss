"""
BART Zero-Shot Healthcare Classifier

Local BART-based zero-shot classification for healthcare queries.
"""

import time
from typing import Dict, Any
from transformers import pipeline
from .base_classifier import BaseHealthcareClassifier, ClassificationResult


class BARTZeroShotClassifier(BaseHealthcareClassifier):
    """Local BART-based zero-shot healthcare classifier"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load the BART model for zero-shot classification"""
        try:
            model_name = self.config.get('model_name', 'facebook/bart-large-mnli')
            self.model = pipeline(
                "zero-shot-classification",
                model=model_name,
                device=self.config.get('device', -1)  # -1 for CPU
            )
        except Exception as e:
            print(f"Error loading BART model: {e}")
            self.model = None
    
    def classify(self, query: str) -> ClassificationResult:
        """Classify query using BART zero-shot classification"""
        start_time = time.time()
        
        if not self.is_available():
            return ClassificationResult(
                is_healthcare=False,
                confidence=0.0,
                model_name=self.model_name,
                processing_time_ms=0.0,
                raw_response={"error": "Model not available"}
            )
        
        try:
            # Zero-shot classification with BART
            result = self.model(
                query,
                ["Healthcare and Medical", "Non-Healthcare"],
                hypothesis_template="This query is about {} topics."
            )
            
            processing_time = (time.time() - start_time) * 1000
            
            # Determine if healthcare
            is_healthcare = result['labels'][0] == 'Healthcare and Medical'
            confidence = result['scores'][0]
            
            return ClassificationResult(
                is_healthcare=is_healthcare,
                confidence=confidence,
                model_name=self.model_name,
                processing_time_ms=processing_time,
                raw_response=result
            )
            
        except Exception as e:
            processing_time = (time.time() - start_time) * 1000
            return ClassificationResult(
                is_healthcare=False,
                confidence=0.0,
                model_name=self.model_name,
                processing_time_ms=processing_time,
                raw_response={"error": str(e)}
            )
    
    def is_available(self) -> bool:
        """Check if BART model is loaded and ready"""
        return self.model is not None
