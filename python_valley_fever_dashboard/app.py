import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from data_processing import load_and_process_data, prepare_map_data

# Load and process data
print("Loading data...")
final_county_data, vf_annual_data, vf_statewide_annual = load_and_process_data()
ca_counties_geojson = prepare_map_data()

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Valley Fever Analysis Dashboard"

# Define the layout
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.H1("Valley Fever Analysis Dashboard", className="text-center mb-4"),
            html.Hr()
        ])
    ]),
    
    # Main content row
    dbc.Row([
        # Left column - Controls and Info
        dbc.Col([
            # Welcome box
            dbc.Card([
                dbc.CardHeader("Welcome"),
                dbc.CardBody([
                    html.P([
                        "Emerging diseases are an existential threat to humanity; the latest one, "
                        "the COVID‑19 pandemic, killed millions and cost the United States 16 trillion dollars. "
                        "It cost the average family of four $200,000—enough to cover their grocery expenses for 17 years. "
                        "Now we introduce a new threat, Valley Fever. Valley Fever is a fungal disease endemic to large swaths "
                        "of California and Arizona. Cases have increased ninefold in the past two decades, and it is projected "
                        "to envelop half of the mainland United States and cost Americans approximately $18 billion annually. "
                        "Our MSRI‑UP project, in the interest of quantitative justice, was to model the relationship between "
                        "Valley Fever and social vulnerability. We created a dashboard highlighting key insights of our research, "
                        "so please feel free to explore what we learned. To learn more about Valley Fever visit: ",
                        html.A("https://www.cdc.gov/valley-fever/", href="https://www.cdc.gov/valley-fever/", target="_blank")
                    ])
                ])
            ], className="mb-3"),
            
            # Key metrics
            dbc.Card([
                dbc.CardHeader("Key Metrics"),
                dbc.CardBody([
                    html.Div(id="metrics-content")
                ])
            ], className="mb-3"),
            

        ], width=4),
        
        # Right column - Visualizations
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    dbc.Tabs([
                        dbc.Tab(label="County Rankings", tab_id="map-tab"),
                        dbc.Tab(label="SVI vs. Rate", tab_id="svi-tab"),
                        dbc.Tab(label="GAM Performance", tab_id="gam-tab"),
                        dbc.Tab(label="Time Series", tab_id="timeseries-tab")
                    ], id="main-tabs", active_tab="map-tab")
                ]),
                dbc.CardBody([
                    html.Div(id="tab-content")
                ])
            ])
        ], width=8)
    ]),
    
    # Bottom section - Annual trends
    html.Hr(),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Total Statewide Valley Fever Cases by Year"),
                dbc.CardBody([
                    dcc.Graph(id="statewide-trend-plot")
                ])
            ])
        ], width=12)
    ], className="mb-3"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Select an Area for Trend Analysis"),
                dbc.CardBody([
                    dbc.Label("Choose an area to see its trend:"),
                    dcc.Dropdown(
                        id="county-selector",
                        options=[{"label": "All Endemic Counties", "value": "statewide"}] + 
                                [{"label": str(county).title(), "value": county} 
                                 for county in sorted(final_county_data['county'].unique()) if county is not None],
                        value="statewide",
                        clearable=False
                    )
                ])
            ])
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Annual Trend for Selected Area"),
                dbc.CardBody([
                    dcc.Graph(id="county-trend-plot")
                ])
            ])
        ], width=8)
    ], className="mb-3"),
    
    # Action section
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("What can we do?"),
                dbc.CardBody([
                    html.P("We can learn lessons from the COVID-19 Pandemic and take steps to prevent the next pandemic. However that is not possible without your help"),
                    html.Ul([
                        html.Li([
                            html.Strong("Information: "),
                            "We cannot solve a problem we cannot see, we urge you keep up with latest developments of this disease from trusted institutions like the NIH and CDC, check out more here: ",
                            html.A("https://www.cdc.gov/valley-fever/", href="https://www.cdc.gov/valley-fever/", target="_blank")
                        ]),
                        html.Li([
                            html.Strong("Policy: "),
                            "Call your representative, and senator, let them know how much you care about your health and that of your loved ones. At town meetings, ask them to explain how they plan to support policies that strengthen, not defund, vaccine develop and treatments. Visit this website to know who your representative is: ",
                            html.A("https://www.house.gov/representatives/find-your-representative", href="https://www.house.gov/representatives/find-your-representative", target="_blank")
                        ]),
                        html.Li([
                            html.Strong("Tell your friends and family: "),
                            "Share what you know with friends and family and ask them to share it with their friends too. The more awareness we have on this disease the more resources we extend towards its eradication"
                        ])
                    ])
                ])
            ])
        ], width=12)
    ])
], fluid=True)

# Callbacks
@callback(
    Output("metrics-content", "children"),
    Input("main-tabs", "active_tab")
)
def update_metrics(active_tab):
    counties_count = len(final_county_data)
    highest_rate_county = final_county_data.loc[final_county_data['vf_rate'].idxmax()]
    
    return [
        dbc.Alert([
            html.H4(f"{counties_count}", className="alert-heading"),
            html.P("Counties Analyzed", className="mb-0")
        ], color="info", className="mb-2"),
        dbc.Alert([
            html.H4(f"{highest_rate_county['vf_rate']:.0f}", className="alert-heading"),
            html.P(f"Highest Rate (per 100k) in {highest_rate_county['county'].title()}", className="mb-0")
        ], color="danger")
    ]

@callback(
    Output("tab-content", "children"),
    Input("main-tabs", "active_tab")
)
def update_tab_content(active_tab):
    if active_tab == "map-tab":
        return create_choropleth_map("vf_rate")  # Default to valley fever rate
    elif active_tab == "svi-tab":
        return create_svi_scatter_plot()
    elif active_tab == "gam-tab":
        return create_gam_performance_plot()
    elif active_tab == "timeseries-tab":
        return create_timeseries_plot()

@callback(
    Output("statewide-trend-plot", "figure"),
    Input("main-tabs", "active_tab")  # Dummy input to trigger initial load
)
def update_statewide_trend(dummy):
    fig = px.line(vf_statewide_annual, x='year', y='total_statewide_cases',
                  title='Total Reported Valley Fever Cases in California (2001-2023)',
                  labels={'year': 'Year', 'total_statewide_cases': 'Total Annual Cases'})
    fig.update_traces(line_color='#6f42c1', marker_color='#6f42c1')
    fig.update_layout(template='plotly_white')
    return fig

@callback(
    Output("county-trend-plot", "figure"),
    Input("county-selector", "value")
)
def update_county_trend(selected_county):
    # Handle case where selected_county is None
    if selected_county is None or selected_county == "statewide":
        plot_data = vf_statewide_annual
        fig = px.line(plot_data, x='year', y='total_statewide_cases',
                      title='Combined Annual Trend for All Endemic Counties',
                      labels={'year': 'Year', 'total_statewide_cases': 'Total Annual Cases'})
    else:
        plot_data = vf_annual_data[vf_annual_data['county'] == selected_county]
        county_name = str(selected_county).title() if selected_county else "Unknown"
        fig = px.line(plot_data, x='year', y='annual_cases',
                      title=f'Annual Cases in {county_name} County',
                      labels={'year': 'Year', 'annual_cases': 'Number of Cases'})
    
    fig.update_traces(line_color='darkorange', marker_color='darkorange')
    fig.update_layout(template='plotly_white')
    return fig

def create_choropleth_map(selected_layer):
    # Create a bar chart instead of a problematic choropleth map
    layer_names = {
        'vf_rate': 'Valley Fever Rate',
        'rpl_themes': 'Overall SVI Score',
        'avg_pm25': 'Average PM2.5',
        'gam_predictions': 'GAM Predictions',
        'total_cases': 'Total Cases'
    }
    
    # Sort counties by the selected metric for better visualization
    sorted_data = final_county_data.sort_values(by=selected_layer, ascending=True)
    
    # Create horizontal bar chart (works better for county names)
    fig = px.bar(sorted_data.tail(20),  # Show top 20 counties
                 x=selected_layer, 
                 y='county',
                 orientation='h',
                 color=selected_layer,
                 color_continuous_scale='Viridis',
                 title=f'Top 20 California Counties - {layer_names.get(selected_layer, selected_layer)}',
                 labels={'county': 'County', selected_layer: layer_names.get(selected_layer, selected_layer)})
    
    fig.update_layout(
        template='plotly_white', 
        height=600,
        yaxis={'categoryorder': 'total ascending'},
        showlegend=False
    )
    
    # Add hover information
    fig.update_traces(
        hovertemplate='<b>%{y}</b><br>' + 
                     f'{layer_names.get(selected_layer, selected_layer)}: %{{x:.2f}}<br>' +
                     '<extra></extra>'
    )
    
    return dcc.Graph(figure=fig)

def create_svi_scatter_plot():
    fig = px.scatter(final_county_data, x='rpl_themes', y='vf_rate',
                     hover_data=['county', 'e_totpop'],
                     title='Valley Fever Rate vs. SVI Score',
                     labels={'rpl_themes': 'Overall SVI Score', 'vf_rate': 'Valley Fever Rate (per 100,000)'},
                     trendline='ols')
    fig.update_layout(template='plotly_white', height=600)
    return dcc.Graph(figure=fig)

def create_gam_performance_plot():
    # Filter out any NaN predictions
    valid_data = final_county_data.dropna(subset=['gam_predictions'])
    
    if len(valid_data) == 0:
        return html.Div("No GAM predictions available", className="text-center mt-5")
    
    fig = px.scatter(valid_data, x='gam_predictions', y='vf_rate',
                     hover_data=['county'],
                     title='GAM Performance: Predicted vs. Actual VF Rate',
                     labels={'gam_predictions': 'Predicted Valley Fever Rate (by GAM)', 
                            'vf_rate': 'Actual Valley Fever Rate'})
    
    # Add perfect prediction line
    min_val = min(valid_data['gam_predictions'].min(), valid_data['vf_rate'].min())
    max_val = max(valid_data['gam_predictions'].max(), valid_data['vf_rate'].max())
    fig.add_trace(go.Scatter(x=[min_val, max_val], y=[min_val, max_val], 
                            mode='lines', name='Perfect Prediction', 
                            line=dict(dash='dash', color='black')))
    
    fig.update_layout(template='plotly_white', height=600)
    return dcc.Graph(figure=fig)

def create_timeseries_plot():
    fig = px.line(vf_statewide_annual, x='year', y='total_statewide_cases',
                  title='Valley Fever Cases Over Time',
                  labels={'year': 'Year', 'total_statewide_cases': 'Total Cases'})
    fig.update_layout(template='plotly_white', height=600)
    return dcc.Graph(figure=fig)

def generate_static_html():
    """Generate static HTML for GitHub Pages - EXACT copy of dashboard"""
    import plotly.express as px
    print("🔄 Generating static HTML for GitHub Pages...")
    
    # Use the EXACT same charts as the interactive dashboard
    fig1 = create_choropleth_map("vf_rate").figure
    fig2 = create_svi_scatter_plot().figure  
    fig3 = create_gam_performance_plot().figure
    fig4 = create_timeseries_plot().figure
    
    # Statewide trend (same as dashboard)
    fig5 = px.line(vf_statewide_annual, x='year', y='total_statewide_cases',
                   title='Total Reported Valley Fever Cases in California (2001-2023)',
                   labels={'year': 'Year', 'total_statewide_cases': 'Total Annual Cases'})
    fig5.update_traces(line_color='#6f42c1', marker_color='#6f42c1')
    fig5.update_layout(template='plotly_white', height=500)
    
    # County trend for Kern (highest rate county)
    kern_data = vf_annual_data[vf_annual_data['county'] == 'KERN']
    fig6 = px.line(kern_data, x='year', y='annual_cases',
                   title='Annual Cases in Kern County (Highest Rate)',
                   labels={'year': 'Year', 'annual_cases': 'Number of Cases'})
    fig6.update_traces(line_color='darkorange', marker_color='darkorange')
    fig6.update_layout(template='plotly_white', height=400)
    
    # Create HTML
    highest_county = final_county_data.loc[final_county_data['vf_rate'].idxmax()]
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Valley Fever Analysis Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-2.24.1.min.js"></script>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {{ font-family: Arial, sans-serif; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem 0; }}
        .metrics {{ background: #f8f9fa; border-radius: 10px; padding: 1.5rem; margin: 1rem 0; text-align: center; }}
        .metric-value {{ font-size: 2rem; font-weight: bold; color: #6f42c1; }}
    </style>
</head>
<body>
    <div class="header">
        <div class="container">
            <h1 class="text-center">Valley Fever Analysis Dashboard</h1>
            <hr style="border-color: white;">
        </div>
    </div>

    <div class="container mt-4">
        <div class="row">
            <div class="col-4">
                <div class="card mb-3">
                    <div class="card-header"><h5>Welcome</h5></div>
                    <div class="card-body">
                        <p>Emerging diseases are an existential threat to humanity; the latest one, the COVID‑19 pandemic, killed millions and cost the United States 16 trillion dollars. It cost the average family of four $200,000—enough to cover their grocery expenses for 17 years. Now we introduce a new threat, Valley Fever. Valley Fever is a fungal disease endemic to large swaths of California and Arizona. Cases have increased ninefold in the past two decades, and it is projected to envelop half of the mainland United States and cost Americans approximately $18 billion annually. Our MSRI‑UP project, in the interest of quantitative justice, was to model the relationship between Valley Fever and social vulnerability. We created a dashboard highlighting key insights of our research, so please feel free to explore what we learned. To learn more about Valley Fever visit: <a href="https://www.cdc.gov/valley-fever/" target="_blank">https://www.cdc.gov/valley-fever/</a> :)</p>
                    </div>
                </div>

                <div class="card mb-3">
                    <div class="card-header"><h5>Key Metrics</h5></div>
                    <div class="card-body">
                        <div class="alert alert-info">
                            <h4>{len(final_county_data)}</h4>
                            <p class="mb-0">Counties Analyzed</p>
                        </div>
                        <div class="alert alert-danger">
                            <h4>{highest_county['vf_rate']:.0f}</h4>
                            <p class="mb-0">Highest Rate (per 100k) in {highest_county['county'].title()}</p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-8">
                <div class="card">
                    <div class="card-header">
                        <ul class="nav nav-tabs card-header-tabs">
                            <li class="nav-item"><a class="nav-link active" href="#tab1">County Rankings</a></li>
                            <li class="nav-item"><a class="nav-link" href="#tab2">SVI vs. Rate</a></li>
                            <li class="nav-item"><a class="nav-link" href="#tab3">GAM Performance</a></li>
                            <li class="nav-item"><a class="nav-link" href="#tab4">Time Series</a></li>
                        </ul>
                    </div>
                    <div class="card-body">
                        <div id="tab1">{fig1.to_html(include_plotlyjs=False)}</div>
                        <div id="tab2" style="display:none">{fig2.to_html(include_plotlyjs=False)}</div>
                        <div id="tab3" style="display:none">{fig3.to_html(include_plotlyjs=False)}</div>
                        <div id="tab4" style="display:none">{fig4.to_html(include_plotlyjs=False)}</div>
                    </div>
                </div>
            </div>
        </div>

        <hr>
        
                 <div class="card mb-3">
             <div class="card-header"><h5>Total Statewide Valley Fever Cases by Year</h5></div>
             <div class="card-body">
                 {fig5.to_html(include_plotlyjs=False)}
             </div>
         </div>

        <div class="row">
            <div class="col-4">
                <div class="card">
                    <div class="card-header"><h5>Select an Area for Trend Analysis</h5></div>
                    <div class="card-body">
                        <p>Showing trend for: <strong>Kern County (Highest Rate)</strong></p>
                    </div>
                </div>
            </div>
            <div class="col-8">
                                 <div class="card">
                     <div class="card-header"><h5>Annual Trend for Selected Area</h5></div>
                     <div class="card-body">
                         {fig6.to_html(include_plotlyjs=False)}
                     </div>
                 </div>
            </div>
        </div>

        <div class="card mt-3">
            <div class="card-header"><h5>How to Interpret These Charts</h5></div>
            <div class="card-body">
                <p>The charts on this page show how the number of Valley Fever cases has changed over time in California. The top graph displays the total annual cases for all analyzed counties combined, showing the overall trend since 2001.</p>
                <p>The bottom graph allows you to focus on a specific area. Use the dropdown menu to see the annual case trend for an individual county or view the combined data for all endemic counties.</p>
            </div>
        </div>

        <div class="card mt-3">
            <div class="card-header"><h5>What can we do?</h5></div>
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

    <script>
        // Simple tab switching
        document.querySelectorAll('.nav-link').forEach(link => {{
            link.addEventListener('click', function(e) {{
                e.preventDefault();
                // Hide all tabs
                document.querySelectorAll('[id^="tab"]').forEach(tab => tab.style.display = 'none');
                // Remove active class
                document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
                // Show selected tab
                const target = this.getAttribute('href').substring(1);
                document.getElementById(target).style.display = 'block';
                // Add active class
                this.classList.add('active');
            }});
        }});
    </script>
</body>
</html>"""

    import os
    os.makedirs("../docs", exist_ok=True)
    with open("../docs/index.html", 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ Static HTML generated: docs/index.html")
    print("🌐 Ready for GitHub Pages!")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--static":
        generate_static_html()
    else:
        app.run(debug=True) 