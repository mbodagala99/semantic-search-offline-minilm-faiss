#!/usr/bin/env python3
"""
Model Configuration for Healthcare Query Router Testing
Defines models and confidence thresholds for comprehensive comparison testing
"""

# Models to test for embedding generation (including alternative models)
MODELS_TO_TEST = [
    "bert-base-uncased",
    "all-MiniLM-L6-v2",
    "bert-large-uncased",
    "emilyalsentzer/Bio_ClinicalBERT",
    "dmis-lab/biobert-base-cased-v1.1"
]

# Confidence thresholds from 0.0 to 1.0 with 0.1 increments (focused on 0.8+ range)
CONFIDENCE_THRESHOLDS = [0.6, 0.7, 0.8, 0.9, 1.0]

# Test parameters
TEST_PARAMETERS = {
    "num_queries": 120,
    "output_formats": ["csv", "json", "html"],
    "save_individual_results": True,
    "results_directory": "results",
    "individual_results_directory": "individual_model_results"
}

# Model descriptions for reporting
MODEL_DESCRIPTIONS = {
    "bert-base-uncased": "BERT Base Uncased (768 dimensions)",
    "all-MiniLM-L6-v2": "MiniLM L6 v2 (384 dimensions)", 
    "bert-large-uncased": "BERT Large Uncased (1024 dimensions)",
    "emilyalsentzer/Bio_ClinicalBERT": "Bio ClinicalBERT (768 dimensions)",
    "dmis-lab/biobert-base-cased-v1.1": "BioBERT Base Cased v1.1 (768 dimensions)"
}

# Output file naming patterns
OUTPUT_PATTERNS = {
    "matrix_csv": "model_comparison_matrix_{timestamp}.csv",
    "matrix_json": "model_comparison_matrix_{timestamp}.json",
    "matrix_html": "model_performance_analysis_{timestamp}.html",
    "individual_results": "model_{model_name}_results_{timestamp}.json",
    "summary_report": "model_comparison_summary_{timestamp}.txt"
}
