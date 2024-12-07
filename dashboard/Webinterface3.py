
# -*- coding: utf-8 -*-

import pandas as pd
import dash
from dash import dcc, html
import plotly.graph_objs as go
import plotly.express as px

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Vehicle Insights Dashboard"

# Sample datasets
fuel_data = pd.DataFrame({'Fuel Source': ['Gasoline', 'Diesel', 'Electric', 'Hybrid'],
                          'Count': [1200, 450, 300, 150]})

accessibility_data = pd.DataFrame({'Accessibility': ['Wheelchair Accessible', 'Not Accessible'],
                                   'Count': [300, 1700]})

registration_data = pd.DataFrame({'Year': [2018, 2019, 2020, 2021, 2022],
                                   'Registrations': [400, 450, 500, 550, 600]})

map_data = pd.DataFrame({'City': ['Chicago', 'Springfield', 'Peoria'],
                         'Latitude': [41.8781, 39.7817, 40.6936],
                         'Longitude': [-87.6298, -89.6501, -89.5880],
                         'Registrations': [1000, 300, 200]})

sentiment_data = pd.DataFrame({'Sentiment Scores': [0.1, 0.5, 0.8, 0.2, 0.9, 0.4, 0.6, 0.7]})

category_data = pd.DataFrame({'Category': ['Driving Experience', 'Features', 'Value for Money', 'Issues', 'Other'],
                              'Positive': [120, 90, 80, 40, 30],
                              'Negative': [10, 20, 15, 50, 5]}).melt(id_vars='Category', var_name='Sentiment', value_name='Count')

# Define layout
app.layout = html.Div([
    html.H1("Vehicle Insights Dashboard", style={'textAlign': 'center'}),
    dcc.Tabs([
        dcc.Tab(label='Fuel Type Distribution', children=[
            dcc.Graph(
                id='fuel-chart',
                figure=px.bar(fuel_data, x='Fuel Source', y='Count', title="Fuel Type Distribution")
            )
        ]),
        dcc.Tab(label='Wheelchair Accessibility', children=[
            dcc.Graph(
                id='accessibility-chart',
                figure=px.pie(accessibility_data, values='Count', names='Accessibility',
                              title="Wheelchair Accessibility Share")
            )
        ]),
        dcc.Tab(label='Registration Trends', children=[
            dcc.Graph(
                id='registration-chart',
                figure=px.line(registration_data, x='Year', y='Registrations',
                               title="Vehicle Registration Trends Over Years")
            )
        ]),
        dcc.Tab(label='Geographic Distribution', children=[
            dcc.Graph(
                id='map-chart',
                figure=px.scatter_mapbox(map_data, lat='Latitude', lon='Longitude', size='Registrations',
                                         text='City', title="Vehicle Registrations by City",
                                         mapbox_style="open-street-map", zoom=5)
            )
        ]),
        dcc.Tab(label='Sentiment Distribution', children=[
            dcc.Graph(
                id='sentiment-chart',
                figure=px.histogram(sentiment_data, x='Sentiment Scores', nbins=5,
                                    title="Sentiment Score Distribution")
            )
        ]),
        dcc.Tab(label='Review Sentiments', children=[
            dcc.Graph(
                id='stacked-bar-chart',
                figure=px.bar(category_data, x='Category', y='Count', color='Sentiment',
                              barmode='stack', title="Sentiment by Review Category")
            )
        ]),
    ])
])

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
