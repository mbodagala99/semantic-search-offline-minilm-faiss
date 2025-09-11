#!/usr/bin/env python3
"""
Main execution script for Healthcare Query Router Model Comparison
Generates comprehensive comparison matrix of multiple embedding models across confidence thresholds
"""

import sys
import os
from datetime import datetime

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from model_comparison_tester import ModelComparisonTester
from model_config import MODELS_TO_TEST, CONFIDENCE_THRESHOLDS

def main():
    """Main execution function"""
    print("🏥 Healthcare Query Router - Model Comparison Testing")
    print("=" * 60)
    print(f"📅 Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🤖 Models to Test: {len(MODELS_TO_TEST)}")
    print(f"🎯 Confidence Thresholds: {len(CONFIDENCE_THRESHOLDS)}")
    print(f"📊 Total Test Combinations: {len(MODELS_TO_TEST) * len(CONFIDENCE_THRESHOLDS)}")
    print("=" * 60)
    
    # Display models and thresholds
    print("\n📋 Models to Test:")
    for i, model in enumerate(MODELS_TO_TEST, 1):
        print(f"   {i}. {model}")
    
    print(f"\n🎯 Confidence Thresholds: {CONFIDENCE_THRESHOLDS}")
    
    # Estimate time
    estimated_hours = len(MODELS_TO_TEST) * len(CONFIDENCE_THRESHOLDS) * 0.05  # ~3 minutes per test
    print(f"\n⏱️  Estimated Time: {estimated_hours:.1f} hours")
    
    # Auto-proceed with testing
    print("\n" + "=" * 60)
    print("🚀 Starting comprehensive testing automatically...")
    
    try:
        # Initialize tester with optimization
        tester = ModelComparisonTester(regenerate_embeddings=False)
        
        # Run complete comparison with optimization
        results = tester.run_complete_comparison_optimized()
        
        # Display summary
        print("\n🎉 TESTING COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        
        matrix_data = results['matrix_data']
        stats = matrix_data['statistics']
        
        print("\n📊 QUICK SUMMARY:")
        print("-" * 30)
        
        # Best overall performance
        best_overall = max(MODELS_TO_TEST, key=lambda m: stats[m]['max_success_rate'])
        best_score = stats[best_overall]['max_success_rate']
        best_threshold = stats[best_overall]['best_threshold']
        
        print(f"🏆 Best Overall Model: {best_overall}")
        print(f"   Max Success Rate: {best_score:.1f}%")
        print(f"   Best Threshold: {best_threshold}")
        
        # Model rankings
        print(f"\n📈 Model Rankings (by max success rate):")
        sorted_models = sorted(MODELS_TO_TEST, key=lambda m: stats[m]['max_success_rate'], reverse=True)
        for i, model in enumerate(sorted_models, 1):
            max_rate = stats[model]['max_success_rate']
            avg_rate = stats[model]['avg_success_rate']
            print(f"   {i}. {model}: {max_rate:.1f}% (avg: {avg_rate:.1f}%)")
        
        # Threshold analysis
        print(f"\n🎯 Threshold Analysis:")
        for threshold in CONFIDENCE_THRESHOLDS:
            best_at_threshold = max(MODELS_TO_TEST, key=lambda m: matrix_data['matrix'][m][threshold])
            score_at_threshold = matrix_data['matrix'][best_at_threshold][threshold]
            print(f"   Threshold {threshold}: {best_at_threshold} ({score_at_threshold:.1f}%)")
        
        print(f"\n📁 Results saved to: results/ directory")
        print(f"📄 Check the generated files for detailed analysis")
        
    except KeyboardInterrupt:
        print("\n❌ Testing interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
