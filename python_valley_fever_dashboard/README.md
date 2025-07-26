# Valley Fever Analysis Dashboard - Python Version

This is a Python implementation of the Valley Fever analysis dashboard using Plotly Dash, recreating the functionality of the original R Shiny application.

## Features

- **Interactive Choropleth Map**: Visualize different metrics across California counties
- **Scatter Plot Analysis**: Explore relationships between Social Vulnerability Index and Valley Fever rates
- **Model Performance**: View GAM (or Random Forest) model predictions vs actual rates
- **Time Series Analysis**: Track Valley Fever cases over time at state and county levels
- **Key Metrics**: Display important statistics and insights

## Setup Instructions

1. **Create Virtual Environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Data Files**: Ensure the following data files are in the project directory:
   - `final_county_data`
   - `valley_fever_cases_by_lhd_2001-2023.csv`
   - `california_county.csv`
   - `CalEnviroScreen_4.0_Results.csv`

## Running the Dashboard

1. Navigate to the project directory:
   ```bash
   cd python_valley_fever_dashboard
   ```

2. Run the application:
   ```bash
   python app.py
   ```

3. Open your web browser and go to: `http://127.0.0.1:8050`

## Project Structure

```
python_valley_fever_dashboard/
├── app.py                     # Main dashboard application
├── data_processing.py         # Data loading and processing functions
├── requirements.txt           # Python dependencies
├── README.md                 # This file
├── final_county_data         # County-level aggregated data
├── valley_fever_cases_by_lhd_2001-2023.csv  # Valley fever cases by year
├── california_county.csv     # Social Vulnerability Index data
└── CalEnviroScreen_4.0_Results.csv  # Environmental screening data
```

## Dashboard Components

### Main Visualizations
1. **Map Tab**: Interactive choropleth map with selectable layers
2. **SVI vs. Rate Tab**: Scatter plot with trend line
3. **GAM Performance Tab**: Model predictions vs actual values
4. **Time Series Tab**: Temporal trends

### Controls
- **Map Layer Selector**: Choose from Valley Fever Rate, SVI Score, PM2.5, GAM Predictions, or Total Cases
- **County Selector**: Focus on specific counties for time series analysis

### Key Metrics
- Total number of counties analyzed
- Highest Valley Fever rate and corresponding county

## Data Sources

- **Valley Fever Cases**: California Department of Public Health (2001-2023)
- **Social Vulnerability Index**: CDC/ATSDR Social Vulnerability Index
- **Environmental Data**: CalEnviroScreen 4.0
- **Geographic Data**: US Census Bureau (county boundaries)

## Technical Details

- **Framework**: Plotly Dash with Bootstrap components
- **Modeling**: Random Forest regression (when GAM predictions unavailable)
- **Styling**: Bootstrap 5 theme
- **Interactive Elements**: Plotly charts with hover tooltips and selection

## Differences from R Shiny Version

- Uses Random Forest instead of GAM when model predictions need to be generated
- Simplified geographic mapping (no detailed county boundary visualization)
- Bootstrap-based layout instead of shinydashboard
- Python data processing pipeline instead of R/tidyverse

## Future Enhancements

- Add actual California county boundary GeoJSON for detailed mapping
- Implement GAM modeling using statsmodels or similar
- Add more interactive filtering options
- Include export functionality for charts and data
- Add real-time data updates

## About Valley Fever

Valley Fever (Coccidioidomycosis) is a fungal infection caused by breathing in spores of Coccidioides fungi. It's endemic to the southwestern United States, particularly California and Arizona. Cases have been increasing significantly over the past two decades, making it an important public health concern.

For more information, visit: [CDC Valley Fever Information](https://www.cdc.gov/valley-fever/) 