"""
Classifier Factory

Factory pattern for creating healthcare classifiers.
Enables easy switching between different classifier implementations.
"""

from typing import Dict, Any, Type
from .base_classifier import BaseHealthcareClassifier
from .bart_zero_shot_classifier import BARTZeroShotClassifier
from .keyword_classifier import KeywordClassifier
from .ensemble_classifier import EnsembleClassifier


class ClassifierFactory:
    """Factory for creating healthcare classifiers"""
    
    _classifiers = {
        'bart_zero_shot': BARTZeroShotClassifier,
        'keyword': KeywordClassifier,
        'ensemble': EnsembleClassifier,
        # Add more classifiers here as needed
    }
    
    @classmethod
    def create_classifier(cls, classifier_type: str, config: Dict[str, Any]) -> BaseHealthcareClassifier:
        """Create a classifier instance based on type"""
        if classifier_type not in cls._classifiers:
            raise ValueError(f"Unknown classifier type: {classifier_type}")
        
        classifier_class = cls._classifiers[classifier_type]
        return classifier_class(config)
    
    @classmethod
    def get_available_classifiers(cls) -> list:
        """Get list of available classifier types"""
        return list(cls._classifiers.keys())
    
    @classmethod
    def register_classifier(cls, name: str, classifier_class: Type[BaseHealthcareClassifier]):
        """Register a new classifier type"""
        cls._classifiers[name] = classifier_class
