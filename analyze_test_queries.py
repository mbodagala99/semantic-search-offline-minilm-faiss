#!/usr/bin/env python3
"""
Analyze test queries and categorize them for index enhancement
"""

import json
import re
from collections import defaultdict

def categorize_query(query_text, description):
    """Categorize a query as claims-related, provider-related, or both."""
    
    # Keywords that indicate claims domain
    claims_keywords = [
        'claim', 'claims', 'payment', 'billing', 'reimbursement', 'denied', 'approved',
        'submitted', 'processed', 'rejected', 'paid', 'outstanding', 'pending',
        'fraud', 'duplicate', 'adjustment', 'reconciliation', 'remittance',
        'cpt', 'drg', 'procedure code', 'diagnosis code', 'icd', 'hcpcs',
        'eligibility', 'authorization', 'prior auth', 'coverage', 'benefit',
        'copay', 'deductible', 'coinsurance', 'out-of-pocket', 'liability',
        'clearinghouse', 'edi', '835', '837', 'paper claim', 'electronic claim',
        'appeal', 'grievance', 'retroactive', 'correction', 'revision',
        'pharmacy', 'prescription', 'drug', 'medication', 'formulary',
        'inpatient', 'outpatient', 'emergency', 'er', 'urgent care',
        'surgery', 'procedure', 'treatment', 'therapy', 'diagnostic',
        'lab', 'laboratory', 'imaging', 'radiology', 'mri', 'ct', 'x-ray',
        'anesthesia', 'pathology', 'cardiology', 'oncology', 'orthopedic',
        'behavioral health', 'mental health', 'substance abuse',
        'maternity', 'obstetrics', 'gynecology', 'pediatric', 'neonatal',
        'hospice', 'palliative', 'home health', 'skilled nursing',
        'telehealth', 'telemedicine', 'virtual care', 'remote monitoring',
        'transplant', 'organ', 'tissue', 'blood', 'plasma',
        'covid', 'pandemic', 'infectious disease', 'vaccination',
        'chronic condition', 'diabetes', 'hypertension', 'heart disease',
        'cancer', 'tumor', 'malignancy', 'benign', 'metastasis',
        'readmission', 'discharge', 'admission', 'length of stay',
        'catastrophic', 'high-cost', 'expensive', 'outlier', 'anomaly',
        'brand', 'generic', 'controlled substance', 'narcotic', 'opioid',
        'weekend', 'holiday', 'after hours', 'on-call', 'emergency',
        'rural', 'urban', 'metropolitan', 'county', 'state', 'region',
        'hmo', 'ppo', 'epo', 'pos', 'medicare', 'medicaid', 'commercial',
        'tier', 'network', 'in-network', 'out-of-network', 'par', 'non-par',
        'capitation', 'fee-for-service', 'bundled payment', 'value-based',
        'quality measure', 'performance', 'outcome', 'satisfaction',
        'readmission rate', 'mortality rate', 'infection rate', 'complication',
        'patient safety', 'adverse event', 'medical error', 'near miss',
        'utilization', 'volume', 'frequency', 'trend', 'pattern', 'analysis',
        'report', 'summary', 'breakdown', 'distribution', 'ranking', 'top',
        'highest', 'lowest', 'average', 'median', 'percentile', 'quartile',
        'year', 'month', 'quarter', 'week', 'day', 'date', 'time', 'period',
        '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025',
        'january', 'february', 'march', 'april', 'may', 'june',
        'july', 'august', 'september', 'october', 'november', 'december',
        'q1', 'q2', 'q3', 'q4', 'first quarter', 'second quarter',
        'third quarter', 'fourth quarter', 'first half', 'second half',
        'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'
    ]
    
    # Keywords that indicate provider domain
    provider_keywords = [
        'provider', 'providers', 'physician', 'doctor', 'nurse', 'practitioner',
        'specialist', 'specialty', 'specialties', 'credential', 'credentialing',
        'license', 'licensing', 'npi', 'taxonomy', 'board certified',
        'facility', 'hospital', 'clinic', 'medical center', 'health system',
        'group practice', 'individual practice', 'solo practice',
        'network', 'directory', 'roster', 'panel', 'staff',
        'recruitment', 'enrollment', 'onboarding', 'termination',
        'performance', 'quality', 'outcome', 'satisfaction', 'rating',
        'volume', 'capacity', 'utilization', 'workload', 'productivity',
        'geographic', 'location', 'address', 'city', 'state', 'zip',
        'rural', 'urban', 'metropolitan', 'county', 'region', 'area',
        'availability', 'schedule', 'appointment', 'wait time', 'access',
        'accepting', 'new patients', 'closed panel', 'open panel',
        'referral', 'consultation', 'collaboration', 'partnership',
        'affiliation', 'membership', 'association', 'organization',
        'contract', 'agreement', 'fee schedule', 'reimbursement rate',
        'acceptance rate', 'denial rate', 'appeal rate', 'grievance rate',
        'malpractice', 'insurance', 'liability', 'risk', 'safety',
        'disciplinary', 'sanction', 'violation', 'complaint', 'investigation',
        'peer review', 'quality review', 'audit', 'assessment', 'evaluation',
        'continuing education', 'cme', 'training', 'certification',
        'expired', 'expiring', 'renewal', 'update', 'current', 'active',
        'inactive', 'suspended', 'terminated', 'resigned', 'retired',
        'deceased', 'moved', 'relocated', 'changed', 'updated',
        'missing', 'incomplete', 'invalid', 'incorrect', 'mismatch',
        'duplicate', 'conflict', 'discrepancy', 'anomaly', 'outlier',
        'top', 'highest', 'lowest', 'best', 'worst', 'ranking', 'rank',
        'count', 'number', 'total', 'sum', 'average', 'mean', 'median',
        'percentage', 'rate', 'ratio', 'proportion', 'distribution',
        'trend', 'pattern', 'change', 'increase', 'decrease', 'growth',
        'decline', 'improvement', 'deterioration', 'stability',
        'comparison', 'benchmark', 'standard', 'target', 'goal',
        'threshold', 'limit', 'maximum', 'minimum', 'range', 'span',
        'zero', 'none', 'all', 'some', 'most', 'few', 'many', 'several'
    ]
    
    # Convert to lowercase for matching
    query_lower = query_text.lower()
    description_lower = description.lower()
    combined_text = f"{query_lower} {description_lower}"
    
    # Count keyword matches
    claims_score = sum(1 for keyword in claims_keywords if keyword in combined_text)
    provider_score = sum(1 for keyword in provider_keywords if keyword in combined_text)
    
    # Determine primary category
    if claims_score > provider_score:
        return "claims"
    elif provider_score > claims_score:
        return "providers"
    else:
        return "both"

def analyze_test_queries():
    """Analyze all test queries and categorize them."""
    
    # Load test results
    with open('healthcare_router_test_results_20250910_082843.json', 'r') as f:
        data = json.load(f)
    
    # Categorize queries
    claims_queries = []
    provider_queries = []
    both_queries = []
    
    for result in data['results']:
        query = result['query']
        description = result['description']
        confidence = result['confidence_score']
        
        category = categorize_query(query, description)
        
        query_info = {
            'query': query,
            'description': description,
            'confidence': confidence,
            'routing_status': result['routing_status']
        }
        
        if category == "claims":
            claims_queries.append(query_info)
        elif category == "providers":
            provider_queries.append(query_info)
        else:
            both_queries.append(query_info)
    
    # Print analysis
    print("🔍 Query Analysis Results:")
    print("=" * 50)
    print(f"Total Queries: {len(data['results'])}")
    print(f"Claims Queries: {len(claims_queries)}")
    print(f"Provider Queries: {len(provider_queries)}")
    print(f"Both Domain Queries: {len(both_queries)}")
    
    print(f"\n📊 Claims Queries ({len(claims_queries)}):")
    print("-" * 30)
    for i, q in enumerate(claims_queries[:10], 1):  # Show first 10
        print(f"{i:2d}. {q['description']}")
        print(f"    Query: {q['query'][:80]}...")
        print(f"    Confidence: {q['confidence']:.3f} - {q['routing_status']}")
        print()
    
    print(f"\n👥 Provider Queries ({len(provider_queries)}):")
    print("-" * 30)
    for i, q in enumerate(provider_queries[:10], 1):  # Show first 10
        print(f"{i:2d}. {q['description']}")
        print(f"    Query: {q['query'][:80]}...")
        print(f"    Confidence: {q['confidence']:.3f} - {q['routing_status']}")
        print()
    
    # Save categorized results
    analysis_results = {
        'total_queries': len(data['results']),
        'claims_queries': claims_queries,
        'provider_queries': provider_queries,
        'both_queries': both_queries,
        'summary': {
            'claims_count': len(claims_queries),
            'provider_count': len(provider_queries),
            'both_count': len(both_queries)
        }
    }
    
    with open('query_analysis_results.json', 'w') as f:
        json.dump(analysis_results, f, indent=2)
    
    print(f"\n💾 Analysis saved to: query_analysis_results.json")
    
    return analysis_results

if __name__ == "__main__":
    analyze_test_queries()
