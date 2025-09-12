#!/usr/bin/env python3
"""
Embedding Generation Logic for Healthcare Claims and Provider Indexes
Generates embeddings from use_cases and reports_generated sections
"""

import json
import os
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from sentence_transformers import SentenceTransformer
import faiss
from config_reader import config

class EmbeddingDataGenerator:
    """Handles text processing and data preparation for embeddings"""
    
    def __init__(self):
        # Get the project root directory (same directory as current file)
        project_root = os.path.dirname(os.path.abspath(__file__))
        self.claims_index_file = os.path.join(project_root, "data/opensearch/claims_index_mapping_expanded.json")
        self.providers_index_file = os.path.join(project_root, "data/opensearch/providers_index_mapping_expanded.json")
    
    def load_index_metadata(self, file_path: str) -> Dict[str, Any]:
        """Load index metadata from JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Error: File {file_path} not found")
            return {}
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in {file_path}")
            return {}
    
    def combine_text_fields(self, use_case: Dict[str, Any]) -> str:
        """Combine use case fields into a single text string"""
        text_parts = []
        
        # Add category
        if 'category' in use_case:
            text_parts.append(f"Category: {use_case['category']}")
        
        # Add description
        if 'description' in use_case:
            text_parts.append(f"Description: {use_case['description']}")
        
        # Add scenarios
        if 'scenarios' in use_case and isinstance(use_case['scenarios'], list):
            scenarios_text = "Scenarios: " + "; ".join(use_case['scenarios'])
            text_parts.append(scenarios_text)
        
        # Add natural language prompts
        if 'natural_language_prompts' in use_case and isinstance(use_case['natural_language_prompts'], list):
            prompts_text = "Natural Language Prompts: " + "; ".join(use_case['natural_language_prompts'])
            text_parts.append(prompts_text)
        
        return " | ".join(text_parts)
    
    def combine_report_fields(self, report: Dict[str, Any]) -> str:
        """Combine report fields into a single text string"""
        text_parts = []
        
        # Add report type
        if 'report_type' in report:
            text_parts.append(f"Report Type: {report['report_type']}")
        
        # Add description
        if 'description' in report:
            text_parts.append(f"Description: {report['description']}")
        
        # Add report categories
        if 'report_categories' in report and isinstance(report['report_categories'], list):
            for category in report['report_categories']:
                category_text = f"Category: {category.get('category', '')}"
                if 'description' in category:
                    category_text += f" - {category['description']}"
                if 'sample_prompts' in category and isinstance(category['sample_prompts'], list):
                    category_text += f" | Sample Prompts: {'; '.join(category['sample_prompts'])}"
                if 'filters' in category and isinstance(category['filters'], list):
                    category_text += f" | Filters: {'; '.join(category['filters'])}"
                text_parts.append(category_text)
        
        return " | ".join(text_parts)
    
    def generate_use_case_data(self, index_metadata: Dict[str, Any], index_name: str) -> List[Dict[str, str]]:
        """Generate data for use case embeddings"""
        data_list = []
        
        if '_meta' not in index_metadata or 'use_cases' not in index_metadata['_meta']:
            return data_list
        
        use_cases = index_metadata['_meta']['use_cases']
        organization_name = index_metadata['_meta'].get('organization_name', 'Healthcare Organization')
        
        for use_case in use_cases:
            text_content = self.combine_text_fields(use_case)
            
            data_item = {
                "text": text_content,
                "source_index": index_name,
                "organization": organization_name
            }
            
            data_list.append(data_item)
        
        return data_list
    
    def generate_report_data(self, index_metadata: Dict[str, Any], index_name: str) -> List[Dict[str, str]]:
        """Generate data for report embeddings"""
        data_list = []
        
        if '_meta' not in index_metadata or 'reports_generated' not in index_metadata['_meta']:
            return data_list
        
        reports = index_metadata['_meta']['reports_generated']
        organization_name = index_metadata['_meta'].get('organization_name', 'Healthcare Organization')
        
        for report in reports:
            text_content = self.combine_report_fields(report)
            
            data_item = {
                "text": text_content,
                "source_index": index_name,
                "organization": organization_name
            }
            
            data_list.append(data_item)
        
        return data_list
    
    def generate_all_data(self) -> List[Dict[str, str]]:
        """Generate all data for both indexes as a flat list"""
        all_data = []
        
        # Load claims index metadata
        claims_metadata = self.load_index_metadata(self.claims_index_file)
        if claims_metadata:
            claims_index_name = claims_metadata.get('_meta', {}).get('index_name', 'healthcare_claims_index')
            
            # Generate use case data
            claims_use_cases = self.generate_use_case_data(claims_metadata, claims_index_name)
            all_data.extend(claims_use_cases)
            
            # Generate report data
            claims_reports = self.generate_report_data(claims_metadata, claims_index_name)
            all_data.extend(claims_reports)
        
        # Load providers index metadata
        providers_metadata = self.load_index_metadata(self.providers_index_file)
        if providers_metadata:
            providers_index_name = providers_metadata.get('_meta', {}).get('index_name', 'healthcare_providers_index')
            
            # Generate use case data
            providers_use_cases = self.generate_use_case_data(providers_metadata, providers_index_name)
            all_data.extend(providers_use_cases)
            
            # Generate report data
            providers_reports = self.generate_report_data(providers_metadata, providers_index_name)
            all_data.extend(providers_reports)
        
        return all_data

class EmbeddingVectorGenerator:
    """Handles actual embedding vector generation using sentence-transformers"""
    
    def __init__(self, model_name: str = None):
        # Use configuration if no model specified
        self.model_name = model_name or config.get_primary_model()
        self.model = None
        self.normalize_vectors = config.is_vector_normalization_enabled()
        self.preprocess_text = config.is_text_preprocessing_enabled()
        self._load_model()
    
    def _load_model(self):
        """Load the sentence transformer model"""
        try:
            print(f"Loading embedding model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            print("Model loaded successfully!")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None
    
    def preprocess_text_for_embedding(self, text: str) -> str:
        """Preprocess text for better embedding quality"""
        if not self.preprocess_text:
            return text
        
        # Remove excessive whitespace
        import re
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Expand healthcare abbreviations
        abbreviations = {
            'ER': 'emergency room',
            'NPI': 'national provider identifier',
            'CPT': 'current procedural terminology',
            'DRG': 'diagnosis related group',
            'HMO': 'health maintenance organization',
            'PPO': 'preferred provider organization'
        }
        
        for abbr, full in abbreviations.items():
            text = text.replace(abbr, f"{abbr} ({full})")
        
        # Add context markers for better semantic understanding
        if 'claim' in text.lower():
            text = f"healthcare claims analysis: {text}"
        elif 'provider' in text.lower():
            text = f"healthcare provider management: {text}"
        
        return text
    
    def generate_embedding_vector(self, text: str) -> List[float]:
        """Generate embedding vector for given text using the loaded model"""
        if self.model is None:
            print("Warning: Model not loaded, returning empty embedding")
            return []
        
        try:
            # Preprocess text if enabled
            processed_text = self.preprocess_text_for_embedding(text)
            
            # Generate embedding vector
            embedding = self.model.encode(processed_text, convert_to_tensor=False)
            
            # Normalize vectors if enabled
            if self.normalize_vectors:
                embedding = embedding / np.linalg.norm(embedding)
            
            return embedding.tolist()
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return []
    
    def generate_embeddings_for_data(self, data_list: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """Generate embedding vectors for a list of data items"""
        embeddings = []
        
        for data_item in data_list:
            text = data_item.get('text', '')
            embedding_vector = self.generate_embedding_vector(text)
            
            embedding_item = {
                "text": data_item.get('text', ''),
                "embedding": embedding_vector,
                "source_index": data_item.get('source_index', ''),
                "organization": data_item.get('organization', '')
            }
            
            embeddings.append(embedding_item)
        
        return embeddings

class EmbeddingGenerator:
    """Main orchestrator class that coordinates data generation and vector generation"""
    
    def __init__(self, model_name: str = None):
        # Use configuration if no model specified
        self.model_name = model_name or config.get_primary_model()
        self.data_generator = EmbeddingDataGenerator()
        self.vector_generator = EmbeddingVectorGenerator(self.model_name)
        self.index_directory = config.get_index_directory()
        self.cache_directory = config.get_cache_directory()
    
    def generate_all_embeddings(self) -> List[Dict[str, Any]]:
        """Generate all embeddings for both indexes as a flat list"""
        # First, generate all the data using the data generator
        all_data = self.data_generator.generate_all_data()
        
        # Then, generate embeddings for all data using the vector generator
        all_embeddings = self.vector_generator.generate_embeddings_for_data(all_data)
        
        return all_embeddings
    
    def save_embeddings_to_file(self, embeddings: List[Dict[str, Any]], output_file: str = "generated_embeddings.json"):
        """Save embeddings to JSON file"""
        try:
            with open(output_file, 'w', encoding='utf-8') as file:
                json.dump(embeddings, file, indent=2, ensure_ascii=False)
            print(f"Embeddings saved to {output_file}")
        except Exception as e:
            print(f"Error saving embeddings: {e}")
    
    def print_embedding_summary(self, embeddings: List[Dict[str, Any]]):
        """Print summary of generated embeddings"""
        print("\n" + "="*60)
        print("EMBEDDING GENERATION SUMMARY")
        print("="*60)
        
        total_embeddings = len(embeddings)
        
        # Count by source index
        index_counts = {}
        for embedding in embeddings:
            source_index = embedding.get('source_index', 'unknown')
            index_counts[source_index] = index_counts.get(source_index, 0) + 1
        
        for index_name, count in index_counts.items():
            print(f"{index_name.replace('_', ' ').title()}: {count} embeddings")
        
        print(f"\nTotal Embeddings Generated: {total_embeddings}")
        print("="*60)
    
    def print_sample_embeddings(self, embeddings: List[Dict[str, Any]], max_samples: int = 2):
        """Print sample embeddings for review"""
        print("\n" + "="*60)
        print("SAMPLE EMBEDDINGS")
        print("="*60)
        
        if embeddings:
            print(f"\nShowing {min(max_samples, len(embeddings))} sample embeddings:")
            print("-" * 40)
            
            for i, embedding in enumerate(embeddings[:max_samples]):
                print(f"\nSample {i+1}:")
                print(f"Source Index: {embedding['source_index']}")
                print(f"Organization: {embedding['organization']}")
                print(f"Text Preview: {embedding['text'][:200]}...")
                if 'embedding' in embedding and embedding['embedding']:
                    print(f"Embedding Vector: {len(embedding['embedding'])} dimensions")
                    print(f"First 5 values: {embedding['embedding'][:5]}")
                else:
                    print("Embedding Vector: Not generated")
                print("-" * 40)
    
    def generate_all_embeddings_for_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Generate all embeddings for a specific file"""
        # Load file metadata
        metadata = self.data_generator.load_index_metadata(file_path)
        if not metadata:
            print(f"Error: Could not load metadata from {file_path}")
            return []
        
        # Get index name and organization
        index_name = metadata.get('_meta', {}).get('index_name', 'unknown_index')
        organization = metadata.get('_meta', {}).get('organization_name', 'Healthcare Organization')
        
        embeddings = []
        
        # Generate use case embeddings
        use_cases = metadata.get('_meta', {}).get('use_cases', [])
        for use_case in use_cases:
            text_content = self.data_generator.combine_text_fields(use_case)
            embedding_vector = self.vector_generator.generate_embedding_vector(text_content)
            
            embedding_data = {
                "text": text_content,
                "embedding": embedding_vector,
                "source_index": index_name,
                "organization": organization,
                "type": "use_case"
            }
            embeddings.append(embedding_data)
        
        # Generate report embeddings
        reports = metadata.get('_meta', {}).get('reports_generated', [])
        for report in reports:
            text_content = self.data_generator.combine_report_fields(report)
            embedding_vector = self.vector_generator.generate_embedding_vector(text_content)
            
            embedding_data = {
                "text": text_content,
                "embedding": embedding_vector,
                "source_index": index_name,
                "organization": organization,
                "type": "report"
            }
            embeddings.append(embedding_data)
        
        return embeddings
    
    def create_file_index(self, file_path: str, output_path: Optional[str] = None) -> bool:
        """Create FAISS index for a single file"""
        try:
            print(f"Creating index for file: {file_path}")
            
            # Generate embeddings for the file
            embeddings = self.generate_all_embeddings_for_file(file_path)
            if not embeddings:
                print(f"Error: No embeddings generated for {file_path}")
                return False
            
            # Extract embedding vectors and metadata
            vectors = []
            metadata = []
            
            for i, embedding in enumerate(embeddings):
                if embedding.get('embedding'):
                    vectors.append(embedding['embedding'])
                    metadata.append({
                        "id": i,
                        "text": embedding.get('text', ''),
                        "source_index": embedding.get('source_index', ''),
                        "organization": embedding.get('organization', ''),
                        "type": embedding.get('type', '')
                    })
            
            if not vectors:
                print("Error: No valid embedding vectors found")
                return False
            
            # Create FAISS index
            dimension = len(vectors[0])
            index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
            
            # Normalize vectors for cosine similarity
            vectors_array = np.array(vectors, dtype=np.float32)
            faiss.normalize_L2(vectors_array)
            
            # Add vectors to index
            index.add(vectors_array)
            
            # Determine output paths
            if output_path is None:
                file_name = os.path.splitext(os.path.basename(file_path))[0]
                output_path = f"indexes/{file_name}"
            
            # Save FAISS index
            faiss.write_index(index, f"{output_path}.faiss")
            
            # Save metadata
            with open(f"{output_path}.json", 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            print(f"Index created successfully: {output_path}.faiss")
            print(f"Metadata saved: {output_path}.json")
            print(f"Total embeddings: {len(vectors)}")
            
            return True
            
        except Exception as e:
            print(f"Error creating index for {file_path}: {e}")
            return False
    
    def search_file_index(self, file_path: str, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search specific file index"""
        try:
            # Determine index paths
            file_name = os.path.splitext(os.path.basename(file_path))[0]
            index_path = f"indexes/{file_name}.faiss"
            metadata_path = f"indexes/{file_name}.json"
            
            # Check if index exists
            if not os.path.exists(index_path) or not os.path.exists(metadata_path):
                print(f"Error: Index not found for {file_path}")
                print(f"Please create index first using create_file_index()")
                return []
            
            # Load FAISS index
            index = faiss.read_index(index_path)
            
            # Load metadata
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            # Generate query embedding
            query_embedding = self.vector_generator.generate_embedding_vector(query)
            if not query_embedding:
                print("Error: Could not generate query embedding")
                return []
            
            # Normalize query vector
            query_array = np.array([query_embedding], dtype=np.float32)
            faiss.normalize_L2(query_array)
            
            # Search
            scores, indices = index.search(query_array, min(top_k, len(metadata)))
            
            # Format results
            results = []
            for score, idx in zip(scores[0], indices[0]):
                if idx < len(metadata):
                    result = {
                        "similarity_score": float(score),
                        "text": metadata[idx]["text"],
                        "source_index": metadata[idx]["source_index"],
                        "organization": metadata[idx]["organization"],
                        "type": metadata[idx]["type"]
                    }
                    results.append(result)
            
            return results
            
        except Exception as e:
            print(f"Error searching index for {file_path}: {e}")
            return []
    
    def list_file_indexes(self) -> List[str]:
        """List all available file indexes"""
        indexes = []
        indexes_dir = "indexes"
        
        if not os.path.exists(indexes_dir):
            return indexes
        
        for file in os.listdir(indexes_dir):
            if file.endswith('.faiss'):
                index_name = file.replace('.faiss', '')
                indexes.append(index_name)
        
        return indexes
    
    def search_all_indexes(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """Search across all file indexes"""
        all_results = []
        available_indexes = self.list_file_indexes()
        
        if not available_indexes:
            print("No indexes found. Please create indexes first.")
            return []
        
        print(f"Searching across {len(available_indexes)} indexes...")
        
        for index_name in available_indexes:
            # Find corresponding source file
            source_file = None
            # Get the project root directory
            project_root = os.path.dirname(os.path.abspath(__file__))
            data_dir = os.path.join(project_root, "data/opensearch")
            
            for file in os.listdir(data_dir):
                if file.startswith(index_name) and file.endswith('.json'):
                    source_file = os.path.join(data_dir, file)
                    break
            
            if source_file:
                results = self.search_file_index(source_file, query, top_k)
                all_results.extend(results)
        
        # Sort by similarity score and return top_k
        all_results.sort(key=lambda x: x['similarity_score'], reverse=True)
        return all_results[:top_k]
    
    def get_index_statistics(self, file_path: str) -> Dict[str, Any]:
        """Get statistics for specific index"""
        try:
            file_name = os.path.splitext(os.path.basename(file_path))[0]
            index_path = f"indexes/{file_name}.faiss"
            metadata_path = f"indexes/{file_name}.json"
            
            if not os.path.exists(index_path) or not os.path.exists(metadata_path):
                return {"error": "Index not found"}
            
            # Load index
            index = faiss.read_index(index_path)
            
            # Load metadata
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            # Calculate statistics
            stats = {
                "index_name": file_name,
                "total_embeddings": index.ntotal,
                "dimensions": index.d,
                "index_type": "IndexFlatIP",
                "file_size_mb": os.path.getsize(index_path) / (1024 * 1024),
                "metadata_size_mb": os.path.getsize(metadata_path) / (1024 * 1024),
                "type_breakdown": {}
            }
            
            # Count by type
            for item in metadata:
                item_type = item.get('type', 'unknown')
                stats["type_breakdown"][item_type] = stats["type_breakdown"].get(item_type, 0) + 1
            
            return stats
            
        except Exception as e:
            return {"error": f"Error getting statistics: {e}"}
    
    def create_consolidated_index(self, output_path: str = None) -> bool:
        """Create a consolidated index directly from source files"""
        try:
            print("Creating healthcare semantic index...")
            
            # Get the project root directory
            project_root = os.path.dirname(os.path.abspath(__file__))
            data_dir = os.path.join(project_root, "data/opensearch")
            
            # Set default output path if not provided
            if output_path is None:
                output_path = os.path.join(project_root, "indexes/healthcare_semantic_index")
            
            # Get all source files
            source_files = []
            for file in os.listdir(data_dir):
                if file.endswith('_expanded.json'):
                    source_files.append(os.path.join(data_dir, file))
            
            if not source_files:
                print(f"No expanded source files found in {data_dir}")
                return False
            
            print(f"Processing {len(source_files)} source files...")
            
            # Collect all embeddings and metadata
            all_vectors = []
            all_metadata = []
            total_embeddings = 0
            
            for source_file in source_files:
                print(f"  Processing: {source_file}")
                
                # Generate embeddings for this file
                embeddings = self.generate_all_embeddings_for_file(source_file)
                
                if embeddings:
                    for i, embedding in enumerate(embeddings):
                        if embedding.get('embedding'):
                            all_vectors.append(embedding['embedding'])
                            
                            # Enhance metadata with source file info
                            enhanced_metadata = {
                                "id": total_embeddings + i,
                                "text": embedding.get('text', ''),
                                "source_index": embedding.get('source_index', ''),
                                "organization": embedding.get('organization', ''),
                                "type": embedding.get('type', ''),
                                "source_file": source_file,
                                "file_index_name": os.path.splitext(os.path.basename(source_file))[0],
                                "consolidated_id": total_embeddings + i
                            }
                            
                            all_metadata.append(enhanced_metadata)
                    
                    total_embeddings += len(embeddings)
                    print(f"    Added {len(embeddings)} embeddings")
            
            if not all_vectors:
                print("Error: No vectors found to consolidate")
                return False
            
            # Create consolidated FAISS index
            dimension = len(all_vectors[0])
            consolidated_index = faiss.IndexFlatIP(dimension)
            
            # Convert to numpy array and normalize
            vectors_array = np.array(all_vectors, dtype=np.float32)
            faiss.normalize_L2(vectors_array)
            
            # Add all vectors to consolidated index
            consolidated_index.add(vectors_array)
            
            # Save consolidated index
            faiss.write_index(consolidated_index, f"{output_path}.faiss")
            
            # Save consolidated metadata
            with open(f"{output_path}.json", 'w', encoding='utf-8') as f:
                json.dump(all_metadata, f, indent=2, ensure_ascii=False)
            
            # Create index registry
            registry = {
                "created_at": str(np.datetime64('now')),
                "total_embeddings": total_embeddings,
                "dimensions": dimension,
                "source_files": [os.path.basename(f) for f in source_files],
                "consolidated_index_path": f"{output_path}.faiss",
                "consolidated_metadata_path": f"{output_path}.json"
            }
            
            with open(f"{output_path}_registry.json", 'w', encoding='utf-8') as f:
                json.dump(registry, f, indent=2, ensure_ascii=False)
            
            print(f"Consolidated index created successfully!")
            print(f"  Total embeddings: {total_embeddings}")
            print(f"  Dimensions: {dimension}")
            print(f"  Index file: {output_path}.faiss")
            print(f"  Metadata file: {output_path}.json")
            print(f"  Registry file: {output_path}_registry.json")
            
            return True
            
        except Exception as e:
            print(f"Error creating consolidated index: {e}")
            return False
    
    def search_consolidated_index(self, query: str, top_k: int = 10, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search the consolidated index with optional filters"""
        try:
            # Get the project root directory
            project_root = os.path.dirname(os.path.abspath(__file__))
            consolidated_path = os.path.join(project_root, "indexes/healthcare_semantic_index")
            index_path = f"{consolidated_path}.faiss"
            metadata_path = f"{consolidated_path}.json"
            
            # Check if consolidated index exists
            if not os.path.exists(index_path) or not os.path.exists(metadata_path):
                print("Consolidated index not found. Creating it now...")
                if not self.create_consolidated_index():
                    return []
            
            # Load consolidated index
            index = faiss.read_index(index_path)
            
            # Load consolidated metadata
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            # Generate query embedding
            query_embedding = self.vector_generator.generate_embedding_vector(query)
            if not query_embedding:
                print("Error: Could not generate query embedding")
                return []
            
            # Normalize query vector
            query_array = np.array([query_embedding], dtype=np.float32)
            faiss.normalize_L2(query_array)
            
            # Search with larger top_k to account for filtering
            search_k = min(top_k * 3, len(metadata)) if filters else top_k
            scores, indices = index.search(query_array, search_k)
            
            # Format results and apply filters
            results = []
            for score, idx in zip(scores[0], indices[0]):
                if idx < len(metadata):
                    result = {
                        "similarity_score": float(score),
                        "text": metadata[idx]["text"],
                        "source_index": metadata[idx]["source_index"],
                        "organization": metadata[idx]["organization"],
                        "type": metadata[idx]["type"],
                        "source_file": metadata[idx]["source_file"],
                        "file_index_name": metadata[idx]["file_index_name"],
                        "consolidated_id": metadata[idx]["consolidated_id"]
                    }
                    
                    # Apply filters if provided
                    if filters:
                        match = True
                        for key, value in filters.items():
                            if key in result and result[key] != value:
                                match = False
                                break
                        if match:
                            results.append(result)
                    else:
                        results.append(result)
                    
                    # Stop when we have enough results
                    if len(results) >= top_k:
                        break
            
            return results
            
        except Exception as e:
            print(f"Error searching consolidated index: {e}")
            return []
    
    def add_file_to_consolidated_index(self, file_path: str) -> bool:
        """Add a new file to the consolidated index"""
        try:
            print(f"Adding {file_path} to healthcare semantic index...")
            
            # Rebuild consolidated index (will include the new file if it's in data/opensearch/)
            return self.create_consolidated_index()
            
        except Exception as e:
            print(f"Error adding file to consolidated index: {e}")
            return False
    
    def get_consolidated_index_statistics(self) -> Dict[str, Any]:
        """Get statistics for the consolidated index"""
        try:
            # Get the project root directory
            project_root = os.path.dirname(os.path.abspath(__file__))
            registry_path = os.path.join(project_root, "indexes/healthcare_semantic_index_registry.json")
            index_path = os.path.join(project_root, "indexes/healthcare_semantic_index.faiss")
            metadata_path = os.path.join(project_root, "indexes/healthcare_semantic_index.json")
            
            if not os.path.exists(registry_path):
                return {"error": "Consolidated index not found"}
            
            # Load registry
            with open(registry_path, 'r', encoding='utf-8') as f:
                registry = json.load(f)
            
            # Load index for additional stats
            if os.path.exists(index_path):
                index = faiss.read_index(index_path)
                registry["index_ntotal"] = index.ntotal
                registry["index_dimensions"] = index.d
                registry["index_file_size_mb"] = os.path.getsize(index_path) / (1024 * 1024)
            
            if os.path.exists(metadata_path):
                registry["metadata_file_size_mb"] = os.path.getsize(metadata_path) / (1024 * 1024)
            
            # Get breakdown by source files
            if os.path.exists(metadata_path):
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                
                source_breakdown = {}
                type_breakdown = {}
                organization_breakdown = {}
                
                for item in metadata:
                    # Source file breakdown
                    source = item.get("source_index", "unknown")
                    source_breakdown[source] = source_breakdown.get(source, 0) + 1
                    
                    # Type breakdown
                    item_type = item.get("type", "unknown")
                    type_breakdown[item_type] = type_breakdown.get(item_type, 0) + 1
                    
                    # Organization breakdown
                    org = item.get("organization", "unknown")
                    organization_breakdown[org] = organization_breakdown.get(org, 0) + 1
                
                registry["source_breakdown"] = source_breakdown
                registry["type_breakdown"] = type_breakdown
                registry["organization_breakdown"] = organization_breakdown
            
            return registry
            
        except Exception as e:
            return {"error": f"Error getting consolidated index statistics: {e}"}
    
    def rebuild_consolidated_index(self) -> bool:
        """Rebuild the consolidated index from all current file indexes"""
        try:
            print("Rebuilding consolidated index...")
            return self.create_consolidated_index()
        except Exception as e:
            print(f"Error rebuilding consolidated index: {e}")
            return False

def main():
    """Main function to generate embeddings"""
    print("Healthcare Embedding Generator")
    print("="*40)
    
    # Initialize generator
    generator = EmbeddingGenerator()
    
    # Generate all embeddings
    print("Generating embeddings from index metadata...")
    embeddings = generator.generate_all_embeddings()
    
    # Print summary
    generator.print_embedding_summary(embeddings)
    
    # Print sample embeddings
    generator.print_sample_embeddings(embeddings, max_samples=1)
    
    # Save to file
    generator.save_embeddings_to_file(embeddings, "healthcare_embeddings.json")
    
    print("\nEmbedding generation completed successfully!")
    
    return embeddings

if __name__ == "__main__":
    embeddings = main()
