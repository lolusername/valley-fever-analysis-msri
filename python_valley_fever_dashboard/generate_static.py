#!/usr/bin/env python3
"""
Generate static HTML page for GitHub Pages deployment
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.offline as pyo
from data_processing import load_and_process_data
import pandas as pd

def create_static_dashboard():
    """Generate complete static HTML dashboard"""
    
    print("🔄 Loading data...")
    final_county_data, vf_annual_data, vf_statewide_annual = load_and_process_data()
    
    print("📊 Creating visualizations...")
    
    # 1. County Rankings Chart (Valley Fever Rate)
    sorted_data = final_county_data.sort_values(by='vf_rate', ascending=True)
    fig1 = px.bar(sorted_data.tail(20), 
                  x='vf_rate', 
                  y='county',
                  orientation='h',
                  color='vf_rate',
                  color_continuous_scale='Viridis',
                  title='Top 20 California Counties - Valley Fever Rate',
                  labels={'county': 'County', 'vf_rate': 'Valley Fever Rate (per 100k)'})
    fig1.update_layout(height=600, yaxis={'categoryorder': 'total ascending'}, showlegend=False)
    
    # 2. SVI vs Valley Fever Rate Scatter
    fig2 = px.scatter(final_county_data, x='rpl_themes', y='vf_rate',
                      hover_data=['county', 'e_totpop'],
                      title='Valley Fever Rate vs. Social Vulnerability Index',
                      labels={'rpl_themes': 'Overall SVI Score', 'vf_rate': 'Valley Fever Rate (per 100k)'},
                      trendline='ols')
    fig2.update_layout(height=600)
    
    # 3. GAM Performance Plot
    valid_data = final_county_data.dropna(subset=['gam_predictions'])
    fig3 = px.scatter(valid_data, x='gam_predictions', y='vf_rate',
                      hover_data=['county'],
                      title='Model Performance: Predicted vs. Actual Valley Fever Rate',
                      labels={'gam_predictions': 'Predicted Valley Fever Rate', 
                             'vf_rate': 'Actual Valley Fever Rate'})
    # Add perfect prediction line
    min_val = min(valid_data['gam_predictions'].min(), valid_data['vf_rate'].min())
    max_val = max(valid_data['gam_predictions'].max(), valid_data['vf_rate'].max())
    fig3.add_trace(go.Scatter(x=[min_val, max_val], y=[min_val, max_val], 
                              mode='lines', name='Perfect Prediction', 
                              line=dict(dash='dash', color='black')))
    fig3.update_layout(height=600)
    
    # 4. Statewide Trend
    fig4 = px.line(vf_statewide_annual, x='year', y='total_statewide_cases',
                   title='Total Reported Valley Fever Cases in California (2001-2023)',
                   labels={'year': 'Year', 'total_statewide_cases': 'Total Annual Cases'})
    fig4.update_traces(line_color='#6f42c1', marker_color='#6f42c1')
    fig4.update_layout(height=500)
    
    # 5. Top 5 Counties Individual Trends
    top_counties = final_county_data.nlargest(5, 'vf_rate')['county'].tolist()
    fig5 = go.Figure()
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    for i, county in enumerate(top_counties):
        county_data = vf_annual_data[vf_annual_data['county'] == county]
        fig5.add_trace(go.Scatter(x=county_data['year'], y=county_data['annual_cases'],
                                  mode='lines+markers', name=county.title(),
                                  line=dict(color=colors[i])))
    
    fig5.update_layout(title='Annual Cases - Top 5 Counties by Valley Fever Rate',
                       xaxis_title='Year', yaxis_title='Annual Cases',
                       height=500)
    
    print("🌐 Generating HTML...")
    
    # Create individual chart HTML files and combine them
    chart1_html = fig1.to_html(include_plotlyjs='cdn', div_id="chart1")
    chart2_html = fig2.to_html(include_plotlyjs='cdn', div_id="chart2") 
    chart3_html = fig3.to_html(include_plotlyjs='cdn', div_id="chart3")
    chart4_html = fig4.to_html(include_plotlyjs='cdn', div_id="chart4")
    chart5_html = fig5.to_html(include_plotlyjs='cdn', div_id="chart5")
    
    # Create complete HTML page
    highest_county = final_county_data.loc[final_county_data['vf_rate'].idxmax()]
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Valley Fever Analysis Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {{ font-family: 'Arial', sans-serif; }}
        .dashboard-header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem 0; }}
        .chart-container {{ margin: 2rem 0; }}
        .metrics-card {{ background: #f8f9fa; border-radius: 10px; padding: 1.5rem; margin: 1rem 0; }}
        .metric-value {{ font-size: 2rem; font-weight: bold; color: #6f42c1; }}
        .footer {{ background: #343a40; color: white; padding: 2rem 0; margin-top: 3rem; }}
    </style>
</head>
<body>
    <div class="dashboard-header">
        <div class="container">
            <h1 class="text-center mb-4">Valley Fever Analysis Dashboard</h1>
            <p class="text-center lead">Interactive Analysis of Social and Environmental Drivers</p>
        </div>
    </div>

    <div class="container mt-4">
        <!-- Welcome Section -->
        <div class="row">
            <div class="col-12">
                <div class="card mb-4">
                    <div class="card-header">
                        <h3>Welcome</h3>
                    </div>
                    <div class="card-body">
                        <p>Emerging diseases are an existential threat to humanity; the latest one, the COVID‑19 pandemic, killed millions and cost the United States 16 trillion dollars. It cost the average family of four $200,000—enough to cover their grocery expenses for 17 years. Now we introduce a new threat, Valley Fever. Valley Fever is a fungal disease endemic to large swaths of California and Arizona. Cases have increased ninefold in the past two decades, and it is projected to envelop half of the mainland United States and cost Americans approximately $18 billion annually. Our MSRI‑UP project, in the interest of quantitative justice, was to model the relationship between Valley Fever and social vulnerability. We created a dashboard highlighting key insights of our research, so please feel free to explore what we learned. To learn more about Valley Fever visit: <a href="https://www.cdc.gov/valley-fever/" target="_blank">https://www.cdc.gov/valley-fever/</a></p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Key Metrics -->
        <div class="row">
            <div class="col-md-6">
                <div class="metrics-card text-center">
                    <div class="metric-value">{len(final_county_data)}</div>
                    <div class="text-muted">Counties Analyzed</div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="metrics-card text-center">
                    <div class="metric-value">{highest_county['vf_rate']:.0f}</div>
                    <div class="text-muted">Highest Rate (per 100k) in {highest_county['county'].title()}</div>
                </div>
            </div>
        </div>

        <!-- Charts -->
        <div class="row">
            <div class="col-12">
                <div class="chart-container">
                    {chart1_html}
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-md-6">
                <div class="chart-container">
                    {chart2_html}
                </div>
            </div>
            <div class="col-md-6">
                <div class="chart-container">
                    {chart3_html}
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-12">
                <div class="chart-container">
                    {chart4_html}
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-12">
                <div class="chart-container">
                    {chart5_html}
                </div>
            </div>
        </div>

        <!-- Action Section -->
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h3>What can we do?</h3>
                    </div>
                    <div class="card-body">
                        <p>We can learn lessons from the COVID-19 Pandemic and take steps to prevent the next pandemic. However that is not possible without your help</p>
                        <ul>
                            <li><strong>Information:</strong> We cannot solve a problem we cannot see, we urge you keep up with latest developments of this disease from trusted institutions like the NIH and CDC, check out more here: <a href="https://www.cdc.gov/valley-fever/" target="_blank">https://www.cdc.gov/valley-fever/</a></li>
                            <li><strong>Policy:</strong> Call your representative, and senator, let them know how much you care about your health and that of your loved ones. At town meetings, ask them to explain how they plan to support policies that strengthen, not defund, vaccine develop and treatments. Visit this website to know who your representative is: <a href="https://www.house.gov/representatives/find-your-representative" target="_blank">https://www.house.gov/representatives/find-your-representative</a></li>
                            <li><strong>Tell your friends and family:</strong> Share what you know with friends and family and ask them to share it with their friends too. The more awareness we have on this disease the more resources we extend towards its eradication</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="footer">
        <div class="container text-center">
            <p>&copy; 2024 Valley Fever Analysis Dashboard | MSRI-UP Research Project</p>
            <p>Data sources: California Department of Public Health, CDC/ATSDR Social Vulnerability Index, CalEnviroScreen 4.0</p>
        </div>
    </div>
</body>
</html>"""

    # Save to docs directory
    output_file = "/docs/index.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Static dashboard generated: {output_file}")
    print("🌐 Ready for GitHub Pages deployment!")
    print("📊 Dashboard includes:")
    print("   - County rankings visualization")
    print("   - SVI vs Valley Fever analysis") 
    print("   - Model performance evaluation")
    print("   - Time series trends")
    print("   - Top counties detailed analysis")

if __name__ == "__main__":
    create_static_dashboard() 