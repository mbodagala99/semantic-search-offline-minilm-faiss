# Model Evaluation & Comparison

This directory contains all scripts and tools for evaluating and comparing different embedding models for healthcare semantic search.

## 📁 Directory Contents

### Core Evaluation Scripts
- **`model_comparison_tester.py`** - Main orchestrator for model comparison testing
- **`generate_comparison_matrix.py`** - Generates comparison matrices and reports
- **`test_healthcare_router_comprehensive.py`** - Comprehensive test suite with 120 healthcare queries
- **`model_config.py`** - Configuration for models and testing parameters

### Analysis Tools
- **`analyze_test_queries.py`** - Analyzes test query patterns and performance
- **`compare_test_results.py`** - Compares results across different model runs

### Configuration
- **`model_config.py`** - Models to test, confidence thresholds, and test parameters

## 🚀 Usage

### Run Complete Model Comparison
```bash
cd model_evaluation_comparison
python generate_comparison_matrix.py
```

### Test Specific Model
```bash
cd model_evaluation_comparison
python -c "
from model_comparison_tester import ModelComparisonTester
from embedding_generator import EmbeddingGenerator

# Test single model
tester = ModelComparisonTester(regenerate_embeddings=False)
result = tester.test_single_model_optimized('dmis-lab/biobert-base-cased-v1.1')
print(f'Success rate: {result[1]:.1f}%')
"
```

### Analyze Test Results
```bash
cd model_evaluation_comparison
python analyze_test_queries.py
```

## 📊 Models Tested

1. **dmis-lab/biobert-base-cased-v1.1** - BioBERT (Best Performance)
2. **bert-base-uncased** - BERT Base
3. **all-MiniLM-L6-v2** - MiniLM
4. **bert-large-uncased** - BERT Large
5. **emilyalsentzer/Bio_ClinicalBERT** - Clinical BERT

## 🎯 Performance Metrics

- **Success Rate**: Percentage of queries with confidence ≥ threshold
- **Confidence Thresholds**: 0.6, 0.7, 0.8, 0.9, 1.0
- **Test Queries**: 120 comprehensive healthcare queries
- **Caching**: Model-specific embedding caches in `../embeddings_cache/`

## 📈 Output Files

- **Comparison Matrix**: CSV and JSON formats
- **Individual Results**: Per-model detailed results
- **Summary Reports**: Performance analysis and recommendations

## 🔧 Configuration

Edit `model_config.py` to:
- Add/remove models for testing
- Adjust confidence thresholds
- Modify test parameters
- Change output formats

## 📝 Notes

- All scripts use the main configuration system (`../healthcare_search.config`)
- Embeddings are cached to avoid regeneration
- Results are automatically timestamped
- Supports both individual and batch testing
