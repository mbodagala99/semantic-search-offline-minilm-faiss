#!/usr/bin/env python3
"""
Healthcare Query Processor - Comprehensive Query Processing System

This module provides comprehensive healthcare query processing capabilities including:
- Healthcare/non-healthcare pre-classification using ensemble models
- Intelligent routing to appropriate data indexes using semantic similarity search
- Analytics and performance tracking
- Enhanced error handling
- User context support and comprehensive logging

"""

import json
import os
import time
from typing import Dict, List, Any, Optional
from datetime import datetime
from embedding_generator import EmbeddingGenerator
from config_reader import config
from classifiers import ClassifierFactory


class HealthcareQueryProcessor:
    """
    Comprehensive healthcare query processing system.
    
    Provides end-to-end healthcare query processing including pre-classification,
    intelligent routing, analytics tracking, and enhanced error handling with
    and user context support.
    """
    
    def __init__(self, embedding_generator: EmbeddingGenerator):
        """
        Initialize the healthcare query processor.
        
        Args:
            embedding_generator: Instance of EmbeddingGenerator for semantic search
        """
        self.embedding_generator = embedding_generator
        # Use configuration for thresholds
        self.confidence_threshold = config.get_default_threshold()
        self.minimum_threshold = config.get_minimum_threshold()
        self.available_domains = [
            "Claims Processing and Payment Reconciliation",
            "Provider Network Management", 
            "Fraud Detection and Investigation",
            "Financial Reporting and Analytics"
        ]
        
        # Initialize healthcare classifier
        self.classifier = self._initialize_classifier()
        
        # Analytics and performance tracking
        self.query_count = 0
        self.classification_count = 0
        self.rejection_count = 0
        self.error_count = 0
        self.total_processing_time = 0.0
        
        # Enhanced configuration
        self.enable_analytics = True  # Default to True
        self.log_classification_results = True  # Default to True
    
    def _initialize_classifier(self):
        """Initialize the healthcare classifier"""
        try:
            classifier_config = {
                'model_name': config.get_bart_model(),
                'confidence_threshold': config.get_classifier_threshold(),
                'device': config.get_classifier_device(),
                'voting_strategy': config.get_voting_strategy(),
                'bart_weight': config.get_bart_weight(),
                'keyword_weight': config.get_keyword_weight(),
                'min_confidence_threshold': config.get_min_confidence_threshold()
            }
            return ClassifierFactory.create_classifier(
                config.get_classifier_type(),
                classifier_config
            )
        except Exception as e:
            print(f"Warning: Could not initialize classifier: {e}")
            return None
    
    def route_healthcare_query(self, user_query: str, user_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Route a healthcare query to the most appropriate data source.
        
        Args:
            user_query: The user's query string
            user_context: Optional user context information
            
        Returns:
            Dictionary containing routing analysis and recommendations
        """
        # Analytics tracking
        start_time = time.time()
        self.query_count += 1
        
        try:
            # Step 1: Enhanced healthcare/non-healthcare classification
            if self.classifier and self.classifier.is_available():
                classification_result = self.classifier.classify(user_query)
                self.classification_count += 1
                
                # Log classification results if enabled
                if self.log_classification_results:
                    self._log_classification_result(user_query, classification_result)
                
                # If not healthcare, reject early with enhanced response
                if not self.classifier.should_route_to_healthcare(classification_result):
                    self.rejection_count += 1
                    processing_time = (time.time() - start_time) * 1000
                    self.total_processing_time += processing_time
                    
                    return self._create_enhanced_rejection_response(
                        user_query, classification_result, user_context, processing_time
                    )
            
            # Step 2: If healthcare, proceed with existing similarity search
            result = self._perform_similarity_search(user_query)
            
            # Update analytics
            processing_time = (time.time() - start_time) * 1000
            self.total_processing_time += processing_time
            
            # Add analytics to result
            if self.enable_analytics:
                result["analytics"] = {
                    "processing_time_ms": processing_time,
                    "query_count": self.query_count,
                    "classification_count": self.classification_count,
                    "rejection_count": self.rejection_count,
                    "timestamp": datetime.now().isoformat()
                }
            
            return result
                
        except Exception as e:
            self.error_count += 1
            processing_time = (time.time() - start_time) * 1000
            self.total_processing_time += processing_time
            
            return self._create_enhanced_error_response(user_query, str(e), processing_time)
    
    def _create_enhanced_rejection_response(self, user_query: str, classification_result, 
                                          user_context: Dict[str, Any] = None, 
                                          processing_time: float = 0.0) -> Dict[str, Any]:
        """Create enhanced rejection response for non-healthcare queries"""
        
        # No suggestions for now - keeping it minimal
        
        # Create base response
        response = {
            "query": user_query,
            "routing_status": "REJECTED_NON_HEALTHCARE",
            "confidence_score": classification_result.confidence,
            "primary_data_source": "N/A",
            "processing_time_ms": processing_time,
            "classification_info": {
                "is_healthcare": classification_result.is_healthcare,
                "model_name": classification_result.model_name,
                "processing_time_ms": classification_result.processing_time_ms,
                "raw_response": classification_result.raw_response
            },
            "message": "Query appears to be non-healthcare related. Please provide a healthcare-specific query.",
            "timestamp": datetime.now().isoformat()
        }
        
        # No suggestions added - keeping response minimal
        
        # Add user context if provided
        if user_context:
            response["user_context"] = {
                "user_id": user_context.get("user_id"),
                "session_id": user_context.get("session_id"),
                "previous_queries": user_context.get("previous_queries", [])
            }
        
        # Add analytics
        if self.enable_analytics:
            response["analytics"] = {
                "query_count": self.query_count,
                "classification_count": self.classification_count,
                "rejection_count": self.rejection_count,
                "rejection_rate": (self.rejection_count / self.query_count) * 100 if self.query_count > 0 else 0
            }
        
        return response
    
    def _create_enhanced_error_response(self, user_query: str, error_message: str, 
                                      processing_time: float = 0.0) -> Dict[str, Any]:
        """Create enhanced error response with analytics"""
        response = {
            "query": user_query,
            "routing_status": "ERROR",
            "confidence_score": 0.0,
            "primary_data_source": "N/A",
            "processing_time_ms": processing_time,
            "message": f"Error processing query: {error_message}",
            "timestamp": datetime.now().isoformat(),
            "error_details": {
                "error_type": "processing_error",
                "error_message": error_message
            }
        }
        
        # Add analytics
        if self.enable_analytics:
            response["analytics"] = {
                "query_count": self.query_count,
                "error_count": self.error_count,
                "error_rate": (self.error_count / self.query_count) * 100 if self.query_count > 0 else 0
            }
        
        return response
    
    def _create_error_response(self, user_query: str, error_message: str) -> Dict[str, Any]:
        """Create basic error response (backward compatibility)"""
        return self._create_enhanced_error_response(user_query, error_message, 0.0)
    
    
    def _log_classification_result(self, query: str, classification_result) -> None:
        """Log classification results for analytics and debugging"""
        try:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "query": query,
                "is_healthcare": classification_result.is_healthcare,
                "confidence": classification_result.confidence,
                "model_name": classification_result.model_name,
                "processing_time_ms": classification_result.processing_time_ms
            }
            
            # Log to console if enabled
            if self.log_classification_results:
                print(f"🔍 Classification: {query[:50]}... -> {'Healthcare' if classification_result.is_healthcare else 'Non-Healthcare'} (conf: {classification_result.confidence:.3f})")
            
            # Could also log to file or database here
            # self._write_to_log_file(log_entry)
            
        except Exception as e:
            print(f"Warning: Could not log classification result: {e}")
    
    def get_analytics_summary(self) -> Dict[str, Any]:
        """Get comprehensive analytics summary"""
        return {
            "total_queries": self.query_count,
            "classification_count": self.classification_count,
            "rejection_count": self.rejection_count,
            "error_count": self.error_count,
            "total_processing_time_ms": self.total_processing_time,
            "average_processing_time_ms": self.total_processing_time / self.query_count if self.query_count > 0 else 0,
            "rejection_rate": (self.rejection_count / self.query_count) * 100 if self.query_count > 0 else 0,
            "error_rate": (self.error_count / self.query_count) * 100 if self.query_count > 0 else 0,
            "classification_rate": (self.classification_count / self.query_count) * 100 if self.query_count > 0 else 0,
            "timestamp": datetime.now().isoformat()
        }
    
    def reset_analytics(self) -> None:
        """Reset analytics counters"""
        self.query_count = 0
        self.classification_count = 0
        self.rejection_count = 0
        self.error_count = 0
        self.total_processing_time = 0.0
        print("📊 Analytics counters reset")
    
    def _perform_similarity_search(self, user_query: str) -> Dict[str, Any]:
        """Perform semantic similarity search for healthcare queries"""
        # Search the consolidated healthcare index
        search_results = self.embedding_generator.search_consolidated_index(
            user_query, 
            top_k=5
        )
        
        # Calculate confidence score from best match
        confidence_score = self._calculate_confidence_score(search_results)
        
        # Make routing decision based on confidence threshold
        if confidence_score >= self.confidence_threshold:
            return self._create_high_confidence_routing_response(
                user_query, confidence_score, search_results
            )
        else:
            return self._create_clarification_request_response(
                user_query, confidence_score
            )
    
    def _calculate_confidence_score(self, search_results: List[Dict[str, Any]]) -> float:
        """
        Calculate confidence score from search results.
        
        Args:
            search_results: List of search results from semantic search
            
        Returns:
            Confidence score between 0.0 and 1.0
        """
        if not search_results:
            return 0.0
        
        # Use the highest similarity score as confidence
        return max(result.get('similarity_score', 0.0) for result in search_results)
    
    def _create_high_confidence_routing_response(
        self, 
        user_query: str, 
        confidence_score: float, 
        search_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Create response for high confidence matches.
        
        Args:
            user_query: Original user query
            confidence_score: Calculated confidence score
            search_results: Search results from semantic search
            
        Returns:
            High confidence routing response
        """
        best_match = search_results[0]
        
        return {
            "user_query": user_query,
            "routing_analysis": {
                "confidence_score": confidence_score,
                "routing_status": "HIGH_CONFIDENCE",
                "primary_data_source": best_match.get('source_index'),
                "index_file_path": "indexes/healthcare_semantic_index.faiss",
                "matching_capabilities": [best_match.get('text', '')[:100] + "..."]
            },
            "routing_recommendation": f"Proceed with {best_match.get('source_index')} for your analysis"
        }
    
    def _create_clarification_request_response(
        self, 
        user_query: str, 
        confidence_score: float
    ) -> Dict[str, Any]:
        """
        Create clarification request for low confidence matches.
        
        Args:
            user_query: Original user query
            confidence_score: Calculated confidence score
            
        Returns:
            Clarification request response
        """
        return {
            "user_query": user_query,
            "routing_analysis": {
                "confidence_score": confidence_score,
                "routing_status": "REQUIRES_CLARIFICATION",
                "reason": "Query too generic - confidence below 0.5 threshold"
            },
            "clarification_request": {
                "message": "Your query needs more specific details to find the right data source",
                "available_healthcare_domains": self.available_domains,
                "required_query_details": [
                    "Specific domain (claims, providers, fraud, etc.)",
                    "Time period (date range, quarter, etc.)",
                    "Type of analysis or report needed"
                ],
                "sample_healthcare_queries": [
                    "Show me fraud detection reports for Q3 2024",
                    "Generate provider network adequacy analysis for cardiology",
                    "Create claims payment reconciliation report for last month",
                    "Analyze provider performance metrics for emergency services"
                ]
            }
        }
    
    def get_routing_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the routing system.
        
        Returns:
            Dictionary containing routing system statistics
        """
        try:
            index_stats = self.embedding_generator.get_consolidated_index_statistics()
            return {
                "routing_system_info": {
                    "confidence_threshold": self.confidence_threshold,
                    "available_domains_count": len(self.available_domains),
                    "routing_decision_levels": 2
                },
                "index_statistics": index_stats
            }
        except Exception as e:
            return {
                "routing_system_info": {
                    "confidence_threshold": self.confidence_threshold,
                    "available_domains_count": len(self.available_domains),
                    "routing_decision_levels": 2
                },
                "error": f"Could not retrieve index statistics: {str(e)}"
            }


class HealthcareQueryAnalyzer:
    """
    Analyzer for healthcare queries to provide insights and recommendations.
    """
    
    def __init__(self, query_router: HealthcareQueryProcessor):
        """
        Initialize the healthcare query analyzer.
        
        Args:
            query_router: Instance of HealthcareQueryProcessor
        """
        self.query_router = query_router
    
    def analyze_query_complexity(self, user_query: str) -> Dict[str, Any]:
        """
        Analyze the complexity of a healthcare query.
        
        Args:
            user_query: The user's query string
            
        Returns:
            Dictionary containing complexity analysis
        """
        # Basic complexity indicators
        word_count = len(user_query.split())
        has_timeframe = any(word in user_query.lower() for word in ['quarter', 'month', 'year', '2024', '2023'])
        has_domain = any(domain.lower() in user_query.lower() for domain in ['claims', 'provider', 'fraud', 'financial'])
        has_analysis_type = any(word in user_query.lower() for word in ['report', 'analysis', 'metrics', 'performance'])
        
        complexity_score = 0
        if word_count > 5:
            complexity_score += 1
        if has_timeframe:
            complexity_score += 1
        if has_domain:
            complexity_score += 1
        if has_analysis_type:
            complexity_score += 1
        
        return {
            "query_complexity_analysis": {
                "word_count": word_count,
                "has_timeframe": has_timeframe,
                "has_domain_specification": has_domain,
                "has_analysis_type": has_analysis_type,
                "complexity_score": complexity_score,
                "complexity_level": self._get_complexity_level(complexity_score)
            }
        }
    
    def _get_complexity_level(self, score: int) -> str:
        """Get complexity level based on score."""
        if score >= 3:
            return "HIGH"
        elif score >= 2:
            return "MEDIUM"
        else:
            return "LOW"
    
    def get_query_recommendations(self, user_query: str) -> Dict[str, Any]:
        """
        Get recommendations for improving a healthcare query.
        
        Args:
            user_query: The user's query string
            
        Returns:
            Dictionary containing query improvement recommendations
        """
        complexity_analysis = self.analyze_query_complexity(user_query)
        routing_result = self.query_router.route_healthcare_query(user_query)
        
        recommendations = []
        
        if routing_result["routing_analysis"]["routing_status"] == "REQUIRES_CLARIFICATION":
            if not complexity_analysis["query_complexity_analysis"]["has_domain_specification"]:
                recommendations.append("Specify the healthcare domain (claims, providers, fraud, etc.)")
            if not complexity_analysis["query_complexity_analysis"]["has_timeframe"]:
                recommendations.append("Add a time period (quarter, month, year, date range)")
            if not complexity_analysis["query_complexity_analysis"]["has_analysis_type"]:
                recommendations.append("Specify the type of analysis or report needed")
        
        return {
            "query_recommendations": {
                "original_query": user_query,
                "routing_status": routing_result["routing_analysis"]["routing_status"],
                "confidence_score": routing_result["routing_analysis"]["confidence_score"],
                "improvement_suggestions": recommendations,
                "complexity_analysis": complexity_analysis["query_complexity_analysis"]
            }
        }


def main():
    """Main function to demonstrate the healthcare query routing system."""
    print("🏥 Healthcare Query Router - Intelligent Data Source Routing")
    print("=" * 60)
    
    # Initialize the embedding generator
    embedding_gen = EmbeddingGenerator()
    
    # Initialize the query router
    query_router = HealthcareQueryProcessor(embedding_gen)
    
    # Initialize the query analyzer
    query_analyzer = HealthcareQueryAnalyzer(query_router)
    
    # Test queries
    test_queries = [
        "Show me fraud detection reports for Q3 2024",
        "Generate provider network adequacy analysis for cardiology",
        "show me data",
        "claims analysis",
        "provider performance metrics for emergency services"
    ]
    
    print("\n🔍 Testing Healthcare Query Routing:")
    print("-" * 40)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: '{query}'")
        print("-" * 30)
        
        # Route the query
        routing_result = query_router.route_healthcare_query(query)
        
        # Display routing analysis
        analysis = routing_result["routing_analysis"]
        print(f"   Confidence Score: {analysis['confidence_score']:.3f}")
        print(f"   Routing Status: {analysis['routing_status']}")
        
        if analysis["routing_status"] == "HIGH_CONFIDENCE":
            print(f"   Primary Data Source: {analysis['primary_data_source']}")
            print(f"   Recommendation: {routing_result['routing_recommendation']}")
        else:
            print("   Clarification Required:")
            clarification = routing_result["clarification_request"]
            print(f"   Message: {clarification['message']}")
            print(f"   Available Domains: {len(clarification['available_healthcare_domains'])}")
            print(f"   Sample Queries: {len(clarification['sample_healthcare_queries'])}")
        
        # Get query recommendations
        recommendations = query_analyzer.get_query_recommendations(query)
        if recommendations["query_recommendations"]["improvement_suggestions"]:
            print("   Improvement Suggestions:")
            for suggestion in recommendations["query_recommendations"]["improvement_suggestions"]:
                print(f"   - {suggestion}")
    
    # Display system statistics
    print("\n📊 Healthcare Query Router Statistics:")
    print("-" * 40)
    stats = query_router.get_routing_statistics()
    system_info = stats["routing_system_info"]
    print(f"   Confidence Threshold: {system_info['confidence_threshold']}")
    print(f"   Available Domains: {system_info['available_domains_count']}")
    print(f"   Routing Decision Levels: {system_info['routing_decision_levels']}")
    
    if "index_statistics" in stats:
        index_stats = stats["index_statistics"]
        print(f"   Total Embeddings: {index_stats.get('total_embeddings', 'N/A')}")
        print(f"   Index Dimensions: {index_stats.get('embedding_dimensions', 'N/A')}")
        print(f"   Source Files: {index_stats.get('source_files_count', 'N/A')}")


if __name__ == "__main__":
    main()
