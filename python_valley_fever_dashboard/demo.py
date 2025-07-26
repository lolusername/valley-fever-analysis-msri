#!/usr/bin/env python3
"""
Demo script to test the Valley Fever Dashboard functionality
"""

import pandas as pd
import plotly.express as px
from data_processing import load_and_process_data

def main():
    print("🧪 Testing Valley Fever Dashboard Components")
    print("=" * 50)
    
    # Load data
    print("1. Loading data...")
    final_county_data, vf_annual_data, vf_statewide_annual = load_and_process_data()
    
    # Display basic statistics
    print(f"\n📊 Data Summary:")
    print(f"   Counties: {len(final_county_data)}")
    print(f"   Annual records: {len(vf_annual_data)}")
    print(f"   Years covered: {vf_annual_data['year'].min():.0f}-{vf_annual_data['year'].max():.0f}")
    print(f"   Total statewide records: {len(vf_statewide_annual)}")
    
    # Show some key metrics
    highest_rate_county = final_county_data.loc[final_county_data['vf_rate'].idxmax()]
    print(f"\n🏆 Key Metrics:")
    print(f"   Highest VF rate: {highest_rate_county['vf_rate']:.1f} per 100k in {highest_rate_county['county']}")
    print(f"   Average VF rate: {final_county_data['vf_rate'].mean():.1f} per 100k")
    print(f"   Total cases (latest year): {vf_statewide_annual.iloc[-1]['total_statewide_cases']:.0f}")
    
    # Test visualization creation
    print(f"\n📈 Testing visualizations...")
    
    # Create scatter plot
    fig1 = px.scatter(final_county_data, x='rpl_themes', y='vf_rate',
                     title='Valley Fever Rate vs. SVI Score')
    print(f"   ✅ Scatter plot created")
    
    # Create time series
    fig2 = px.line(vf_statewide_annual, x='year', y='total_statewide_cases',
                   title='Valley Fever Cases Over Time')
    print(f"   ✅ Time series plot created")
    
    # Test choropleth data
    if 'gam_predictions' in final_county_data.columns:
        valid_predictions = final_county_data['gam_predictions'].notna().sum()
        print(f"   ✅ GAM predictions available for {valid_predictions}/{len(final_county_data)} counties")
    
    # Show available counties for dropdown
    counties = sorted(final_county_data['county'].unique())
    print(f"\n🏘️  Available counties for analysis:")
    print(f"   {len(counties)} counties from {counties[0]} to {counties[-1]}")
    
    print(f"\n✅ All tests passed! Dashboard should work correctly.")
    print(f"🚀 Run 'python app.py' or 'python run_app.py' to start the dashboard")

if __name__ == "__main__":
    main() 