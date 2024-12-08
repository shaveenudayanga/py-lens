import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import numpy as np

# Create a mock dataset
np.random.seed(42)
data = {
    "Vehicle Fuel Source": np.random.choice(["Gasoline", "Diesel", "Electric", "Hybrid"], size=100),
    "Wheelchair Accessible": np.random.choice(["Yes", "No"], size=100),
    "Vehicle Model Year": np.random.randint(2000, 2023, size=100),
    "Vehicle Make": np.random.choice(["Toyota", "Ford", "Chevrolet", "Honda"], size=100),
    "Vehicle Color": np.random.choice(["Red", "Blue", "Green", "Black", "White"], size=100),
}
vehicles_df = pd.DataFrame(data)

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server

# Example charts (mock data)
bar_chart = px.bar(
    vehicles_df,
    x="Vehicle Fuel Source",
    y=vehicles_df.index,
    title="Fuel Source Distribution"
)

pie_chart = px.pie(
    vehicles_df,
    names="Wheelchair Accessible",
    title="Wheelchair Accessibility"
)

line_chart = px.line(
    vehicles_df.groupby("Vehicle Model Year").size().reset_index(name="Counts"),
    x="Vehicle Model Year",
    y="Counts",
    title="Registrations Over Time"
)

scatter_chart = px.scatter(
    vehicles_df,
    x="Vehicle Model Year",
    y=vehicles_df.index,
    color="Vehicle Make",
    title="Scatter of Vehicle Makes by Year"
)

histogram_chart = px.histogram(
    vehicles_df,
    x="Vehicle Color",
    title="Vehicle Color Distribution"
)

box_chart = px.box(
    vehicles_df,
    x="Vehicle Fuel Source",
    y="Vehicle Model Year",
    title="Fuel Source vs Model Year"
)

# Define layout with colorful design and a header image
app.layout = html.Div(
    style={
        'backgroundColor': '#f0f8ff',
        'fontFamily': 'Arial, sans-serif',
        'padding': '20px'
    },
   children=[
        # Header Section
       html.Div(
            children=[
                html.H1("Vehicle Dashboard", style={
                    'textAlign': 'center',
                    'color': '#2c3e50',
                    'marginBottom': '20px'
                }),
                html.Img(src='', 
                         style={'width': '100%', 'borderRadius': '10px', 'marginBottom': '20px'})
            ]
        ),


        # Graphs Section
        html.Div(
            children=[
                html.Div(
                    dcc.Graph(figure=bar_chart, id="bar-chart"),
                    style={
                        'width': '48%', 
                        'display': 'inline-block', 
                        'padding': '10px',
                        'backgroundColor': '#eaf2f8',
                        'borderRadius': '10px',
                        'boxShadow': '0px 4px 6px rgba(0,0,0,0.1)'
                    }
                ),
                html.Div(
                    dcc.Graph(figure=pie_chart, id="pie-chart"),
                    style={
                        'width': '48%', 
                        'display': 'inline-block', 
                        'padding': '10px',
                        'backgroundColor': '#eafaf1',
                        'borderRadius': '10px',
                        'boxShadow': '0px 4px 6px rgba(0,0,0,0.1)'
                    }
                ),
                html.Div(
                    dcc.Graph(figure=line_chart, id="line-chart"),
                    style={
                        'width': '48%', 
                        'display': 'inline-block', 
                        'padding': '10px',
                        'backgroundColor': '#fef9e7',
                        'borderRadius': '10px',
                        'boxShadow': '0px 4px 6px rgba(0,0,0,0.1)'
                    }
                ),
                html.Div(
                    dcc.Graph(figure=scatter_chart, id="scatter-chart"),
                    style={
                        'width': '48%', 
                        'display': 'inline-block', 
                        'padding': '10px',
                        'backgroundColor': '#fdebd0',
                        'borderRadius': '10px',
                        'boxShadow': '0px 4px 6px rgba(0,0,0,0.1)'
                    }
                ),
                html.Div(
                    dcc.Graph(figure=histogram_chart, id="histogram-chart"),
                    style={
                        'width': '48%', 
                        'display': 'inline-block', 
                        'padding': '10px',
                        'backgroundColor': '#fbeee6',
                        'borderRadius': '10px',
                        'boxShadow': '0px 4px 6px rgba(0,0,0,0.1)'
                    }
                ),
                html.Div(
                    dcc.Graph(figure=box_chart, id="box-chart"),
                    style={
                        'width': '48%', 
                        'display': 'inline-block', 
                        'padding': '10px',
                        'backgroundColor': '#f5eef8',
                        'borderRadius': '10px',
                        'boxShadow': '0px 4px 6px rgba(0,0,0,0.1)'
                    }
                ),
            ],
            style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'space-between'}
        )
    ]
)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)