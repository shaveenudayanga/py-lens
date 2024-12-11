# -*- coding: utf-8 -*-
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

#--------------------------------------------------------------------------------------------------

# Load Vehicle Data
vehicle_data = pd.read_csv("final_data_output.csv")

custom_labels = {
    "N": "Not Accessible",
    "Y": "Accessible",
}

# Replace 'Wheelchair Accessible' values with custom labels
vehicle_data['Wheelchair Accessible'] = vehicle_data['Wheelchair Accessible'].map(custom_labels)
    
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

def show_graphs(vehicle_data):

    # Create the fuel pie chart
    # Group by 'Vehicle Fuel Source' and 'Vehicle Make' columns
    grouped_fuel =  vehicle_data.groupby(['Vehicle Fuel Source', 'Vehicle Make']).size().reset_index(name='count')
    #Calculate percentage
    grouped_fuel['Percentage'] = (grouped_fuel['count'] / grouped_fuel['count'].sum()) * 100
    # Create the pie chart
    fuelPieChart=px.pie(
            grouped_fuel, values='Percentage',
            names='Vehicle Fuel Source',
            title="Fuel Type Distribution",
    )

    # Create the accessibility treemap
    # Group the data by 'Wheelchair Accessible', 'Vehicle Make', and 'Vehicle Model', and calculate counts
    grouped_accessibility_data = vehicle_data.groupby(['Wheelchair Accessible', 'Vehicle Make', 'Vehicle Model']).size().reset_index(name='Count')
    # Create the treemap
    accessibilityTreeMap = px.treemap(
                                grouped_accessibility_data,
                                path=['Wheelchair Accessible', 'Vehicle Make', 'Vehicle Model'],
                                values='Count',
                                labels={'Wheelchair Accessible': 'Wheelchair Accessible',
                                        'Vehicle Make': 'Vehicle Make'},
                                title='Treemap of Vehicle Data by Accessibility and Make'
                            ) 
             
    # Create the heatmap of vehicle status by fuel source
    # Group by 'Status' and 'Vehicle Fuel Source' columns
    grouped_status_fuel_source = vehicle_data.groupby(['Status', 'Vehicle Fuel Source']).size().reset_index(name='count')
    # Pivot the data to create a matrix
    heatmap_data = grouped_status_fuel_source.pivot(index='Status', columns='Vehicle Fuel Source', values='count')
    # Create the heatmap figure
    heatMap = px.imshow(
        heatmap_data,
        text_auto=True,  # Display numbers inside heatmap cells
        color_continuous_scale='Blues',  # Set color scale
        title='Heatmap of Vehicle Status by Fuel Source'
    )

    # Create the stacked bar chart of vehicle status by company name
    # Group by 'Status' and 'Company Name' columns
    grouped_Status_Company_Name = vehicle_data.groupby(['Status', 'Company Name']).size().reset_index(name='count')
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
    
    return fuelPieChart, accessibilityTreeMap, heatMap, stackedBarChart

# Call the function to show the graphs
fuelPieChart, accessibilityTreeMap, heatMap, stackedBarChart = show_graphs(vehicle_data)

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
                    min=int(vehicle_data['Vehicle Model Year'].min()),
                    max=int(vehicle_data['Vehicle Model Year'].max()),
                    step=1,
                    marks={year: str(year) for year in range(int(vehicle_data['Vehicle Model Year'].min()),
                                                             int(vehicle_data['Vehicle Model Year'].max()) + 1, 2)},
                    value=[int(vehicle_data['Vehicle Model Year'].min()), int(vehicle_data['Vehicle Model Year'].max())],
                    className='slider'
                ),
                html.Div([
                    html.Label('Select Fuel Type:', className='label'),
                    dcc.Dropdown(
                        id='fuel-type-filter',
                        options=[{'label': ft, 'value': ft} for ft in vehicle_data['Vehicle Fuel Source'].unique()],
                        placeholder="Filter by Fuel Type",
                        multi=True,  # Allow multiple selections
                        className='dropdown',
                        style={'width': '200px', 'marginRight': '50px'}
                    ),
                    html.Label('Select Wheelchair Accessibility:', className='label'),
                    dcc.Dropdown(
                        id='accessibility-filter',
                        placeholder="All",
                        options=[{'label': acc, 'value': acc} for acc in vehicle_data['Wheelchair Accessible'].unique()],
                        clearable=True,
                        className='dropdown',
                        style={'width': '150px', 'marginRight': '50px'}
                    ),
                    html.Label("Select Vehicle Make", className='label'),
                    dcc.Dropdown(
                        id='vehicle-make-filter',
                        options=[{'label': vm, 'value': vm} for vm in vehicle_data['Vehicle Make'].unique()],
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
                # dcc.Graph(
                #     id='status-company-name-chart',
                #     figure = stackedBarChart
                # )
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


#-------------------------------------------------------------------------------------------

# Callbacks for updating charts based on filters
@app.callback(
    [Output('fuel-chart', 'figure'),
     Output('accessibility-chart', 'figure'),
     Output('status-fuel-source-chart', 'figure')
     ],
    [Input('year-range-slider', 'value'),
     Input('fuel-type-filter', 'value'),
     Input('accessibility-filter', 'value'),
     Input('vehicle-make-filter', 'value')]
)

# Function to update the charts based on the selected filters
def update_fuel_chart(selected_year_range, selected_fuel_types, selected_accessibility, selected_vehicle_makes):
    filtered_data = vehicle_data    # Initialize the filtered data with the original data
    if selected_year_range:
        year_range = list(range(selected_year_range[0], selected_year_range[1] + 1)) # Create a list of years
        filtered_data = filtered_data[filtered_data['Vehicle Model Year'].isin(year_range)]
    if selected_fuel_types:
        filtered_data = filtered_data[filtered_data['Vehicle Fuel Source'].isin(selected_fuel_types)]
    if selected_accessibility:
        filtered_data = filtered_data[filtered_data['Wheelchair Accessible'].isin([selected_accessibility])]
    if selected_vehicle_makes:
        filtered_data = filtered_data[filtered_data['Vehicle Make'].isin(selected_vehicle_makes)]
    
    # Call the function to show the graphs
    fuelPieChart, accessibilityTreeMap, heatMap, stackedBarChart = show_graphs(filtered_data)
    # Return the updated figures
    return fuelPieChart, accessibilityTreeMap, heatMap

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
