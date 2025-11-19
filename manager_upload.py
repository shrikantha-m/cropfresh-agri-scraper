#!/usr/bin/env python3
"""Manager Upload - Merges all artifacts and uploads to Hugging Face"""
import os
import pandas as pd
from pathlib import Path
from huggingface_hub import HfApi, create_repo

def merge_and_upload():
    print("📦 Merging all scraped data...")
    
    # Collect all parquet files
    all_files = list(Path("artifacts").rglob("*.parquet"))
    print(f"Found {len(all_files)} parquet files")
    
    if not all_files:
        print("⚠️  No data files found!")
        return
    
    # Read and combine all files
    dfs = []
    for file in all_files:
        try:
            df = pd.read_parquet(file)
            dfs.append(df)
        except Exception as e:
            print(f"❌ Error reading {file}: {e}")
    
    if not dfs:
        print("⚠️  No valid dataframes!")
        return
    
    # Combine all data
    combined = pd.concat(dfs, ignore_index=True)
    print(f"✅ Combined: {len(combined):,} total records")
    
    # Save merged file
    output_path = Path("merged_data/india_agri_prices_full.parquet")
    output_path.parent.mkdir(exist_ok=True)
    combined.to_parquet(output_path, index=False)
    print(f"💾 Saved merged file: {output_path}")
    
    # Upload to Hugging Face
    hf_token = os.getenv("HF_TOKEN")
    hf_repo = os.getenv("HF_REPO_ID")
    
    if not hf_token or not hf_repo:
        print("❌ Missing HF_TOKEN or HF_REPO_ID environment variables!")
        return
    
    print(f"
🚀 Uploading to Hugging Face: {hf_repo}")
    
    api = HfApi(token=hf_token)
    
    try:
        # Upload the merged file
        api.upload_file(
            path_or_fileobj=str(output_path),
            path_in_repo="data/india_agri_prices_full.parquet",
            repo_id=hf_repo,
            repo_type="dataset",
            commit_message=f"Add {len(combined):,} agricultural price records"
        )
        print(f"✅ Successfully uploaded {len(combined):,} records to Hugging Face!")
        print(f"🔗 View dataset: https://huggingface.co/datasets/{hf_repo}")
    except Exception as e:
        print(f"❌ Upload failed: {e}")

if __name__ == "__main__":
    merge_and_upload()
