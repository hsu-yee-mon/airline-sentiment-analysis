import kagglehub
import hashlib
import datetime
import json
import sys
import os
import shutil
import importlib.metadata

def fetch_and_record_kaggle_data(dataset_handle, target_dir, metadata_file):
    # 1. Record Acquisition Date
    acquisition_date = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    # 2. Download to Kaggle Cache
    print(f"Downloading {dataset_handle} to cache...")
    cache_path = kagglehub.dataset_download(dataset_handle)
    
    # 3. Copy Actual Dataset to Your Project Folder
    print(f"Copying dataset to {target_dir}...")
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir) # Clear existing directory if it exists
    shutil.copytree(cache_path, target_dir)
    
    # 4. Calculate Hashes from Your Local Copy
    file_hashes = {}
    for root, _, files in os.walk(target_dir):
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, target_dir)
            
            sha256 = hashlib.sha256()
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(8192), b''):
                    sha256.update(chunk)
            file_hashes[rel_path] = sha256.hexdigest()
            
    aggregate_hash = hashlib.sha256(json.dumps(file_hashes, sort_keys=True).encode()).hexdigest()
    
    # 5. Record Package Versions
    versions = {
        "python": sys.version.split()[0],
        "kagglehub": importlib.metadata.version("kagglehub")
    }
    
    # 6. Save Metadata
    metadata = {
        "dataset_handle": dataset_handle,
        "kaggle_url": f"https://www.kaggle.com/datasets/{dataset_handle}",
        "acquisition_date": acquisition_date,
        "dataset_aggregate_sha256": aggregate_hash,
        "files": file_hashes,
        "local_project_path": target_dir,
        "package_versions": versions
    }
    
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=4)
        
    print(f"Success! Actual dataset saved to '{target_dir}/' and metadata to '{metadata_file}'")

# Example Usage:
# fetch_and_record_kaggle_data(
#     dataset_handle="bricevergnou/spotify-recommendation",
#     target_dir="./data/spotify_dataset",
#     metadata_file="./data/spotify_metadata.json"
# )