#!/usr/bin/env python3
"""
Extract queries from CSV file and organize them into separate JSON files by index type.
"""

import csv
import json
import os
from collections import defaultdict

def extract_queries_from_csv(csv_file_path):
    """Extract queries from CSV file and organize by index type."""
    
    queries_by_index = defaultdict(list)
    
    with open(csv_file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            test_number = int(row['test_number'])
            query = row['query']
            description = row['description']
            expected_index = row['expected_index']
            
            # Create query object
            query_obj = {
                "test_number": test_number,
                "query": query,
                "description": description,
                "expected_index": expected_index
            }
            
            queries_by_index[expected_index].append(query_obj)
    
    return queries_by_index

def create_json_files(queries_by_index, output_dir="test_queries"):
    """Create separate JSON files for each index type."""
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Mapping of index names to file names
    index_file_mapping = {
        "healthcare_claims_index": "claims_queries_001.json",
        "healthcare_providers_index": "providers_queries_002.json", 
        "healthcare_members_index": "members_queries_003.json",
        "healthcare_procedures_index": "procedures_queries_004.json"
    }
    
    created_files = []
    
    for index_name, queries in queries_by_index.items():
        if index_name in index_file_mapping:
            filename = index_file_mapping[index_name]
            filepath = os.path.join(output_dir, filename)
            
            # Create the JSON structure
            json_data = {
                "index_name": index_name,
                "total_queries": len(queries),
                "description": f"Test queries for {index_name}",
                "queries": queries
            }
            
            # Write to file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
            
            created_files.append(filepath)
            print(f"Created {filepath} with {len(queries)} queries")
    
    return created_files

def main():
    """Main function to extract and organize queries."""
    
    csv_file = "healthcare_router_150_queries_20250911_194041.csv"
    
    if not os.path.exists(csv_file):
        print(f"Error: CSV file {csv_file} not found")
        return
    
    print("Extracting queries from CSV file...")
    queries_by_index = extract_queries_from_csv(csv_file)
    
    print(f"\nFound queries for {len(queries_by_index)} index types:")
    for index_name, queries in queries_by_index.items():
        print(f"  {index_name}: {len(queries)} queries")
    
    print("\nCreating JSON files...")
    created_files = create_json_files(queries_by_index)
    
    print(f"\n✅ Successfully created {len(created_files)} JSON files:")
    for filepath in created_files:
        print(f"  - {filepath}")

if __name__ == "__main__":
    main()
