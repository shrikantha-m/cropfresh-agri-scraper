#!/usr/bin/env python3
"""Agmarknet Worker - Scrapes single commodity for single state and year"""
import os
import sys
import json
import pandas as pd
import requests
from datetime import datetime, timedelta
from pathlib import Path

def scrape_agmarknet(commodity, state, year):
    """Scrape Agmarknet for single commodity/state/year"""
    
    base_url = "https://agmarknet.gov.in/SearchCmmMkt.aspx"
    
    # Date range for the year
    start_date = f"01/01/{year}"
    end_date = f"31/12/{year}"
    
    params = {
        'Tx_Commodity': commodity,
        'Tx_State': state,
        'Tx_District': 'All',
        'Tx_Market': 'All',
        'DateFrom': start_date,
        'DateTo': end_date,
        'Fr_Date': start_date,
        'To_Date': end_date,
        'Tx_Trend': '0',
        'Tx_CommodityHead': commodity,
        'Tx_StateHead': state
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=30)
        response.raise_for_status()
        
        # Parse HTML tables using pandas
        tables = pd.read_html(response.text)
        
        if not tables:
            print(f"⚠️  No data: {commodity}/{state}/{year}")
            return pd.DataFrame()
        
        df = tables[0]  # First table contains price data
        
        # Add metadata
        df['commodity'] = commodity
        df['state'] = state
        df['year'] = year
        df['source'] = 'agmarknet'
        df['scraped_at'] = datetime.now().isoformat()
        
        print(f"✅ Success: {commodity}/{state}/{year} - {len(df)} records")
        return df
        
    except Exception as e:
        print(f"❌ Error: {commodity}/{state}/{year} - {str(e)}")
        return pd.DataFrame()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python agmarknet_worker.py <commodity> <state> <year>")
        sys.exit(1)
    
    commodity = sys.argv[1]
    state = sys.argv[2]
    year = sys.argv[3]
    
    # Scrape data
    df = scrape_agmarknet(commodity, state, year)
    
    # Save to artifacts
    if not df.empty:
        output_dir = Path(f"artifacts/{year}")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"{commodity.replace(' ', '_')}_{state.replace(' ', '_')}_{year}.parquet"
        output_path = output_dir / filename
        
        df.to_parquet(output_path, index=False)
        print(f"💾 Saved: {output_path}")
    else:
        print(f"⚠️  No data to save for {commodity}/{state}/{year}")
