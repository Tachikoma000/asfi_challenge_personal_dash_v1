# The purpose of this program is to test out and develop a prototype of a custom dashboard which provides personalized
# metrics for users of Olympus Protocol
# ==================================================
# Import libraries for this app
import dash
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html, State
from dash.dependencies import Input, Output
import base64
import requests
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import math
from millify import millify

# This is a single page app

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])

# Nav bar creation. Something simple for now
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink('Main', href='#')),
    ],
    brand='Ohmie Personal Metrics',
    brand_href='#',
    color='#2e343e',
    dark=True,
),

# create the app layout. Nothing too fancy, we just need a way to display the data from the users wallet

app.layout = dbc.Container([
    dbc.Row(navbar),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    dbc.Col(dbc.Label('Enter your address:', style={'padding': '0px'})),
                    dbc.Col(
                        dbc.Input(
                            id='address',
                            placeholder='0x0149f30...',
                            type='text',
                            value='0x0149f30573c638eef7e2786c04b666d1da0fb497',
                            size='sm',
                            style={'text-align': 'center'}
                        )
                    ),
                ]),
                dbc.CardBody(
                    dcc.Markdown(
                        '''
                        This tool provides advanced insight on your sOHM holdings in relation to Olympus Protocol.

                        Use this tool to view the following metrics:

                        - sOHM balance over time
                        - Your percentage of Olympus Market Cap
                        - Your wallets RFV in relation to treasury RFV
                        - Your wallets MV in relation to treasury MV
                        - Dollar value of your total sOHM holding over time
                        '''
                    )
                ),
                dbc.CardFooter('Click here to learn more about your metrics')
            ], style={'height': '100%'}, color='#273342', inverse=True)
        ], xs=12, sm=12, md=12, lg=4, xl=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='main_chart', style={"height": "100%", "width": "auto"})
                ], style={"height": "auto", "width": "auto"}),
            ], color='#273342', inverse=True)
        ], xs=12, sm=12, md=12, lg=8, xl=8)
    ], style={'padding': '10px'}),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Percentage of Market Cap'),
                dbc.CardBody([
                    dcc.Graph(id='main_chart_2', style={"height": "100%", "width": "auto"})
                ], style={"height": "auto", "width": "auto"})
            ], color='#273342', inverse=True)
        ], xs=12, sm=12, md=12, lg=4, xl=4),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Wallet Market Value and Risk Free Value'),
                dbc.CardBody([
                    dcc.Graph(id='main_chart_3', style={"height": "100%", "width": "auto"})
                ], style={"height": "auto", "width": "auto"})
            ], color='#273342', inverse=True)
        ], xs=12, sm=12, md=12, lg=4, xl=4),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Dollar value of sOHM over time'),
                dbc.CardBody([
                    dcc.Graph(id='main_chart_4', style={"height": "100%", "width": "auto"})
                ], style={"height": "auto", "width": "auto"})
            ], color='#273342', inverse=True)
        ], xs=12, sm=12, md=12, lg=4, xl=4),
    ], style={'padding': '10px'})
], style={'backgroundColor': '#2a3847'}, fluid=True)


if __name__ == '__main__':
    app.run_server(debug=True)
