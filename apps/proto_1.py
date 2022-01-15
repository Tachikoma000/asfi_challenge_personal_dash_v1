# Import all required packages for this page
import dash
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html, State
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import math
from millify import millify

es = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=es)

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Label('Personal Dash Version1')
        ])
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
