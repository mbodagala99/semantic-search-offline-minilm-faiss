#!/usr/bin/env python3
"""
Core Initialization Module for Healthcare Search APIs
Handles one-time initialization of all core components at service startup
"""

import os
import sys
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from datetime import datetime

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from embedding_generator import EmbeddingGenerator
    from healthcare_query_processor import HealthcareQueryProcessor
    from dsl_query_generator import DSLQueryGenerator
    from opensearch_query_executor import QueryExecutorFactory
    from config_reader import config
except ImportError as e:
    logging.error(f"Failed to import core modules: {e}")
    raise

logger = logging.getLogger(__name__)


class HealthcareSearchComponents:
    """
    Container for all initialized healthcare search components.
    This class holds references to all core components after initialization.
    """
    
    def __init__(self):
        self.embedding_generator: Optional[EmbeddingGenerator] = None
        self.query_processor: Optional[HealthcareQueryProcessor] = None
        self.dsl_generator: Optional[DSLQueryGenerator] = None
        self.query_executor_factory: Optional[QueryExecutorFactory] = None
        self.config: Optional[Any] = None
        self.initialization_time: Optional[datetime] = None
        self.is_initialized: bool = False
        self.initialization_errors: list = []

    def get_status(self) -> Dict[str, Any]:
        """Get initialization status and component health"""
        return {
            "is_initialized": self.is_initialized,
            "initialization_time": self.initialization_time.isoformat() if self.initialization_time else None,
            "components": {
                "embedding_generator": self.embedding_generator is not None,
                "query_processor": self.query_processor is not None,
                "dsl_generator": self.dsl_generator is not None,
                "query_executor_factory": self.query_executor_factory is not None,
                "config": self.config is not None
            },
            "errors": self.initialization_errors
        }


# Global instance - initialized once at startup
_components: Optional[HealthcareSearchComponents] = None


def initialize_components() -> HealthcareSearchComponents:
    """
    Initialize all core components for the healthcare search system.
    This function should be called once at application startup.
    
    Returns:
        HealthcareSearchComponents: Initialized components container
        
    Raises:
        RuntimeError: If critical components fail to initialize
    """
    global _components
    
    if _components is not None and _components.is_initialized:
        logger.info("Components already initialized, returning existing instance")
        return _components
    
    logger.info("Starting healthcare search components initialization...")
    start_time = datetime.now()
    
    components = HealthcareSearchComponents()
    errors = []
    
    try:
        # Step 1: Initialize configuration
        logger.info("Initializing configuration...")
        components.config = config
        logger.info("✓ Configuration loaded successfully")
        
    except Exception as e:
        error_msg = f"Failed to initialize configuration: {e}"
        logger.error(error_msg)
        errors.append(error_msg)
    
    try:
        # Step 2: Initialize embedding generator
        logger.info("Initializing embedding generator...")
        components.embedding_generator = EmbeddingGenerator()
        
        # Check if consolidated index exists by trying to get statistics
        try:
            stats = components.embedding_generator.get_consolidated_index_statistics()
            if "error" in stats:
                logger.info("Consolidated index not found, creating it...")
                if not components.embedding_generator.create_consolidated_index():
                    raise RuntimeError("Failed to create consolidated index")
        except Exception as e:
            logger.info(f"Consolidated index check failed, creating it: {e}")
            if not components.embedding_generator.create_consolidated_index():
                raise RuntimeError("Failed to create consolidated index")
        
        logger.info("✓ Embedding generator initialized successfully")
        
    except Exception as e:
        error_msg = f"Failed to initialize embedding generator: {e}"
        logger.error(error_msg)
        errors.append(error_msg)
    
    try:
        # Step 3: Initialize query processor
        logger.info("Initializing healthcare query processor...")
        components.query_processor = HealthcareQueryProcessor(
            embedding_generator=components.embedding_generator
        )
        logger.info("✓ Query processor initialized successfully")
        
    except Exception as e:
        error_msg = f"Failed to initialize query processor: {e}"
        logger.error(error_msg)
        errors.append(error_msg)
    
    try:
        # Step 4: Initialize DSL query generator
        logger.info("Initializing DSL query generator...")
        components.dsl_generator = DSLQueryGenerator()
        logger.info("✓ DSL query generator initialized successfully")
        
    except Exception as e:
        error_msg = f"Failed to initialize DSL query generator: {e}"
        logger.error(error_msg)
        errors.append(error_msg)
    
    try:
        # Step 5: Initialize OpenSearch query executor
        logger.info("Initializing OpenSearch query executor...")
        components.query_executor_factory = QueryExecutorFactory()
        logger.info("✓ Query executor factory initialized successfully")
        
    except Exception as e:
        error_msg = f"Failed to initialize query executor: {e}"
        logger.error(error_msg)
        errors.append(error_msg)
    
    # Check if critical components are initialized
    critical_components = [
        components.embedding_generator,
        components.query_processor,
        components.dsl_generator,
        components.query_executor_factory
    ]
    
    if not all(comp is not None for comp in critical_components):
        error_msg = "Critical components failed to initialize"
        logger.error(error_msg)
        components.initialization_errors = errors
        raise RuntimeError(f"{error_msg}. Errors: {errors}")
    
    # Mark as initialized
    components.is_initialized = True
    components.initialization_time = datetime.now()
    components.initialization_errors = errors
    
    initialization_duration = (components.initialization_time - start_time).total_seconds()
    logger.info(f"✓ Healthcare search components initialized successfully in {initialization_duration:.2f}s")
    
    # Store globally
    _components = components
    return components


def get_components() -> HealthcareSearchComponents:
    """
    Get the initialized components.
    If not initialized, attempts to initialize them.
    
    Returns:
        HealthcareSearchComponents: Initialized components
        
    Raises:
        RuntimeError: If components are not initialized and initialization fails
    """
    global _components
    
    if _components is None or not _components.is_initialized:
        logger.warning("Components not initialized, attempting to initialize...")
        return initialize_components()
    
    return _components


def reset_components() -> None:
    """
    Reset the global components instance.
    Useful for testing or re-initialization.
    """
    global _components
    _components = None
    logger.info("Components reset")


def health_check() -> Dict[str, Any]:
    """
    Perform a comprehensive health check of all components.
    
    Returns:
        Dict containing health status of all components
    """
    try:
        components = get_components()
        
        health_status = {
            "overall_status": "healthy" if components.is_initialized else "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "components": components.get_status(),
            "detailed_checks": {}
        }
        
        # Test embedding generator
        if components.embedding_generator:
            try:
                test_embedding = components.embedding_generator.vector_generator.generate_embedding_vector("test")
                health_status["detailed_checks"]["embedding_generator"] = {
                    "status": "healthy",
                    "test_embedding_length": len(test_embedding) if test_embedding else 0
                }
            except Exception as e:
                health_status["detailed_checks"]["embedding_generator"] = {
                    "status": "unhealthy",
                    "error": str(e)
                }
        
        # Test query processor
        if components.query_processor:
            try:
                # Test with a simple query
                test_result = components.query_processor.route_healthcare_query("test healthcare query")
                health_status["detailed_checks"]["query_processor"] = {
                    "status": "healthy",
                    "test_result_keys": list(test_result.keys()) if isinstance(test_result, dict) else []
                }
            except Exception as e:
                health_status["detailed_checks"]["query_processor"] = {
                    "status": "unhealthy",
                    "error": str(e)
                }
        
        # Test DSL generator
        if components.dsl_generator:
            try:
                # Test DSL generation
                test_dsl = components.dsl_generator.generate_dsl_query("test query", "test_index")
                health_status["detailed_checks"]["dsl_generator"] = {
                    "status": "healthy",
                    "test_dsl_type": type(test_dsl).__name__
                }
            except Exception as e:
                health_status["detailed_checks"]["dsl_generator"] = {
                    "status": "unhealthy",
                    "error": str(e)
                }
        
        # Test query executor
        if components.query_executor_factory:
            try:
                executor = components.query_executor_factory.create_executor()
                health_status["detailed_checks"]["query_executor"] = {
                    "status": "healthy",
                    "executor_type": type(executor).__name__
                }
            except Exception as e:
                health_status["detailed_checks"]["query_executor"] = {
                    "status": "unhealthy",
                    "error": str(e)
                }
        
        return health_status
        
    except Exception as e:
        return {
            "overall_status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "error": str(e),
            "components": {"is_initialized": False}
        }


if __name__ == "__main__":
    # Test initialization
    logging.basicConfig(level=logging.INFO)
    
    try:
        components = initialize_components()
        print("✓ Initialization successful!")
        print(f"Status: {components.get_status()}")
        
        # Run health check
        health = health_check()
        print(f"Health check: {health['overall_status']}")
        
    except Exception as e:
        print(f"✗ Initialization failed: {e}")
        sys.exit(1)
