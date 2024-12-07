import dash
from dash import dcc, html
import plotly.graph_objs as go

# Sample data for car sales
years = list(range(2010, 2024))
total_income = [50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115]
total_policies = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
net_ratio = [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75]
net_income = [5, 8, 12, 16, 21, 26, 32, 38, 45, 52, 60, 68, 77, 86]
surplus_income = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

app = dash.Dash(__name__)

app.layout = html.Div(style={'backgroundColor': '#1e1e2f', 'color': '#ffffff', 'padding': '20px'}, children=[
    html.H1('Car Sales 2010-2023', style={'textAlign': 'center'}),
    
    html.Div([
        html.Div([
            html.H2('Total Income | 2010-2023'),
            html.H3(f'${sum(total_income)}M', style={'fontSize': '50px'})
        ], style={'width': '48%', 'display': 'inline-block', 'padding': '20px', 'backgroundColor': '#2e2e3f'}),
        
        html.Div([
            html.H2('Total Number of Car Sales | 2010-2023'),
            html.H3(f'{sum(total_policies)}K', style={'fontSize': '50px'})
        ], style={'width': '48%', 'display': 'inline-block', 'padding': '20px', 'backgroundColor': '#2e2e3f'}),
    ]),
    
    html.Div([
        dcc.Graph(
            id='net-income-ratio',
            figure={
                'data': [
                    go.Bar(
                        x=years,
                        y=net_ratio,
                        name='Net Ratio',
                        marker={'color': '#00cc96'}
                    ),
                    go.Bar(
                        x=years,
                        y=net_income,
                        name='Net Income',
                        marker={'color': '#636efa'}
                    )
                ],
                'layout': go.Layout(
                    title='Net Income Ratio | 2010-2023',
                    barmode='group',
                    plot_bgcolor='#1e1e2f',
                    paper_bgcolor='#1e1e2f',
                    font={'color': '#ffffff'}
                )
            }
        )
    ]),
    
    html.Div([
        dcc.Graph(
            id='surplus-income',
            figure={
                'data': [
                    go.Scatter(
                        x=years,
                        y=surplus_income,
                        mode='lines+markers',
                        name='Surplus Income',
                        line={'color': '#00cc96'}
                    )
                ],
                'layout': go.Layout(
                    title='Surplus Income | 2010-2023',
                    plot_bgcolor='#1e1e2f',
                    paper_bgcolor='#1e1e2f',
                    font={'color': '#ffffff'}
                )
            }
        )
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
