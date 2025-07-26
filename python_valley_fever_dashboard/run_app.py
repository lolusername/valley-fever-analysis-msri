#!/usr/bin/env python3
"""
Simple runner script for the Valley Fever Dashboard
"""

import os
import sys

def main():
    """Run the dashboard application"""
    print("=" * 60)
    print("Valley Fever Analysis Dashboard - Python Version")
    print("=" * 60)
    print()
    
    # Check if data files exist
    required_files = [
        'final_county_data',
        'valley_fever_cases_by_lhd_2001-2023.csv',
        'california_county.csv'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required data files:")
        for file in missing_files:
            print(f"   - {file}")
        print()
        print("Please ensure all data files are in the current directory.")
        sys.exit(1)
    
    print("✅ All required data files found")
    print()
    print("Starting dashboard...")
    print("🌐 Dashboard will be available at: http://127.0.0.1:8050")
    print("📊 Press Ctrl+C to stop the server")
    print()
    
    # Import and run the app
    try:
        from app import app
        app.run(debug=True, host='127.0.0.1', port=8050)
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting dashboard: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 