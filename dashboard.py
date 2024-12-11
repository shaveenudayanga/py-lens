# -*- coding: utf-8 -*-
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
import seaborn as sns




# Mock Data for Visualization
np.random.seed(42)

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

#--------------------------------------------------------------------------------------------------

# Load Vehicle Data
vehicle_data = pd.read_csv("final_data_output.csv")

# Group by 'Status' and 'Company Name' columns
grouped_Status_Company_Name = vehicle_data.groupby(['Status', 'Company Name']).size().reset_index(name='count')

# Group by 'Vehicle Fuel Source' and 'Vehicle Make' columns
grouped_fuel =  vehicle_data.groupby(['Vehicle Fuel Source', 'Vehicle Make']).size().reset_index(name='count')
#Calculate percentage
grouped_fuel['Percentage'] = (grouped_fuel['count'] / grouped_fuel['count'].sum()) * 100

# Group the data by 'Wheelchair Accessible', 'Vehicle Make', and 'Vehicle Model', and calculate counts
grouped_accessibility_data = vehicle_data.groupby(['Wheelchair Accessible', 'Vehicle Make', 'Vehicle Model']).size().reset_index(name='Count')
custom_labels = {
    "N": "Not Accessible",
    "Y": "Accessible",
}

# Replace 'Wheelchair Accessible' values with custom labels
grouped_accessibility_data['Wheelchair Accessible'] = grouped_accessibility_data['Wheelchair Accessible'].map(custom_labels)

# Group by 'Status' and 'Vehicle Fuel Source' columns
grouped_status_fuel_source = vehicle_data.groupby(['Status', 'Vehicle Fuel Source']).size().reset_index(name='count')

# Pivot the data to create a matrix
heatmap_data = grouped_status_fuel_source.pivot(index='Status', columns='Vehicle Fuel Source', values='count')

#--------------------------------------------------------------------------------------------------

# Load Reviews Data
classified_reviews = pd.read_csv("classified_sentiment_reviews.csv")  # Make sure this contains 'talks_about' and 'sentiment'
classified_reviews['talks_about'] = classified_reviews['talks_about'].str.strip().str.lower()

# Define custom labels as a mapping
custom_labels = {
    "talks about driving experience": "Driving Experience",
    "talks about features": "Features",
    "talks about value for money": "Value for Money",
    "talks about issues": "Issues",
    "other": "Other"
}

# Replace 'talks_about' values with custom labels
classified_reviews['talks_about'] = classified_reviews['talks_about'].map(custom_labels)

# Prepare the data for the bar chart
grouped_talks_about_sentiment = classified_reviews.groupby(['talks_about', 'sentiment']).size().reset_index(name='count')

# Define custom order for the x-axis
custom_order = [
    "Driving Experience",
    "Features",
    "Value for Money",
    "Issues",
    "Other"
]

#--------------------------------------------------------------------------------------------------

# Create the fuel pie chart
fuelPieChart=px.pie(
        grouped_fuel, values='Percentage',
        names='Vehicle Fuel Source',
        title="Fuel Type Distribution",
)

# Create the accessibility treemap
accessibilityTreeMap = px.treemap(
                            grouped_accessibility_data,
                            path=['Wheelchair Accessible', 'Vehicle Make', 'Vehicle Model'],
                            values='Count',
                            labels={'Wheelchair Accessible': 'Wheelchair Accessible',
                                    'Vehicle Make': 'Vehicle Make'},
                            title='Treemap of Vehicle Data by Accessibility and Make'
                        )          

# Create the heatmap figure
heatMap = px.imshow(
    heatmap_data,
    text_auto=True,  # Display numbers inside heatmap cells
    color_continuous_scale='Blues',  # Set color scale
    title='Heatmap of Vehicle Status by Fuel Source'
)

# Create the stacked bar chart
stackedBarChart = px.bar(
                    grouped_Status_Company_Name,
                    x='Status',
                    y='count',
                    color='Company Name',
                    barmode='group',
                    labels={'Status': 'Status', 'count': 'Count'},
                    title='Vehicle Status Distribution by Company Name',
                    )

#-------------------------------------------------------------------------------------------

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server

# Main Dashboard Layout
app.layout = html.Div([
    html.Header([
    html.H1("Vehicle Insights Dashboard", style={'textAlign': 'center', 'marginBottom': '20px', 'marginTop': '20px', 'color': 'white'}),
    ], style={'background': 'linear-gradient(to bottom, #05414e, #026c72)', 'padding': '20px'}),

    # Tabs for Main Dashboard
    dcc.Tabs([

        # Vehicle Details Tab
        dcc.Tab(label='Vehicle Details', children=[
            
            # Filters-------------------------------------------------------------------------------------------
            html.Div([
                html.Label('Select Year Range:', className='label'),
                dcc.RangeSlider(
                    id='year-range-slider',
                    min=2000,
                    max=2022,
                    step=1,
                    marks={year: str(year) for year in range(2000, 2023)},
                    value=[2000, 2022],
                    className='slider'
                ),
                html.Div([
                    html.Label('Select Fuel Type:', className='label'),
                    dcc.Dropdown(
                        id='fuel-type-filter',
                        options=[{'label': 'All', 'value': 'All'}] or [{'label': ft, 'value': ft} for ft in vehicle_data['Vehicle Fuel Source'].unique()],
                        placeholder="Filter by Fuel Type",
                        multi=True,  # Allow multiple selections
                        className='dropdown',
                        style={'width': '200px', 'marginRight': '50px'}
                    ),
                    html.Label('Select Accessibility:', className='label'),
                    dcc.Dropdown(
                        id='accessibility-filter',
                        options=[{'label': 'All', 'value': 'All'}] + [{'label': acc, 'value': acc} for acc in vehicle_data['Wheelchair Accessible'].unique()],
                        value='All',
                        clearable=False,
                        className='dropdown',
                        style={'width': '100px', 'marginRight': '50px'}
                    ),
                    html.Label("Select Vehicle Make"),
                    dcc.Dropdown(
                        id='vehicle-make-filter',
                        options=[{'label': 'All', 'value': 'All'}] or [{'label': vm, 'value': vm} for vm in vehicle_data['Vehicle Make'].unique()],
                        placeholder="Filter by Vehicle Make",
                        multi=True,  # Allow multiple selections
                        style={'width': '200px'}
                    )
                ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'padding': '20px', 'gap': '20px'})
            ], style={'padding': '30px'}),

            # Graphs-------------------------------------------------------------------------------------------

            # Fuel Type Distribution Pie Chart
            html.Div([
                dcc.Graph(
                    id='fuel-chart',
                    figure=fuelPieChart,
                    config={'displayModeBar': False},
                    style={'height': '600px', 'width': '100%'}
                    )
            ], style={'padding': '0 20px'}),

            # Accessibility Treemap Chart
            html.Div([
                dcc.Graph(
                    id='accessibility-chart',
                    figure=accessibilityTreeMap,
                    config={'displayModeBar': False},
                    style={'height': '600px', 'width': '100%'}
                    )
            ], style={'padding': '0 20px'}),

            # Status and Fuel Source Heatmap Chart
            html.Div([
                dcc.Graph(
                    id='status-fuel-source-chart',
                    figure=heatMap,
                    config={'displayModeBar': False},
                    style={'height': '600px', 'width': '100%'}
                    )
            ], style={'padding': '0 20px'}),

            # Vehicle Status Distribution Stacked Bar Chart  
            html.Div([
                dcc.Graph(
                    id='status-company-name-chart',
                    figure = stackedBarChart
                )
            ], style={'padding': '0 20px'})


        ], style={'backgroundColor': '#33a0a6', 'border': '0px', 'fontSize': '18px'},
           selected_style={'backgroundColor': '#207f85', 'color': 'white', 'border': '0px', 'fontSize': '18px'}),

        # Kia Vehicles Tab
        dcc.Tab(label='Kia Vehicles', children=[
            dcc.Graph(
                id='stacked-bar-chart',
                figure = px.bar(
                    grouped_talks_about_sentiment,
                    x='talks_about',
                    y='count',
                    color='sentiment',
                    barmode='group',
                    labels={'talks_about': 'Talks About', 'count': 'Count'},
                    title='Sentiment Distribution by Category',
                    category_orders={'talks_about': custom_order}
                    )
                )
        ], style={'backgroundColor': '#33a0a6', 'border': '0px', 'fontSize': '18px'},
           selected_style={'backgroundColor': '#207f85', 'color': 'white', 'border': '0px', 'fontSize': '18px'})
    ], style={'color': 'black', 'fontSize': '18px'}) 
], style={'margin': '0', 'padding': '0', 'boxSizing': 'border-box', 'fontFamily': 'Arial, sans-serif'})


# # Callback to update the heatmap based on filters
# @app.callback(
#     Output('status-fuel-source-chart', 'figure'),
#     [Input('fuel-type-filter', 'value'),
#      Input('vehicle-make-filter', 'value')]
# )
# def update_heatmap(selected_fuel_types, selected_vehicle_makes):
#     # Filter data based on selections
#     filtered_data = vehicle_data
#     if selected_fuel_types:
#         filtered_data = filtered_data[filtered_data['Vehicle Fuel Source'].isin(selected_fuel_types)]
#     if selected_vehicle_makes:
#         filtered_data = filtered_data[filtered_data['Vehicle Make'].isin(selected_vehicle_makes)]

# Callbacks for updating charts based on filters
# Callback to update the fuel chart based on selected fuel type
# @app.callback(
#     Output('fuel-chart', 'figure'),
#     Input('fuel-type-filter', 'value')
# )
# def update_fuel_chart(selected_fuel):
#     if selected_fuel == 'All':
#         filtered_data = fuel_data
#     else:
#         filtered_data = fuel_data[fuel_data['Fuel Source'] == selected_fuel]
#     fig = px.bar(filtered_data, x='Fuel Source', y='Percentage', title="Fuel Type Distribution")
#     return fig

# Callback to update the accessibility chart based on selected accessibility option
# @app.callback(
#     Output('accessibility-chart', 'figure'),
#     Input('accessibility-filter', 'value')
# )
# def update_accessibility_chart(selected_accessibility):
#     if selected_accessibility == 'All':
#         filtered_data = accessibility_data
#     else:
#         filtered_data = accessibility_data[accessibility_data['Accessibility'] == selected_accessibility]
#     fig = px.pie(filtered_data, values='Count', names='Accessibility', title="Wheelchair Accessibility Share")
#     return fig

# Callback to update the registration chart based on selected year range
# @app.callback(
#     Output('registration-chart', 'figure'),
#     Input('year-range-slider', 'value')
# )
# def update_registration_chart(selected_years):
#     filtered_data = registration_data[(registration_data['Year'] >= selected_years[0]) & (registration_data['Year'] <= selected_years[1])]
#     fig = px.line(filtered_data, x='Year', y='Registrations', title="Vehicle Registration Trends Over Years")
#     return fig

# # Callback to update the map chart based on selected year range
# @app.callback(
#     Output('status-company-name-chart', 'figure'),
#     Input('year-range-slider', 'value')
# )
# def update_map_chart(selected_years):
#     filtered_data = map_data[(map_data['Registrations'] >= selected_years[0]) & (map_data['Registrations'] <= selected_years[1])]
#     fig = px.scatter_mapbox(
#         filtered_data,
#         lat='Latitude',
#         lon='Longitude',
#         size='Registrations',
#         text='City',
#         title="Vehicle Registrations by City",
#         mapbox_style="open-street-map",
#         zoom=5
#     )
#     return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
