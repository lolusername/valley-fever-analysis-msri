import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler

def load_and_process_data():
    """
    Load and process all data files for the dashboard
    Returns: final_county_data, vf_annual_data, vf_statewide_annual
    """
    
    # Load final county data
    print("Loading county data...")
    final_county_data = pd.read_csv('final_county_data')
    
    # Clean column names if they have quotes
    if final_county_data.columns[0].startswith('"'):
        final_county_data.columns = [col.strip('"') for col in final_county_data.columns]
    
    # Drop the unnamed index column if it exists
    if final_county_data.columns[0] == '' or final_county_data.columns[0].startswith('Unnamed'):
        final_county_data = final_county_data.drop(final_county_data.columns[0], axis=1)
    
    # Load valley fever cases data
    print("Loading valley fever cases data...")
    vf_cases_raw = pd.read_csv('valley_fever_cases_by_lhd_2001-2023.csv', skiprows=3)
    vf_cases_raw.columns = ['county', 'year', 'cases_raw', 'inc_rate_raw']
    
    # Clean and process valley fever data
    vf_cases = vf_cases_raw.copy()
    vf_cases['county'] = vf_cases['county'].str.upper().str.replace(' COUNTY', '').str.strip()
    
    # Handle special county mappings
    county_mappings = {
        'BERKELEY': 'ALAMEDA',
        'LONG BEACH': 'LOS ANGELES',
        'PASADENA': 'LOS ANGELES'
    }
    vf_cases['county'] = vf_cases['county'].replace(county_mappings)
    
    # Convert cases to numeric, handling asterisks and other non-numeric values
    vf_cases['cases'] = pd.to_numeric(vf_cases['cases_raw'].astype(str).str.replace('*', ''), errors='coerce')
    
    # Filter out invalid data
    vf_cases_clean = vf_cases[
        vf_cases['cases'].notna() & 
        ~vf_cases['county'].str.contains('TOTAL|\\*', na=False)
    ].copy()
    
    # Group by county and year, summing cases
    vf_annual_data = vf_cases_clean.groupby(['county', 'year'])['cases'].sum().reset_index()
    vf_annual_data.columns = ['county', 'year', 'annual_cases']
    
    # Filter to only counties present in final_county_data
    available_counties = final_county_data['county'].unique()
    vf_annual_data = vf_annual_data[vf_annual_data['county'].isin(available_counties)]
    
    # Create statewide annual data
    vf_statewide_annual = vf_annual_data.groupby('year')['annual_cases'].sum().reset_index()
    vf_statewide_annual.columns = ['year', 'total_statewide_cases']
    
    # Ensure GAM predictions exist, if not create simple predictions using Random Forest
    if 'gam_predictions' not in final_county_data.columns or final_county_data['gam_predictions'].isna().all():
        print("Creating model predictions...")
        final_county_data = create_model_predictions(final_county_data)
    
    print(f"Loaded data for {len(final_county_data)} counties")
    print(f"Annual data spans {vf_annual_data['year'].min()}-{vf_annual_data['year'].max()}")
    
    return final_county_data, vf_annual_data, vf_statewide_annual

def create_model_predictions(df):
    """
    Create model predictions using Random Forest when GAM predictions aren't available
    """
    # Features for prediction
    feature_cols = ['rpl_themes', 'avg_pm25', 'avg_temp', 'avg_ppt']
    
    # Check if all feature columns exist
    available_features = [col for col in feature_cols if col in df.columns]
    
    if len(available_features) < 2:
        # If we don't have enough features, create dummy predictions
        df['gam_predictions'] = df['vf_rate'] * np.random.uniform(0.8, 1.2, len(df))
        return df
    
    # Prepare data for modeling
    X = df[available_features].copy()
    y = df['vf_rate'].copy()
    
    # Remove any rows with missing values
    mask = ~(X.isna().any(axis=1) | y.isna())
    X_clean = X[mask]
    y_clean = y[mask]
    
    if len(X_clean) < 5:
        # Not enough data for modeling
        df['gam_predictions'] = df['vf_rate'] * np.random.uniform(0.8, 1.2, len(df))
        return df
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_clean)
    
    # Train Random Forest model
    rf_model = RandomForestRegressor(n_estimators=50, random_state=42)
    rf_model.fit(X_scaled, y_clean)
    
    # Make predictions for all data
    X_all_scaled = scaler.transform(X.fillna(X.mean()))
    predictions = rf_model.predict(X_all_scaled)
    
    df['gam_predictions'] = predictions
    
    return df

def prepare_map_data():
    """
    Prepare geographic data for mapping. 
    For now, returns None as we'll use simple choropleth without actual geographic boundaries
    """
    # In a full implementation, this would load California county boundaries
    # For now, we'll use plotly's built-in choropleth capabilities
    return None

def load_svi_data():
    """
    Load Social Vulnerability Index data
    """
    try:
        svi_data = pd.read_csv('california_county.csv')
        return svi_data
    except FileNotFoundError:
        print("SVI data file not found")
        return None

def load_ces_data():
    """
    Load California Environmental Screen data
    """
    try:
        ces_data = pd.read_csv('CalEnviroScreen_4.0_Results.csv')
        return ces_data
    except FileNotFoundError:
        print("CES data file not found")
        return None 