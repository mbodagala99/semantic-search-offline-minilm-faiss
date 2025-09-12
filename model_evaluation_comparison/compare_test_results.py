#!/usr/bin/env python3
"""
Compare test results before and after index enhancement
"""

import json
from datetime import datetime

def compare_test_results():
    """Compare test results before and after enhancement."""
    
    # Load original results
    with open('healthcare_router_test_results_20250910_082843.json', 'r') as f:
        original_results = json.load(f)
    
    # Load enhanced results
    with open('healthcare_router_test_results_20250910_084243.json', 'r') as f:
        enhanced_results = json.load(f)
    
    print("🔍 Test Results Comparison: Before vs After Enhancement")
    print("=" * 60)
    
    # Overall comparison
    print(f"📊 Overall Results:")
    print(f"   Original Success Rate: {original_results['success_rate']:.1f}%")
    print(f"   Enhanced Success Rate: {enhanced_results['success_rate']:.1f}%")
    print(f"   Change: {enhanced_results['success_rate'] - original_results['success_rate']:+.1f}%")
    
    # Detailed comparison
    improvements = []
    degradations = []
    unchanged = []
    
    for i, (orig, enh) in enumerate(zip(original_results['results'], enhanced_results['results'])):
        orig_conf = orig['confidence_score']
        enh_conf = enh['confidence_score']
        diff = enh_conf - orig_conf
        
        if abs(diff) < 0.01:  # Essentially unchanged
            unchanged.append({
                'test_number': i + 1,
                'query': orig['query'][:60] + "...",
                'original': orig_conf,
                'enhanced': enh_conf,
                'difference': diff
            })
        elif diff > 0.01:  # Improved
            improvements.append({
                'test_number': i + 1,
                'query': orig['query'][:60] + "...",
                'original': orig_conf,
                'enhanced': enh_conf,
                'difference': diff
            })
        else:  # Degraded
            degradations.append({
                'test_number': i + 1,
                'query': orig['query'][:60] + "...",
                'original': orig_conf,
                'enhanced': enh_conf,
                'difference': diff
            })
    
    print(f"\n📈 Improvements: {len(improvements)} queries")
    print(f"📉 Degradations: {len(degradations)} queries")
    print(f"➡️  Unchanged: {len(unchanged)} queries")
    
    # Show top improvements
    if improvements:
        print(f"\n🎯 Top 10 Improvements:")
        print("-" * 40)
        sorted_improvements = sorted(improvements, key=lambda x: x['difference'], reverse=True)
        for i, imp in enumerate(sorted_improvements[:10], 1):
            print(f"{i:2d}. Test {imp['test_number']:3d}: {imp['difference']:+.3f} ({imp['original']:.3f} → {imp['enhanced']:.3f})")
            print(f"    Query: {imp['query']}")
    
    # Show top degradations
    if degradations:
        print(f"\n⚠️  Top 10 Degradations:")
        print("-" * 40)
        sorted_degradations = sorted(degradations, key=lambda x: x['difference'])
        for i, deg in enumerate(sorted_degradations[:10], 1):
            print(f"{i:2d}. Test {deg['test_number']:3d}: {deg['difference']:+.3f} ({deg['original']:.3f} → {deg['enhanced']:.3f})")
            print(f"    Query: {deg['query']}")
    
    # Analyze confidence score distribution
    print(f"\n📊 Confidence Score Distribution Analysis:")
    print("-" * 50)
    
    # Original distribution
    orig_high = sum(1 for r in original_results['results'] if r['confidence_score'] >= 0.5)
    orig_medium = sum(1 for r in original_results['results'] if 0.3 <= r['confidence_score'] < 0.5)
    orig_low = sum(1 for r in original_results['results'] if r['confidence_score'] < 0.3)
    
    # Enhanced distribution
    enh_high = sum(1 for r in enhanced_results['results'] if r['confidence_score'] >= 0.5)
    enh_medium = sum(1 for r in enhanced_results['results'] if 0.3 <= r['confidence_score'] < 0.5)
    enh_low = sum(1 for r in enhanced_results['results'] if r['confidence_score'] < 0.3)
    
    print(f"High Confidence (≥0.5):")
    print(f"   Original: {orig_high:3d} ({orig_high/120*100:5.1f}%)")
    print(f"   Enhanced: {enh_high:3d} ({enh_high/120*100:5.1f}%)")
    print(f"   Change:   {enh_high-orig_high:+3d} ({(enh_high-orig_high)/120*100:+.1f}%)")
    
    print(f"\nMedium Confidence (0.3-0.49):")
    print(f"   Original: {orig_medium:3d} ({orig_medium/120*100:5.1f}%)")
    print(f"   Enhanced: {enh_medium:3d} ({enh_medium/120*100:5.1f}%)")
    print(f"   Change:   {enh_medium-orig_medium:+3d} ({(enh_medium-orig_medium)/120*100:+.1f}%)")
    
    print(f"\nLow Confidence (<0.3):")
    print(f"   Original: {orig_low:3d} ({orig_low/120*100:5.1f}%)")
    print(f"   Enhanced: {enh_low:3d} ({enh_low/120*100:5.1f}%)")
    print(f"   Change:   {enh_low-orig_low:+3d} ({(enh_low-orig_low)/120*100:+.1f}%)")
    
    # Average confidence scores
    orig_avg = sum(r['confidence_score'] for r in original_results['results']) / len(original_results['results'])
    enh_avg = sum(r['confidence_score'] for r in enhanced_results['results']) / len(enhanced_results['results'])
    
    print(f"\n📈 Average Confidence Scores:")
    print(f"   Original: {orig_avg:.3f}")
    print(f"   Enhanced: {enh_avg:.3f}")
    print(f"   Change:   {enh_avg-orig_avg:+.3f}")
    
    # Save comparison results
    comparison_data = {
        'comparison_date': datetime.now().isoformat(),
        'original_results': {
            'success_rate': original_results['success_rate'],
            'high_confidence': orig_high,
            'medium_confidence': orig_medium,
            'low_confidence': orig_low,
            'average_confidence': orig_avg
        },
        'enhanced_results': {
            'success_rate': enhanced_results['success_rate'],
            'high_confidence': enh_high,
            'medium_confidence': enh_medium,
            'low_confidence': enh_low,
            'average_confidence': enh_avg
        },
        'changes': {
            'success_rate_change': enhanced_results['success_rate'] - original_results['success_rate'],
            'high_confidence_change': enh_high - orig_high,
            'medium_confidence_change': enh_medium - orig_medium,
            'low_confidence_change': enh_low - orig_low,
            'average_confidence_change': enh_avg - orig_avg
        },
        'detailed_changes': {
            'improvements': improvements,
            'degradations': degradations,
            'unchanged': unchanged
        }
    }
    
    with open('test_results_comparison.json', 'w') as f:
        json.dump(comparison_data, f, indent=2)
    
    print(f"\n💾 Comparison results saved to: test_results_comparison.json")
    
    # Analysis and recommendations
    print(f"\n🔍 Analysis and Recommendations:")
    print("-" * 40)
    
    if enhanced_results['success_rate'] == original_results['success_rate']:
        print("❌ No improvement in success rate after enhancement")
        print("   Possible reasons:")
        print("   1. The semantic similarity model may not be finding matches with the new content")
        print("   2. The new use cases may be too generic and not specific enough")
        print("   3. The embedding model may need fine-tuning for healthcare domain")
        print("   4. The confidence threshold of 0.5 may be too high")
        
        print("\n💡 Recommendations:")
        print("   1. Lower the confidence threshold to 0.4 or 0.3")
        print("   2. Add more specific healthcare terminology to the use cases")
        print("   3. Consider using a healthcare-specific embedding model")
        print("   4. Add more detailed scenarios with specific healthcare terms")
        print("   5. Test with a different similarity search approach")
    
    elif enhanced_results['success_rate'] > original_results['success_rate']:
        print("✅ Improvement detected in success rate")
        print(f"   Success rate increased by {enhanced_results['success_rate'] - original_results['success_rate']:.1f}%")
    
    else:
        print("⚠️  Degradation detected in success rate")
        print(f"   Success rate decreased by {original_results['success_rate'] - enhanced_results['success_rate']:.1f}%")

if __name__ == "__main__":
    compare_test_results()
