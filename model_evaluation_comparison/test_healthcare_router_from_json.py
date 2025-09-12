#!/usr/bin/env python3
"""
Healthcare Query Router Test Script - JSON File Based

This script tests the intelligent query routing capabilities
for healthcare data queries using semantic similarity search
by reading test queries from separate JSON files for each index type.
"""

import json
import csv
import sys
import os
from datetime import datetime
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from index_router import HealthcareQueryRouter, HealthcareQueryAnalyzer
from embedding_generator import EmbeddingGenerator


def load_queries_from_json_files(queries_dir="test_queries"):
    """Load all test queries from JSON files in the specified directory."""
    
    all_queries = []
    query_files = []
    
    # Find all JSON files in the queries directory
    queries_path = Path(queries_dir)
    if not queries_path.exists():
        raise FileNotFoundError(f"Queries directory {queries_dir} not found")
    
    json_files = list(queries_path.glob("*.json"))
    json_files.sort()  # Sort to ensure consistent order
    
    print(f"Found {len(json_files)} query files:")
    
    for json_file in json_files:
        print(f"  Loading {json_file.name}...")
        
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extract queries from the JSON structure
        queries = data.get('queries', [])
        index_name = data.get('index_name', 'unknown')
        
        print(f"    - {len(queries)} queries for {index_name}")
        
        # Add queries to the main list
        all_queries.extend(queries)
        query_files.append({
            'filename': json_file.name,
            'index_name': index_name,
            'query_count': len(queries)
        })
    
    print(f"\nTotal queries loaded: {len(all_queries)}")
    return all_queries, query_files


def test_healthcare_query_routing(query_router=None, save_results=True):
    """Test the healthcare query routing system with queries loaded from JSON files."""
    
    if query_router is None:
        # Initialize the embedding generator and router
        embedding_gen = EmbeddingGenerator()
        query_router = HealthcareQueryRouter(embedding_gen)
    
    # Load queries from JSON files
    print("🏥 Healthcare Query Router - JSON File Based Test Suite")
    print("=" * 60)
    
    try:
        test_queries, query_files = load_queries_from_json_files()
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        return None
    
    print(f"\n🔍 Testing {len(test_queries)} healthcare queries from {len(query_files)} files...")
    print("=" * 60)
    
    results = []
    high_confidence_matches = 0
    low_confidence_clarification = 0
    
    for i, test_case in enumerate(test_queries, 1):
        query = test_case["query"]
        description = test_case["description"]
        expected_index = test_case["expected_index"]
        
        print(f"\n{i:3d}. {description}")
        print(f"     Query: '{query}'")
        print("-" * 50)
        
        try:
            # Route the query
            routing_result = query_router.route_healthcare_query(query)
            
            # Extract key information
            confidence_score = routing_result.get('routing_analysis', {}).get('confidence_score', 0.0)
            routing_status = routing_result.get('routing_analysis', {}).get('routing_status', 'UNKNOWN')
            primary_data_source = routing_result.get('routing_analysis', {}).get('primary_data_source', 'UNKNOWN')
            recommendation = routing_result.get('routing_recommendation', 'No recommendation available')
            
            # Determine if it's a high confidence match
            if confidence_score >= query_router.confidence_threshold:
                high_confidence_matches += 1
                status_icon = "✅"
                status_text = "High Confidence Match"
            else:
                low_confidence_clarification += 1
                status_icon = "❓"
                status_text = "Low Confidence - Clarification"
            
            print(f"     Confidence: {confidence_score:.3f}")
            print(f"     Status: {routing_status}")
            print(f"     {status_icon} {status_text}")
            print(f"     Data Source: {primary_data_source}")
            print(f"     Recommendation: {recommendation}")
            
            # Store result
            result = {
                "test_number": test_case["test_number"],
                "query": query,
                "description": description,
                "expected_index": expected_index,
                "confidence_score": confidence_score,
                "routing_status": routing_status,
                "primary_data_source": primary_data_source,
                "recommendation": recommendation,
                "improvement_suggestions_count": len(routing_result.get('improvement_suggestions', [])),
                "improvement_suggestions": routing_result.get('improvement_suggestions', [])
            }
            results.append(result)
            
        except Exception as e:
            print(f"     ❌ Error: {e}")
            result = {
                "test_number": test_case["test_number"],
                "query": query,
                "description": description,
                "expected_index": expected_index,
                "confidence_score": 0.0,
                "routing_status": "ERROR",
                "primary_data_source": "ERROR",
                "recommendation": f"Error: {e}",
                "improvement_suggestions_count": 0,
                "improvement_suggestions": []
            }
            results.append(result)
    
    # Calculate success rate
    total_queries = len(test_queries)
    success_rate = (high_confidence_matches / total_queries) * 100 if total_queries > 0 else 0
    
    # Print summary
    print(f"\n📊 Test Results Summary:")
    print("-" * 50)
    print(f"   Total Queries Tested: {total_queries}")
    print(f"   High Confidence Matches: {high_confidence_matches}")
    print(f"   Low Confidence (Clarification): {low_confidence_clarification}")
    print(f"   Success Rate: {success_rate:.1f}%")
    
    # Print breakdown by index
    print(f"\n📋 Results by Index:")
    print("-" * 30)
    index_stats = {}
    for result in results:
        index_name = result['expected_index']
        if index_name not in index_stats:
            index_stats[index_name] = {'total': 0, 'high_confidence': 0, 'low_confidence': 0}
        
        index_stats[index_name]['total'] += 1
        if result['routing_status'] == 'HIGH_CONFIDENCE':
            index_stats[index_name]['high_confidence'] += 1
        else:
            index_stats[index_name]['low_confidence'] += 1
    
    for index_name, stats in index_stats.items():
        success_rate = (stats['high_confidence'] / stats['total']) * 100 if stats['total'] > 0 else 0
        print(f"   {index_name}:")
        print(f"     Total: {stats['total']}, High Confidence: {stats['high_confidence']}, Success Rate: {success_rate:.1f}%")
    
    # Save results if requested
    if save_results:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save JSON results
        json_filename = f"healthcare_router_json_test_{timestamp}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump({
                "test_summary": {
                    "total_queries": total_queries,
                    "high_confidence_matches": high_confidence_matches,
                    "low_confidence_clarification": low_confidence_clarification,
                    "success_rate": success_rate,
                    "timestamp": timestamp,
                    "query_files_used": query_files
                },
                "index_breakdown": index_stats,
                "test_results": results
            }, f, indent=2, ensure_ascii=False)
        
        # Save CSV results
        csv_filename = f"healthcare_router_json_test_{timestamp}.csv"
        with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
            if results:
                writer = csv.DictWriter(f, fieldnames=results[0].keys())
                writer.writeheader()
                writer.writerows(results)
        
        # Save summary report
        report_filename = f"healthcare_router_json_test_{timestamp}.txt"
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write("Healthcare Query Router - JSON File Based Test Report\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Queries: {total_queries}\n")
            f.write(f"High Confidence Matches: {high_confidence_matches}\n")
            f.write(f"Low Confidence Clarification: {low_confidence_clarification}\n")
            f.write(f"Success Rate: {success_rate:.1f}%\n\n")
            
            f.write("Query Files Used:\n")
            f.write("-" * 20 + "\n")
            for file_info in query_files:
                f.write(f"{file_info['filename']}: {file_info['query_count']} queries for {file_info['index_name']}\n")
            
            f.write(f"\nIndex Breakdown:\n")
            f.write("-" * 20 + "\n")
            for index_name, stats in index_stats.items():
                success_rate = (stats['high_confidence'] / stats['total']) * 100 if stats['total'] > 0 else 0
                f.write(f"{index_name}: {stats['total']} total, {stats['high_confidence']} high confidence ({success_rate:.1f}%)\n")
            
            f.write(f"\nDetailed Results:\n")
            f.write("-" * 20 + "\n")
            for result in results:
                f.write(f"\nTest {result['test_number']:3d}: {result['description']}\n")
                f.write(f"Query: {result['query']}\n")
                f.write(f"Confidence: {result['confidence_score']:.3f}\n")
                f.write(f"Status: {result['routing_status']}\n")
                f.write(f"Data Source: {result['primary_data_source']}\n")
        
        print(f"\n📄 Results saved to:")
        print(f"   JSON: {json_filename}")
        print(f"   CSV: {csv_filename}")
        print(f"   Report: {report_filename}")
    
    return {
        "total_queries": total_queries,
        "high_confidence_matches": high_confidence_matches,
        "low_confidence_clarification": low_confidence_clarification,
        "success_rate": success_rate,
        "index_breakdown": index_stats,
        "results": results
    }


def main():
    """Main function to run the healthcare query routing test from JSON files."""
    print("🏥 Healthcare Query Router - JSON File Based Test Suite")
    print("=" * 60)
    
    # Initialize the embedding generator and router
    embedding_gen = EmbeddingGenerator()
    router = HealthcareQueryRouter(embedding_gen)
    
    # Run the test
    result_data = test_healthcare_query_routing(router, save_results=True)
    
    if result_data:
        print(f"\n🎉 Testing completed!")
        print(f"Success Rate: {result_data['success_rate']:.1f}%")
    else:
        print(f"\n❌ Testing failed!")


if __name__ == "__main__":
    main()
