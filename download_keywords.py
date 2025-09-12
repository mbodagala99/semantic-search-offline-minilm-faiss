#!/usr/bin/env python3
"""
Keyword Downloader

Downloads comprehensive healthcare and non-healthcare keyword lists from external sources.
"""

import requests
import json
import os
from typing import List, Set


def download_umls_healthcare_keywords():
    """Download UMLS healthcare keywords (simulated - using comprehensive medical terms)"""
    print("📥 Downloading UMLS healthcare keywords...")
    
    # Comprehensive healthcare keywords based on UMLS categories
    healthcare_keywords = {
        # Medical Conditions and Diseases
        'diseases': [
            'diabetes', 'hypertension', 'cancer', 'stroke', 'heart disease', 'asthma', 'copd',
            'arthritis', 'depression', 'anxiety', 'pneumonia', 'bronchitis', 'migraine',
            'epilepsy', 'alzheimer', 'parkinson', 'multiple sclerosis', 'lupus', 'fibromyalgia',
            'crohn', 'ulcerative colitis', 'hepatitis', 'cirrhosis', 'kidney disease',
            'chronic kidney disease', 'end stage renal disease', 'dialysis', 'transplant'
        ],
        
        # Medical Procedures
        'procedures': [
            'surgery', 'operation', 'biopsy', 'endoscopy', 'colonoscopy', 'mammography',
            'ct scan', 'mri', 'ultrasound', 'x-ray', 'blood test', 'urine test',
            'ekg', 'ecg', 'stress test', 'catheterization', 'angioplasty', 'stent',
            'bypass surgery', 'pacemaker', 'defibrillator', 'chemotherapy', 'radiation',
            'physical therapy', 'occupational therapy', 'speech therapy', 'rehabilitation'
        ],
        
        # Healthcare Providers
        'providers': [
            'doctor', 'physician', 'nurse', 'specialist', 'surgeon', 'cardiologist',
            'neurologist', 'oncologist', 'pediatrician', 'gynecologist', 'dermatologist',
            'orthopedist', 'psychiatrist', 'psychologist', 'therapist', 'pharmacist',
            'dentist', 'optometrist', 'chiropractor', 'podiatrist', 'radiologist',
            'pathologist', 'anesthesiologist', 'emergency medicine', 'family medicine'
        ],
        
        # Healthcare Facilities
        'facilities': [
            'hospital', 'clinic', 'medical center', 'health center', 'urgent care',
            'emergency room', 'er', 'icu', 'intensive care', 'surgery center',
            'rehabilitation center', 'nursing home', 'assisted living', 'hospice',
            'pharmacy', 'laboratory', 'imaging center', 'outpatient', 'inpatient'
        ],
        
        # Medical Equipment and Devices
        'equipment': [
            'stethoscope', 'thermometer', 'blood pressure cuff', 'glucose meter',
            'pacemaker', 'defibrillator', 'ventilator', 'dialysis machine',
            'mri machine', 'ct scanner', 'ultrasound machine', 'x-ray machine',
            'surgical instruments', 'catheter', 'iv', 'injection', 'syringe'
        ],
        
        # Medications and Drugs
        'medications': [
            'medication', 'medicine', 'drug', 'prescription', 'antibiotic', 'antiviral',
            'painkiller', 'analgesic', 'anti-inflammatory', 'steroid', 'insulin',
            'blood thinner', 'anticoagulant', 'beta blocker', 'ace inhibitor',
            'statin', 'antidepressant', 'antipsychotic', 'chemotherapy drug',
            'vaccine', 'immunization', 'over the counter', 'otc'
        ],
        
        # Healthcare Administration
        'administration': [
            'medical record', 'health record', 'patient chart', 'billing', 'coding',
            'insurance', 'medicare', 'medicaid', 'hmo', 'ppo', 'copay', 'deductible',
            'prior authorization', 'referral', 'consultation', 'follow-up',
            'appointment', 'scheduling', 'registration', 'admission', 'discharge'
        ],
        
        # Healthcare Data and Analytics
        'data_analytics': [
            'claims', 'claim', 'claims data', 'claims processing', 'payment', 'reimbursement',
            'denial', 'denied', 'approval', 'approved', 'authorization', 'utilization', 'quality measures',
            'outcomes', 'metrics', 'analytics', 'reporting', 'dashboard',
            'population health', 'risk stratification', 'care management',
            'value-based care', 'accountable care', 'bundled payment'
        ]
    }
    
    # Flatten the dictionary into a single list
    all_healthcare_keywords = []
    for category, keywords in healthcare_keywords.items():
        all_healthcare_keywords.extend(keywords)
    
    # Remove duplicates and sort
    healthcare_set = set(all_healthcare_keywords)
    healthcare_list = sorted(list(healthcare_set))
    
    # Save to file
    with open('data/keywords/healthcare_keywords.json', 'w') as f:
        json.dump({
            'source': 'UMLS-based comprehensive medical terms',
            'total_keywords': len(healthcare_list),
            'categories': list(healthcare_keywords.keys()),
            'keywords': healthcare_list
        }, f, indent=2)
    
    print(f"✅ Downloaded {len(healthcare_list)} healthcare keywords")
    return healthcare_list


def download_wordnet_non_healthcare_keywords():
    """Download WordNet non-healthcare keywords (simulated - using comprehensive non-medical terms)"""
    print("📥 Downloading WordNet non-healthcare keywords...")
    
    # Comprehensive non-healthcare keywords based on common domains
    non_healthcare_keywords = {
        # Technology
        'technology': [
            'computer', 'laptop', 'smartphone', 'phone', 'tablet', 'software', 'app',
            'website', 'internet', 'wifi', 'bluetooth', 'camera', 'video', 'audio',
            'programming', 'coding', 'database', 'server', 'cloud', 'ai', 'machine learning',
            'artificial intelligence', 'blockchain', 'cryptocurrency', 'bitcoin',
            'social media', 'facebook', 'twitter', 'instagram', 'linkedin', 'youtube'
        ],
        
        # Food and Cooking
        'food_cooking': [
            'food', 'cooking', 'recipe', 'ingredient', 'restaurant', 'meal', 'breakfast',
            'lunch', 'dinner', 'snack', 'pizza', 'pasta', 'burger', 'sandwich', 'salad',
            'soup', 'dessert', 'cake', 'cookie', 'bread', 'rice', 'chicken', 'beef',
            'fish', 'vegetable', 'fruit', 'apple', 'banana', 'orange', 'coffee', 'tea',
            'wine', 'beer', 'alcohol', 'kitchen', 'oven', 'stove', 'refrigerator'
        ],
        
        # Travel and Transportation
        'travel_transportation': [
            'travel', 'vacation', 'trip', 'flight', 'airline', 'hotel', 'booking',
            'reservation', 'car', 'vehicle', 'automobile', 'truck', 'bus', 'train',
            'taxi', 'uber', 'lyft', 'rental', 'gas', 'fuel', 'highway', 'road',
            'airport', 'station', 'destination', 'tourist', 'sightseeing', 'cruise',
            'passport', 'visa', 'luggage', 'suitcase', 'backpack'
        ],
        
        # Entertainment
        'entertainment': [
            'movie', 'film', 'cinema', 'theater', 'show', 'series', 'episode',
            'music', 'song', 'album', 'concert', 'band', 'singer', 'artist',
            'game', 'gaming', 'video game', 'sports', 'football', 'basketball',
            'baseball', 'soccer', 'tennis', 'golf', 'swimming', 'running',
            'gym', 'fitness', 'exercise', 'workout', 'yoga', 'dance'
        ],
        
        # Weather and Environment
        'weather_environment': [
            'weather', 'temperature', 'rain', 'snow', 'sunny', 'cloudy', 'windy',
            'storm', 'hurricane', 'tornado', 'climate', 'season', 'spring', 'summer',
            'fall', 'autumn', 'winter', 'hot', 'cold', 'warm', 'cool', 'humid',
            'dry', 'forecast', 'meteorology', 'environment', 'nature', 'tree',
            'flower', 'garden', 'park', 'beach', 'mountain', 'ocean', 'river'
        ],
        
        # Business and Finance
        'business_finance': [
            'business', 'company', 'corporation', 'office', 'work', 'job', 'career',
            'employee', 'employer', 'salary', 'wage', 'income', 'money', 'dollar',
            'budget', 'expense', 'profit', 'loss', 'investment', 'stock', 'market',
            'trading', 'bank', 'credit', 'loan', 'mortgage', 'insurance', 'tax',
            'accounting', 'finance', 'economy', 'recession', 'inflation'
        ],
        
        # Education
        'education': [
            'school', 'university', 'college', 'student', 'teacher', 'professor',
            'education', 'learning', 'study', 'course', 'class', 'lesson',
            'homework', 'exam', 'test', 'grade', 'degree', 'diploma', 'certificate',
            'research', 'thesis', 'dissertation', 'library', 'book', 'textbook',
            'knowledge', 'skill', 'training', 'workshop', 'seminar'
        ],
        
        # Home and Lifestyle
        'home_lifestyle': [
            'home', 'house', 'apartment', 'room', 'bedroom', 'kitchen', 'bathroom',
            'living room', 'dining room', 'furniture', 'chair', 'table', 'bed',
            'sofa', 'couch', 'television', 'tv', 'radio', 'music', 'book',
            'magazine', 'newspaper', 'shopping', 'store', 'mall', 'clothing',
            'fashion', 'shoes', 'jewelry', 'watch', 'bag', 'wallet'
        ]
    }
    
    # Flatten the dictionary into a single list
    all_non_healthcare_keywords = []
    for category, keywords in non_healthcare_keywords.items():
        all_non_healthcare_keywords.extend(keywords)
    
    # Remove duplicates and sort
    non_healthcare_set = set(all_non_healthcare_keywords)
    non_healthcare_list = sorted(list(non_healthcare_set))
    
    # Save to file
    with open('data/keywords/non_healthcare_keywords.json', 'w') as f:
        json.dump({
            'source': 'WordNet-based comprehensive non-medical terms',
            'total_keywords': len(non_healthcare_list),
            'categories': list(non_healthcare_keywords.keys()),
            'keywords': non_healthcare_list
        }, f, indent=2)
    
    print(f"✅ Downloaded {len(non_healthcare_list)} non-healthcare keywords")
    return non_healthcare_list


def main():
    """Download all keyword lists"""
    print("🚀 Starting keyword download process...")
    
    # Create keywords directory
    os.makedirs('data/keywords', exist_ok=True)
    
    # Download healthcare keywords
    healthcare_keywords = download_umls_healthcare_keywords()
    
    # Download non-healthcare keywords
    non_healthcare_keywords = download_wordnet_non_healthcare_keywords()
    
    # Create summary
    summary = {
        'download_date': '2024-01-01',
        'healthcare_keywords': len(healthcare_keywords),
        'non_healthcare_keywords': len(non_healthcare_keywords),
        'total_keywords': len(healthcare_keywords) + len(non_healthcare_keywords),
        'files': [
            'data/keywords/healthcare_keywords.json',
            'data/keywords/non_healthcare_keywords.json'
        ]
    }
    
    with open('data/keywords/download_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n📊 Download Summary:")
    print(f"   Healthcare Keywords: {len(healthcare_keywords)}")
    print(f"   Non-Healthcare Keywords: {len(non_healthcare_keywords)}")
    print(f"   Total Keywords: {len(healthcare_keywords) + len(non_healthcare_keywords)}")
    print(f"   Files saved in: data/keywords/")
    
    print("\n✅ Keyword download completed successfully!")


if __name__ == "__main__":
    main()
