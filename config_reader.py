#!/usr/bin/env python3
"""
Configuration Reader for Healthcare Semantic Search System
Reads configuration from .config file and provides easy access to settings
"""

import configparser
import os
from typing import List, Dict, Any, Union

class HealthcareSearchConfig:
    """Configuration reader for healthcare search system"""
    
    def __init__(self, config_file: str = "healthcare_search.config"):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.load_config()
    
    def load_config(self):
        """Load configuration from file"""
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"Configuration file {self.config_file} not found")
        
        self.config.read(self.config_file)
        print(f"✅ Configuration loaded from {self.config_file}")
    
    def reload_config(self):
        """Reload configuration from file"""
        self.load_config()
        print("🔄 Configuration reloaded")
    
    # Embedding Model Configuration
    def get_primary_model(self) -> str:
        """Get primary embedding model"""
        return self.config.get('EMBEDDING_MODEL', 'primary_model', fallback='dmis-lab/biobert-base-cased-v1.1')
    
    def get_alternative_models(self) -> List[str]:
        """Get alternative models for testing"""
        models_str = self.config.get('EMBEDDING_MODEL', 'alternative_models', fallback='bert-base-uncased,all-MiniLM-L6-v2')
        return [model.strip() for model in models_str.split(',')]
    
    def get_model_dimensions(self) -> int:
        """Get model dimensions"""
        return self.config.getint('EMBEDDING_MODEL', 'model_dimensions', fallback=768)
    
    def is_caching_enabled(self) -> bool:
        """Check if model caching is enabled"""
        return self.config.getboolean('EMBEDDING_MODEL', 'enable_caching', fallback=True)
    
    def get_cache_directory(self) -> str:
        """Get cache directory path"""
        return self.config.get('EMBEDDING_MODEL', 'cache_directory', fallback='embeddings_cache')
    
    # Confidence Threshold Configuration
    def get_minimum_threshold(self) -> float:
        """Get minimum confidence threshold"""
        return self.config.getfloat('CONFIDENCE_THRESHOLDS', 'minimum_threshold', fallback=0.8)
    
    def get_default_threshold(self) -> float:
        """Get default confidence threshold"""
        return self.config.getfloat('CONFIDENCE_THRESHOLDS', 'default_threshold', fallback=0.6)
    
    def get_test_thresholds(self) -> List[float]:
        """Get thresholds for testing"""
        thresholds_str = self.config.get('CONFIDENCE_THRESHOLDS', 'test_thresholds', fallback='0.6,0.7,0.8,0.9,1.0')
        return [float(t.strip()) for t in thresholds_str.split(',')]
    
    def is_adaptive_threshold_enabled(self) -> bool:
        """Check if adaptive thresholds are enabled"""
        return self.config.getboolean('CONFIDENCE_THRESHOLDS', 'adaptive_thresholds', fallback=True)
    
    def get_healthcare_domain_threshold(self) -> float:
        """Get healthcare domain-specific threshold"""
        return self.config.getfloat('CONFIDENCE_THRESHOLDS', 'healthcare_domain_threshold', fallback=0.75)
    
    def get_non_healthcare_threshold(self) -> float:
        """Get non-healthcare rejection threshold"""
        return self.config.getfloat('CONFIDENCE_THRESHOLDS', 'non_healthcare_threshold', fallback=0.3)
    
    # Search Optimization Configuration
    def is_vector_normalization_enabled(self) -> bool:
        """Check if vector normalization is enabled"""
        return self.config.getboolean('SEARCH_OPTIMIZATION', 'normalize_vectors', fallback=True)
    
    def is_text_preprocessing_enabled(self) -> bool:
        """Check if text preprocessing is enabled"""
        return self.config.getboolean('SEARCH_OPTIMIZATION', 'preprocess_text', fallback=True)
    
    def is_query_expansion_enabled(self) -> bool:
        """Check if query expansion is enabled"""
        return self.config.getboolean('SEARCH_OPTIMIZATION', 'query_expansion', fallback=True)
    
    def get_max_results(self) -> int:
        """Get maximum search results"""
        return self.config.getint('SEARCH_OPTIMIZATION', 'max_results', fallback=10)
    
    def is_similarity_cache_enabled(self) -> bool:
        """Check if similarity caching is enabled"""
        return self.config.getboolean('SEARCH_OPTIMIZATION', 'enable_similarity_cache', fallback=True)
    
    def is_domain_filtering_enabled(self) -> bool:
        """Check if domain filtering is enabled"""
        return self.config.getboolean('SEARCH_OPTIMIZATION', 'enable_domain_filtering', fallback=True)
    
    def is_healthcare_keywords_enabled(self) -> bool:
        """Check if healthcare keyword detection is enabled"""
        return self.config.getboolean('SEARCH_OPTIMIZATION', 'enable_healthcare_keywords', fallback=True)
    
    def is_non_healthcare_rejection_enabled(self) -> bool:
        """Check if non-healthcare rejection is enabled"""
        return self.config.getboolean('SEARCH_OPTIMIZATION', 'enable_non_healthcare_rejection', fallback=True)
    
    # Index Configuration
    def get_index_type(self) -> str:
        """Get FAISS index type"""
        return self.config.get('INDEX_CONFIGURATION', 'index_type', fallback='IndexFlatIP')
    
    def get_index_directory(self) -> str:
        """Get index directory"""
        return self.config.get('INDEX_CONFIGURATION', 'index_directory', fallback='indexes')
    
    def is_incremental_updates_enabled(self) -> bool:
        """Check if incremental updates are enabled"""
        return self.config.getboolean('INDEX_CONFIGURATION', 'incremental_updates', fallback=True)
    
    def get_batch_size(self) -> int:
        """Get batch size for updates"""
        return self.config.getint('INDEX_CONFIGURATION', 'batch_size', fallback=100)
    
    # Performance Configuration
    def is_parallel_processing_enabled(self) -> bool:
        """Check if parallel processing is enabled"""
        return self.config.getboolean('PERFORMANCE', 'parallel_processing', fallback=True)
    
    def get_worker_threads(self) -> int:
        """Get number of worker threads"""
        return self.config.getint('PERFORMANCE', 'worker_threads', fallback=4)
    
    def is_memory_optimization_enabled(self) -> bool:
        """Check if memory optimization is enabled"""
        return self.config.getboolean('PERFORMANCE', 'memory_optimization', fallback=True)
    
    def get_cache_size_limit(self) -> int:
        """Get cache size limit in MB"""
        return self.config.getint('PERFORMANCE', 'cache_size_limit', fallback=1000)
    
    # Logging Configuration
    def get_log_level(self) -> str:
        """Get log level"""
        return self.config.get('LOGGING', 'log_level', fallback='INFO')
    
    def is_performance_logging_enabled(self) -> bool:
        """Check if performance logging is enabled"""
        return self.config.getboolean('LOGGING', 'performance_logging', fallback=True)
    
    def get_log_file(self) -> str:
        """Get log file path"""
        return self.config.get('LOGGING', 'log_file', fallback='healthcare_search.log')
    
    def get_all_config(self) -> Dict[str, Any]:
        """Get all configuration as dictionary"""
        return {
            'primary_model': self.get_primary_model(),
            'alternative_models': self.get_alternative_models(),
            'minimum_threshold': self.get_minimum_threshold(),
            'default_threshold': self.get_default_threshold(),
            'test_thresholds': self.get_test_thresholds(),
            'index_type': self.get_index_type(),
            'cache_directory': self.get_cache_directory(),
            'normalize_vectors': self.is_vector_normalization_enabled(),
            'preprocess_text': self.is_text_preprocessing_enabled(),
            'max_results': self.get_max_results()
        }
    
    def print_config_summary(self):
        """Print configuration summary"""
        print("\n" + "="*60)
        print("HEALTHCARE SEARCH CONFIGURATION SUMMARY")
        print("="*60)
        print(f"Primary Model: {self.get_primary_model()}")
        print(f"Alternative Models: {', '.join(self.get_alternative_models())}")
        print(f"Minimum Threshold: {self.get_minimum_threshold()}")
        print(f"Default Threshold: {self.get_default_threshold()}")
        print(f"Test Thresholds: {self.get_test_thresholds()}")
        print(f"Index Type: {self.get_index_type()}")
        print(f"Cache Directory: {self.get_cache_directory()}")
        print(f"Vector Normalization: {self.is_vector_normalization_enabled()}")
        print(f"Text Preprocessing: {self.is_text_preprocessing_enabled()}")
        print(f"Max Results: {self.get_max_results()}")
        print("="*60)

# Global configuration instance
config = HealthcareSearchConfig()
