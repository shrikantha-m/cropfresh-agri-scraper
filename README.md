# CropFresh AgriData Scraper

🌾 **Enterprise-Scale Agricultural Data Scraping System**

## Overview
- **15,400 parallel jobs** across GitHub Actions
- **55 commodities**: 20 vegetables + 16 fruits + 10 leafy greens + 9 cereals
- **28 Indian states** covered
- **10 years** of historical data (2015-2024)
- **Target**: 5-10 million price records for ML training

## Quick Start

### 1. Configure GitHub Secrets
Add these secrets to your repository:
```
HF_TOKEN: <your_huggingface_token>
HF_REPO_ID: shrikantha55/cropfresh-india-agri-prices
```

### 2. Push Code to GitHub
```bash
cd cropfresh_deployment
git init
git add .
git commit -m "Initial: 15,400-job enterprise scraper"
git remote add origin https://github.com/shrikantha-m/cropfresh-agri-scraper.git
git push -u origin main
```

### 3. Run the Workflow
1. Go to: https://github.com/shrikantha-m/cropfresh-agri-scraper/actions
2. Select "AgriData Matrix Scraper"
3. Click "Run workflow"
4. Wait 2-4 hours for 15,400 jobs to complete

### 4. Verify Data
Check: https://huggingface.co/datasets/shrikantha55/cropfresh-india-agri-prices

## Architecture
- **Phase 1**: 15,400 scraping jobs run in parallel (100 at a time)
- **Phase 2**: Merge all outputs and upload to Hugging Face

## Dataset Structure
```
shrikantha55/cropfresh-india-agri-prices/
└── data/
    └── india_agri_prices_full.parquet  (5-10M records)
```

## License
MIT License
