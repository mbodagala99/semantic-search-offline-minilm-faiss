#!/usr/bin/env python3
"""
Model Comparison Tester for Healthcare Query Router
Tests multiple embedding models across different confidence thresholds
"""

import json
import os
import time
import csv
from datetime import datetime
from typing import Dict, List, Any, Tuple
import numpy as np

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config_reader import HealthcareSearchConfig
from embedding_generator import EmbeddingGenerator
from healthcare_query_processor import HealthcareQueryProcessor
from test_healthcare_router_comprehensive import test_healthcare_query_routing

class ModelComparisonTester:
    """Orchestrates comprehensive testing of multiple models and confidence thresholds"""
    
    def __init__(self, regenerate_embeddings=False):
        # Initialize configuration
        self.config = HealthcareSearchConfig()
        
        # Get configuration values
        self.models_to_test = self.config.get_alternative_models()
        self.confidence_thresholds = self.config.get_test_thresholds()
        
        # Test parameters (using config defaults)
        self.results_dir = "results"
        self.individual_dir = os.path.join(self.results_dir, "individual_model_results")
        
        self.results = {}
        self.matrix_data = {}
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.regenerate_embeddings = regenerate_embeddings
        
        # Create directories
        os.makedirs(self.results_dir, exist_ok=True)
        os.makedirs(self.individual_dir, exist_ok=True)
        
        # Create embeddings cache directory
        self.embeddings_cache_dir = "embeddings_cache"
        os.makedirs(self.embeddings_cache_dir, exist_ok=True)
    
    def get_model_cache_path(self, model_name: str) -> str:
        """Get the cache path for a specific model"""
        clean_model_name = model_name.replace('/', '_').replace('-', '_')
        return os.path.join(self.embeddings_cache_dir, clean_model_name)
    
    def test_single_model_optimized(self, model_name: str) -> Dict[str, Any]:
        """Test a single model once and capture all confidence scores"""
        print(f"\n🔧 Testing {model_name} (optimized single run)")
        
        try:
            # Check if embeddings cache exists
            model_cache_path = self.get_model_cache_path(model_name)
            cache_exists = os.path.exists(os.path.join(model_cache_path, "healthcare_semantic_index.faiss"))
            
            if not cache_exists or self.regenerate_embeddings:
                print(f"   📦 Generating embeddings for {model_name}")
                # Create model-specific directory
                os.makedirs(model_cache_path, exist_ok=True)
                
                # Update embedding generator with new model
                embedding_gen = EmbeddingGenerator(model_name=model_name)
                embedding_gen.create_consolidated_index()
                
                # Copy the generated index files to the model-specific cache
                import shutil
                source_files = [
                    "healthcare_semantic_index.faiss",
                    "healthcare_semantic_index.json", 
                    "healthcare_semantic_index_registry.json"
                ]
                
                for file_name in source_files:
                    source_path = os.path.join("indexes", file_name)
                    dest_path = os.path.join(model_cache_path, file_name)
                    if os.path.exists(source_path):
                        shutil.copy2(source_path, dest_path)
                        print(f"   📁 Cached {file_name}")
                
                print(f"   ✅ Embeddings cached in {model_cache_path}")
            else:
                print(f"   📦 Using cached embeddings for {model_name}")
                # Load existing embeddings from cache
                embedding_gen = EmbeddingGenerator(model_name=model_name)
                
                # Temporarily move current indexes and copy cached ones
                import shutil
                original_indexes_dir = "indexes"
                backup_dir = f"{original_indexes_dir}_backup_{self.timestamp}"
                
                if os.path.exists(original_indexes_dir):
                    if not os.path.exists(backup_dir):
                        shutil.move(original_indexes_dir, backup_dir)
                
                # Copy cached files to indexes directory
                os.makedirs(original_indexes_dir, exist_ok=True)
                cached_files = [
                    "healthcare_semantic_index.faiss",
                    "healthcare_semantic_index.json", 
                    "healthcare_semantic_index_registry.json"
                ]
                
                for file_name in cached_files:
                    cached_path = os.path.join(model_cache_path, file_name)
                    dest_path = os.path.join(original_indexes_dir, file_name)
                    if os.path.exists(cached_path):
                        shutil.copy2(cached_path, dest_path)
                
                print(f"   📁 Loaded cached embeddings from {model_cache_path}")
            
            # Run tests with threshold 0.0 to capture all confidence scores
            router = HealthcareQueryProcessor(embedding_gen)
            router.confidence_threshold = 0.0  # Capture all confidence scores
            
            # Run comprehensive tests
            test_results = test_healthcare_query_routing(router, save_results=False)
            
            # Extract detailed results with confidence scores
            query_results = test_results.get('results', [])
            confidence_scores = []
            
            # Debug: Print structure of query_results
            print(f"   🔍 Debug: Found {len(query_results)} query results")
            if query_results:
                print(f"   🔍 Debug: First result keys: {list(query_results[0].keys()) if query_results[0] else 'None'}")
            
            for query_result in query_results:
                if isinstance(query_result, dict) and 'confidence_score' in query_result:
                    confidence_scores.append(query_result['confidence_score'])
                elif isinstance(query_result, dict) and 'confidence' in query_result:
                    confidence_scores.append(query_result['confidence'])
            
            result = {
                'model_name': model_name,
                'total_queries': test_results.get('total_queries', 0),
                'confidence_scores': confidence_scores,
                'query_results': query_results,
                'test_timestamp': datetime.now().isoformat(),
                'model_description': model_name  # Simplified - can add descriptions to config later
            }
            
            print(f"   ✅ Captured {len(confidence_scores)} confidence scores")
            
            # Cleanup: Restore original indexes directory if we used cached embeddings
            if cache_exists and not self.regenerate_embeddings:
                import shutil
                original_indexes_dir = "indexes"
                backup_dir = f"{original_indexes_dir}_backup_{self.timestamp}"
                
                if os.path.exists(backup_dir):
                    # Remove current indexes and restore backup
                    shutil.rmtree(original_indexes_dir)
                    shutil.move(backup_dir, original_indexes_dir)
                    print(f"   🧹 Restored original indexes directory")
            
            return result
            
        except Exception as e:
            print(f"   ❌ Error testing {model_name}: {str(e)}")
            
            # Cleanup on error: Restore original indexes directory
            import shutil
            original_indexes_dir = "indexes"
            backup_dir = f"{original_indexes_dir}_backup_{self.timestamp}"
            
            if os.path.exists(backup_dir):
                shutil.rmtree(original_indexes_dir)
                shutil.move(backup_dir, original_indexes_dir)
                print(f"   🧹 Restored original indexes directory after error")
            
            return {
                'model_name': model_name,
                'error': str(e),
                'confidence_scores': [],
                'query_results': [],
                'total_queries': 0
            }
    
    def calculate_success_rate_at_threshold(self, confidence_scores: List[float], threshold: float) -> float:
        """Calculate success rate at a specific confidence threshold"""
        if not confidence_scores:
            return 0.0
        
        high_confidence_count = sum(1 for score in confidence_scores if score >= threshold)
        return (high_confidence_count / len(confidence_scores)) * 100
    
    def test_all_combinations_optimized(self) -> Dict[str, Any]:
        """Test all models once and generate matrix from confidence scores"""
        print("🚀 Starting Optimized Model Comparison Testing")
        print(f"📊 Testing {len(self.models_to_test)} models (single run each) × {len(self.confidence_thresholds)} thresholds = {len(self.models_to_test)} executions")
        
        model_results = {}
        start_time = time.time()
        
        for i, model_name in enumerate(self.models_to_test, 1):
            print(f"\n📋 Model {i}/{len(self.models_to_test)}: {model_name}")
            result = self.test_single_model_optimized(model_name)
            model_results[model_name] = result
            
            # Save model-specific results
            self.save_model_results(model_name, [result])
        
        end_time = time.time()
        total_time = end_time - start_time
        
        print(f"\n⏱️  Total testing time: {total_time/3600:.2f} hours")
        
        return {
            'model_results': model_results,
            'total_models': len(model_results),
            'total_time_hours': total_time / 3600,
            'timestamp': self.timestamp
        }
    
    def generate_comparison_matrix_optimized(self, model_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comparison matrix from optimized model results"""
        print("\n📊 Generating Comparison Matrix from Confidence Scores...")
        
        # Initialize matrix
        matrix = {}
        for model_name in self.models_to_test:
            matrix[model_name] = {}
            for threshold in self.confidence_thresholds:
                matrix[model_name][threshold] = 0
        
        # Populate matrix with calculated success rates
        for model_name, result in model_results.items():
            confidence_scores = result.get('confidence_scores', [])
            
            for threshold in self.confidence_thresholds:
                success_rate = self.calculate_success_rate_at_threshold(confidence_scores, threshold)
                matrix[model_name][threshold] = success_rate
        
        # Calculate statistics
        stats = self.calculate_matrix_statistics(matrix)
        
        return {
            'matrix': matrix,
            'statistics': stats,
            'models': self.models_to_test,
            'thresholds': self.confidence_thresholds,
            'timestamp': self.timestamp,
            'model_results': model_results
        }
    
    def calculate_matrix_statistics(self, matrix: Dict[str, Dict[float, float]]) -> Dict[str, Any]:
        """Calculate statistics from the comparison matrix"""
        stats = {}
        
        for model_name in self.models_to_test:
            model_scores = [matrix[model_name][t] for t in self.confidence_thresholds]
            stats[model_name] = {
                'max_success_rate': max(model_scores),
                'min_success_rate': min(model_scores),
                'avg_success_rate': np.mean(model_scores),
                'std_success_rate': np.std(model_scores),
                'best_threshold': self.confidence_thresholds[np.argmax(model_scores)],
                'worst_threshold': self.confidence_thresholds[np.argmin(model_scores)]
            }
        
        # Overall statistics
        all_scores = [matrix[model][threshold] for model in self.models_to_test for threshold in self.confidence_thresholds]
        stats['overall'] = {
            'max_success_rate': max(all_scores),
            'min_success_rate': min(all_scores),
            'avg_success_rate': np.mean(all_scores),
            'std_success_rate': np.std(all_scores)
        }
        
        return stats
    
    def save_individual_result(self, result: Dict[str, Any]):
        """Save individual test result"""
        # Clean model name for file path
        clean_model_name = result['model_name'].replace('/', '_').replace('-', '_')
        filename = f"result_{clean_model_name}_{result['confidence_threshold']}_{self.timestamp}.json"
        filepath = os.path.join(self.individual_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(result, f, indent=2)
    
    def save_model_results(self, model_name: str, results: List[Dict[str, Any]]):
        """Save all results for a specific model"""
        filename = OUTPUT_PATTERNS["individual_results"].format(
            model_name=model_name.replace('/', '_').replace('-', '_'),
            timestamp=self.timestamp
        )
        filepath = os.path.join(self.results_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2)
    
    def save_matrix_csv(self, matrix_data: Dict[str, Any]):
        """Save comparison matrix as CSV"""
        filename = OUTPUT_PATTERNS["matrix_csv"].format(timestamp=self.timestamp)
        filepath = os.path.join(self.results_dir, filename)
        
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Header row
            header = ['Model'] + [str(t) for t in self.confidence_thresholds]
            writer.writerow(header)
            
            # Data rows
            for model_name in self.models_to_test:
                row = [model_name] + [f"{matrix_data['matrix'][model_name][t]:.1f}%" for t in self.confidence_thresholds]
                writer.writerow(row)
        
        print(f"📄 Matrix saved to: {filepath}")
        return filepath
    
    def save_matrix_json(self, matrix_data: Dict[str, Any]):
        """Save comparison matrix as JSON"""
        filename = OUTPUT_PATTERNS["matrix_json"].format(timestamp=self.timestamp)
        filepath = os.path.join(self.results_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(matrix_data, f, indent=2)
        
        print(f"📄 Matrix JSON saved to: {filepath}")
        return filepath
    
    def save_summary_report(self, matrix_data: Dict[str, Any]):
        """Save summary report"""
        filename = OUTPUT_PATTERNS["summary_report"].format(timestamp=self.timestamp)
        filepath = os.path.join(self.results_dir, filename)
        
        with open(filepath, 'w') as f:
            f.write("HEALTHCARE QUERY ROUTER - MODEL COMPARISON SUMMARY\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Models Tested: {len(self.models_to_test)}\n")
            f.write(f"Confidence Thresholds: {len(self.confidence_thresholds)}\n")
            f.write(f"Total Tests: {len(self.models_to_test) * len(self.confidence_thresholds)}\n\n")
            
            # Best performing model at each threshold
            f.write("BEST PERFORMING MODEL AT EACH THRESHOLD:\n")
            f.write("-" * 40 + "\n")
            for threshold in self.confidence_thresholds:
                best_model = max(self.models_to_test, key=lambda m: matrix_data['matrix'][m][threshold])
                best_score = matrix_data['matrix'][best_model][threshold]
                f.write(f"Threshold {threshold}: {best_model} ({best_score:.1f}%)\n")
            
            f.write("\nMODEL STATISTICS:\n")
            f.write("-" * 20 + "\n")
            for model_name in self.models_to_test:
                stats = matrix_data['statistics'][model_name]
                f.write(f"\n{model_name}:\n")
                f.write(f"  Max Success Rate: {stats['max_success_rate']:.1f}%\n")
                f.write(f"  Avg Success Rate: {stats['avg_success_rate']:.1f}%\n")
                f.write(f"  Best Threshold: {stats['best_threshold']}\n")
                f.write(f"  Std Deviation: {stats['std_success_rate']:.1f}%\n")
        
        print(f"📄 Summary report saved to: {filepath}")
        return filepath
    
    def run_complete_comparison_optimized(self) -> Dict[str, Any]:
        """Run complete model comparison testing with optimization"""
        print("🎯 Starting Optimized Model Comparison Testing")
        print("=" * 60)
        
        # Test all models once
        test_results = self.test_all_combinations_optimized()
        
        # Generate comparison matrix from confidence scores
        matrix_data = self.generate_comparison_matrix_optimized(test_results['model_results'])
        
        # Save results in multiple formats
        csv_path = self.save_matrix_csv(matrix_data)
        json_path = self.save_matrix_json(matrix_data)
        summary_path = self.save_summary_report(matrix_data)
        
        print("\n🎉 Optimized Model Comparison Testing Completed!")
        print("=" * 60)
        print(f"📊 Results saved to:")
        print(f"   CSV Matrix: {csv_path}")
        print(f"   JSON Data: {json_path}")
        print(f"   Summary: {summary_path}")
        print(f"📦 Embeddings cached in: {self.embeddings_cache_dir}/")
        
        return {
            'test_results': test_results,
            'matrix_data': matrix_data,
            'output_files': {
                'csv': csv_path,
                'json': json_path,
                'summary': summary_path
            }
        }
