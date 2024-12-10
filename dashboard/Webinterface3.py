# -*- coding: utf-8 -*-
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc

# Mock Data for Visualization
np.random.seed(42)

# Mock fuel data
fuel_data = pd.DataFrame({
    'Fuel Source': ['Gasoline', 'Diesel', 'Electric', 'Hybrid'],
    'Count': [90, 60, 30, 50]
})

# Mock wheelchair accessibility data
accessibility_data = pd.DataFrame({
    'Accessibility': ['Yes', 'No'],
    'Count': [70, 30]
})

# Mock registration trends data
registration_data = pd.DataFrame({
    'Year': np.arange(2000, 2023),
    'Registrations': np.random.randint(50, 200, size=23)
})

# Mock geographic distribution data
map_data = pd.DataFrame({
    'Latitude': np.random.uniform(30.0, 42.0, 50),
    'Longitude': np.random.uniform(-90.0, -80.0, 50),
    'Registrations': np.random.randint(1, 100, size=50),
    'City': [f'City {i}' for i in range(50)]
})

# Mock sentiment data
sentiment_data = pd.DataFrame({
    'Sentiment Scores': np.random.randint(-5, 5, 100)
})

# Mock Kia vehicle sentiment category data
category_data = pd.DataFrame({
    'Category': ['Driving Experience', 'Features', 'Value for Money', 'Issues', 'Other'],
    'Count': np.random.randint(10, 100, 5),
    'Sentiment': ['Positive', 'Neutral', 'Positive', 'Negative', 'Neutral']
})

# Calculate percentage
fuel_data['Percentage'] = (fuel_data['Count'] / fuel_data['Count'].sum()) * 100

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server

# Main Dashboard Layout
app.layout = html.Div([
    html.H1("Vehicle Insights Dashboard", style={'textAlign': 'center', 'marginBottom': '20px', 'marginTop': '20px'}),
    

    # Filters
    html.Div([
        html.Label('Select Fuel Type:', className='label'),
        dcc.Dropdown(
            id='fuel-type-filter',
            options=[{'label': 'All', 'value': 'All'}] + [{'label': fuel, 'value': fuel} for fuel in fuel_data['Fuel Source']],
            value='All',
            clearable=False,
            className='dropdown'
        ),
        html.Label('Select Accessibility:', className='label'),
        dcc.Dropdown(
            id='accessibility-filter',
            options=[{'label': 'All', 'value': 'All'}] + [{'label': acc, 'value': acc} for acc in accessibility_data['Accessibility']],
            value='All',
            clearable=False,
            className='dropdown'
        ),
        html.Label('Select Year Range:', className='label'),
        dcc.RangeSlider(
            id='year-range-slider',
            min=2000,
            max=2022,
            step=1,
            marks={year: str(year) for year in range(2000, 2023)},
            value=[2000, 2022],
            className='slider'
        )
    ], style={'padding': '30px'}),

    # Tabs for Main Dashboard
    dcc.Tabs([
        
        # Vehicle Details Tab
        dcc.Tab(label='Vehicle Details', children=[
            dcc.Tabs([


                # Sub-tab 1: Fuel Type Distribution
                dcc.Tab(
                    label='Fuel Type Distribution',
                     children=[
                        dcc.Graph(
                           id='fuel-chart',
                           figure=px.bar(
                                fuel_data, 
                                x='Fuel Source', 
                                y='Percentage', 
                                title="Fuel Type Distribution",
                                labels={'Percentage': 'Percentage (%)'}  # Label y-axis as Percentage
                                        )
                                  )
                               ], 
                    style={
                     'backgroundColor': '#f0f8ff', 
                     'border': '1px solid #d1e7ff', 
                     'fontSize': '12px', 
                     'padding': '5px'
                          },
                    selected_style={
                    'backgroundColor': '#d1e7ff', 
                    'color': 'black', 
                    'fontSize': '12px', 
                    'padding': '5px'
                                    }
                          ),


                # Sub-tab 2: Wheelchair Accessibility
                 dcc.Tab(label='Wheelchair Accessibility', children=[
                    dcc.Graph(
                        id='accessibility-chart',
                        figure=px.pie(accessibility_data, values='Count', names='Accessibility',
                                      title="Wheelchair Accessibility Share")
                    )
                ], style={'backgroundColor': '#f0f8ff', 'border': '1px solid #d1e7ff', 'fontSize': '12px', 'padding': '5px'},
                   selected_style={'backgroundColor': '#d1e7ff', 'color': 'black', 'fontSize': '12px', 'padding': '5px'}),
                

                
                # Sub-tab 3: Registration Trends
                dcc.Tab(label='Registration Trends', children=[
                    dcc.Graph(
                        id='registration-chart',
                        figure=px.line(registration_data, x='Year', y='Registrations',
                                       title="Vehicle Registration Trends Over Years")
                    )
                ], style={'backgroundColor': '#f0f8ff', 'border': '1px solid #d1e7ff', 'fontSize': '12px', 'padding': '5px'},
                   selected_style={'backgroundColor': '#d1e7ff', 'color': 'black',  'fontSize': '12px', 'padding': '5px'}),



                # Sub-tab 4: Geographic Distribution
                 dcc.Tab(label='Geographic Distribution', children=[
                    dcc.Graph(
                        id='map-chart',
                        figure=px.scatter_mapbox(
                            map_data,
                            lat='Latitude',
                            lon='Longitude',
                            size='Registrations',
                            text='City',
                            title="Vehicle Registrations by City",
                            mapbox_style="open-street-map",
                            zoom=5
                        )
                    )
                ], style={'backgroundColor': '#f0f8ff', 'border': '1px solid #d1e7ff', 'fontSize': '12px', 'padding': '5px'},
                   selected_style={'backgroundColor': '#d1e7ff', 'color': 'black', 'fontSize': '12px', 'padding': '5px'})
            ],
               style={'backgroundColor': '#e3f2fd', 'borderRadius': '5px', 'padding': '10px'})
        ], style={'backgroundColor': '#fce4ec', 'borderRadius': '10px', 'fontSize': '18px'}),



        # Kia Vehicles Tab
        dcc.Tab(label='Kia Vehicles', children=[
            dcc.Graph(
                id='stacked-bar-chart',
                figure=px.bar(category_data, x='Category', y='Count', color='Sentiment',
                              barmode='stack', title="Sentiment by Review Category")
            )
        ], style={'backgroundColor': '#fce4ec', 'border': '1px solid #f8bbd0', 'fontSize': '18px'},
           selected_style={'backgroundColor': '#f8bbd0', 'color': 'black', 'border': '1px solid #ad1457', 'fontSize': '18px'})


          
    ],
       style={'backgroundColor': '#f8f9fa', 'borderRadius': '10px'})
])


# Callbacks for updating charts based on filters
@app.callback(
    Output('fuel-chart', 'figure'),
    Input('fuel-type-filter', 'value')
)
def update_fuel_chart(selected_fuel):
    if selected_fuel == 'All':
        filtered_data = fuel_data
    else:
        filtered_data = fuel_data[fuel_data['Fuel Source'] == selected_fuel]
    fig = px.bar(filtered_data, x='Fuel Source', y='Percentage', title="Fuel Type Distribution")
    return fig

@app.callback(
    Output('accessibility-chart', 'figure'),
    Input('accessibility-filter', 'value')
)
def update_accessibility_chart(selected_accessibility):
    if selected_accessibility == 'All':
        filtered_data = accessibility_data
    else:
        filtered_data = accessibility_data[accessibility_data['Accessibility'] == selected_accessibility]
    fig = px.pie(filtered_data, values='Count', names='Accessibility', title="Wheelchair Accessibility Share")
    return fig

@app.callback(
    Output('registration-chart', 'figure'),
    Input('year-range-slider', 'value')
)
def update_registration_chart(selected_years):
    filtered_data = registration_data[(registration_data['Year'] >= selected_years[0]) & (registration_data['Year'] <= selected_years[1])]
    fig = px.line(filtered_data, x='Year', y='Registrations', title="Vehicle Registration Trends Over Years")
    return fig

@app.callback(
    Output('map-chart', 'figure'),
    Input('year-range-slider', 'value')
)
def update_map_chart(selected_years):
    filtered_data = map_data[(map_data['Registrations'] >= selected_years[0]) & (map_data['Registrations'] <= selected_years[1])]
    fig = px.scatter_mapbox(
        filtered_data,
        lat='Latitude',
        lon='Longitude',
        size='Registrations',
        text='City',
        title="Vehicle Registrations by City",
        mapbox_style="open-street-map",
        zoom=5
    )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)