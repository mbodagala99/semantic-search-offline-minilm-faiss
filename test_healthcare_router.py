#!/usr/bin/env python3
"""
Test script for Healthcare Query Router

This script demonstrates the intelligent query routing capabilities
for healthcare data queries using semantic similarity search.
"""

import json
from index_router import HealthcareQueryRouter, HealthcareQueryAnalyzer
from embedding_generator import EmbeddingGenerator


def test_healthcare_query_routing():
    """Test the healthcare query routing system with various query types."""
    
    print("🏥 Healthcare Query Router - Test Suite")
    print("=" * 50)
    
    # Initialize the system
    embedding_gen = EmbeddingGenerator()
    query_router = HealthcareQueryRouter(embedding_gen)
    query_analyzer = HealthcareQueryAnalyzer(query_router)
    
    # Test queries covering different scenarios
    test_queries = [
        # High confidence queries
        {
            "query": "Show me fraud detection reports for Q3 2024",
            "expected_confidence": "HIGH",
            "description": "Specific fraud detection query with timeframe"
        },
        {
            "query": "Generate provider network adequacy analysis for cardiology",
            "expected_confidence": "HIGH", 
            "description": "Specific provider analysis query"
        },
        {
            "query": "Create claims payment reconciliation report for last month",
            "expected_confidence": "HIGH",
            "description": "Specific claims processing query"
        },
        
        # Low confidence queries
        {
            "query": "show me data",
            "expected_confidence": "LOW",
            "description": "Generic query without specifics"
        },
        {
            "query": "claims",
            "expected_confidence": "LOW",
            "description": "Single word query"
        },
        {
            "query": "analysis",
            "expected_confidence": "LOW",
            "description": "Generic analysis request"
        },
        
        # Medium complexity queries
        {
            "query": "provider performance metrics",
            "expected_confidence": "MEDIUM",
            "description": "Provider query without timeframe"
        },
        {
            "query": "fraud detection for 2024",
            "expected_confidence": "MEDIUM",
            "description": "Fraud query with partial timeframe"
        }
    ]
    
    print(f"\n🔍 Testing {len(test_queries)} Healthcare Queries:")
    print("-" * 50)
    
    high_confidence_count = 0
    low_confidence_count = 0
    
    for i, test_case in enumerate(test_queries, 1):
        query = test_case["query"]
        expected = test_case["expected_confidence"]
        description = test_case["description"]
        
        print(f"\n{i}. {description}")
        print(f"   Query: '{query}'")
        print(f"   Expected: {expected} confidence")
        print("-" * 30)
        
        # Route the query
        routing_result = query_router.route_healthcare_query(query)
        
        # Analyze the result
        analysis = routing_result["routing_analysis"]
        confidence_score = analysis["confidence_score"]
        routing_status = analysis["routing_status"]
        
        print(f"   Actual Confidence: {confidence_score:.3f}")
        print(f"   Routing Status: {routing_status}")
        
        # Count results
        if routing_status == "HIGH_CONFIDENCE":
            high_confidence_count += 1
            print(f"   ✅ High Confidence Match")
            print(f"   Data Source: {analysis['primary_data_source']}")
            print(f"   Recommendation: {routing_result['routing_recommendation']}")
        else:
            low_confidence_count += 1
            print(f"   ⚠️  Requires Clarification")
            clarification = routing_result["clarification_request"]
            print(f"   Message: {clarification['message']}")
            print(f"   Available Domains: {len(clarification['available_healthcare_domains'])}")
        
        # Get query recommendations
        recommendations = query_analyzer.get_query_recommendations(query)
        if recommendations["query_recommendations"]["improvement_suggestions"]:
            print("   Improvement Suggestions:")
            for suggestion in recommendations["query_recommendations"]["improvement_suggestions"]:
                print(f"   - {suggestion}")
    
    # Summary
    print(f"\n📊 Test Results Summary:")
    print("-" * 30)
    print(f"   Total Queries Tested: {len(test_queries)}")
    print(f"   High Confidence Matches: {high_confidence_count}")
    print(f"   Low Confidence (Clarification): {low_confidence_count}")
    print(f"   Success Rate: {(high_confidence_count / len(test_queries)) * 100:.1f}%")
    
    return {
        "total_queries": len(test_queries),
        "high_confidence": high_confidence_count,
        "low_confidence": low_confidence_count,
        "success_rate": (high_confidence_count / len(test_queries)) * 100
    }


def test_query_complexity_analysis():
    """Test the query complexity analysis functionality."""
    
    print(f"\n🧠 Query Complexity Analysis Test:")
    print("-" * 40)
    
    # Initialize the system
    embedding_gen = EmbeddingGenerator()
    query_router = HealthcareQueryRouter(embedding_gen)
    query_analyzer = HealthcareQueryAnalyzer(query_router)
    
    complexity_test_queries = [
        "Show me fraud detection reports for Q3 2024 with detailed analysis",
        "provider performance",
        "data",
        "Generate comprehensive provider network adequacy analysis for cardiology services in Q3 2024"
    ]
    
    for i, query in enumerate(complexity_test_queries, 1):
        print(f"\n{i}. Query: '{query}'")
        
        # Analyze complexity
        complexity_result = query_analyzer.analyze_query_complexity(query)
        complexity_analysis = complexity_result["query_complexity_analysis"]
        
        print(f"   Word Count: {complexity_analysis['word_count']}")
        print(f"   Has Timeframe: {complexity_analysis['has_timeframe']}")
        print(f"   Has Domain: {complexity_analysis['has_domain_specification']}")
        print(f"   Has Analysis Type: {complexity_analysis['has_analysis_type']}")
        print(f"   Complexity Score: {complexity_analysis['complexity_score']}")
        print(f"   Complexity Level: {complexity_analysis['complexity_level']}")


def test_routing_statistics():
    """Test the routing system statistics."""
    
    print(f"\n📈 Routing System Statistics Test:")
    print("-" * 40)
    
    # Initialize the system
    embedding_gen = EmbeddingGenerator()
    query_router = HealthcareQueryRouter(embedding_gen)
    
    # Get statistics
    stats = query_router.get_routing_statistics()
    
    print("Routing System Information:")
    system_info = stats["routing_system_info"]
    for key, value in system_info.items():
        print(f"   {key}: {value}")
    
    if "index_statistics" in stats:
        print("\nIndex Statistics:")
        index_stats = stats["index_statistics"]
        for key, value in index_stats.items():
            print(f"   {key}: {value}")
    elif "error" in stats:
        print(f"\nError retrieving index statistics: {stats['error']}")


def demonstrate_clarification_workflow():
    """Demonstrate the clarification workflow for low confidence queries."""
    
    print(f"\n🔄 Clarification Workflow Demonstration:")
    print("-" * 45)
    
    # Initialize the system
    embedding_gen = EmbeddingGenerator()
    query_router = HealthcareQueryRouter(embedding_gen)
    query_analyzer = HealthcareQueryAnalyzer(query_router)
    
    # Start with a generic query
    original_query = "show me data"
    print(f"1. Original Query: '{original_query}'")
    
    # Get routing result
    routing_result = query_router.route_healthcare_query(original_query)
    analysis = routing_result["routing_analysis"]
    
    print(f"   Confidence Score: {analysis['confidence_score']:.3f}")
    print(f"   Status: {analysis['routing_status']}")
    
    if analysis["routing_status"] == "REQUIRES_CLARIFICATION":
        clarification = routing_result["clarification_request"]
        print(f"\n2. Clarification Request:")
        print(f"   Message: {clarification['message']}")
        print(f"   Available Domains:")
        for domain in clarification["available_healthcare_domains"]:
            print(f"   - {domain}")
        
        print(f"\n   Sample Queries:")
        for sample in clarification["sample_healthcare_queries"]:
            print(f"   - {sample}")
        
        # Simulate improved query
        improved_query = "Show me fraud detection reports for Q3 2024"
        print(f"\n3. Improved Query: '{improved_query}'")
        
        # Test improved query
        improved_result = query_router.route_healthcare_query(improved_query)
        improved_analysis = improved_result["routing_analysis"]
        
        print(f"   Confidence Score: {improved_analysis['confidence_score']:.3f}")
        print(f"   Status: {improved_analysis['routing_status']}")
        
        if improved_analysis["routing_status"] == "HIGH_CONFIDENCE":
            print(f"   ✅ Successfully routed to: {improved_analysis['primary_data_source']}")
            print(f"   Recommendation: {improved_result['routing_recommendation']}")


def main():
    """Main test function."""
    
    try:
        # Run all tests
        test_results = test_healthcare_query_routing()
        test_query_complexity_analysis()
        test_routing_statistics()
        demonstrate_clarification_workflow()
        
        print(f"\n🎉 All Tests Completed Successfully!")
        print(f"   Overall Success Rate: {test_results['success_rate']:.1f}%")
        
    except Exception as e:
        print(f"\n❌ Test Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
