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

from subgrounds.dash_wrappers import Graph
from subgrounds.plotly_wrappers import Figure, Scatter, Indicator

from olympus_subgrounds import protocol_metrics_1year, last_metric, sg

# This is a single page app

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])

# Nav bar creation. Something simple for now
navbar = dbc.NavbarSimple(
    children=[],
    brand='Playgrounds Analytics',
    brand_href='#',
    color='#2e343e',
    dark=True,
    fluid=True,
    style={'font-size': '20px',
           'justify - content': 'stretch'
           }
),

# create the app layout. Nothing too fancy, we just need a way to display the data from the users wallet

app.layout = dbc.Container([
    dbc.Row(navbar),
    dbc.Row([
        dbc.Col([
            dbc.Label('Personal Metrics',
                      style={'font-style': 'normal',
                             'font-weight': '600',
                             'font-size': '64px',
                             'line-height': '96px',
                             'color': '#FFFFFF'
                             }, xs=12, sm=12, md=12, lg=6, xl=6)
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Welcome to your personal metrics explorer tool'),
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
                dbc.CardHeader(
                    dbc.Row([
                        dbc.Col(dbc.Label('Enter your address:', style={'padding': '0px'})),
                        dbc.Col(
                            dbc.Input(
                                id='address',
                                placeholder='0x0149f30...',
                                type='text',
                                value='0x0149f30573c638eef7e2786c04b666d1da0fb497',
                                size='sm',
                                style={'text-align': 'center'}
                            ), xs=12, sm=12, md=12, lg=10, xl=10
                        )
                    ])
                ),
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
    ], style={'padding': '10px'}),
    dbc.Row([
        dbc.Col([
            dbc.Label('Protocol Metrics',
                      style={'font-style': 'normal',
                             'font-weight': '600',
                             'font-size': '64px',
                             'line-height': '96px',
                             'color': '#FFFFFF'
                             }, xs=12, sm=12, md=12, lg=6, xl=6)
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    Graph(Figure(
                        subgrounds=sg,
                        traces=[
                            Indicator(value=last_metric.marketCap, title='Market Cap', domain={'row': 0, 'column': 0},
                                      number={'valueformat': '$,.0f'})]
                    )),
                ]),
            ]),
        ], xs=12, sm=12, md=12, lg=3, xl=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    Graph(Figure(
                        subgrounds=sg,
                        traces=[
                            Indicator(value=last_metric.ohmPrice, title='Price', domain={'row': 0, 'column': 1},
                                      number={'valueformat': '$,.2f'})]
                    )),
                ]),
            ]),
        ], xs=12, sm=12, md=12, lg=3, xl=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H1('Current APY', className='display-3', style={'text-align': 'center'}),
                    html.Hr(className='my-2'),
                    html.H1(
                        millify(
                            sg.execute(
                                sg.mk_request([
                                    last_metric.currentAPY
                                ])
                            )[0]['protocolMetrics'][0]['currentAPY'],
                            precision=2),
                        style={'text-align': 'center'}
                    ),
                ]),
            ]),
        ], xs=12, sm=12, md=12, lg=3, xl=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H1('Current APY', className='display-3', style={'text-align': 'center'}),
                    html.Hr(className='my-2'),
                    html.H1(
                        millify(
                            sg.execute(
                                sg.mk_request([
                                    last_metric.currentAPY
                                ])
                            )[0]['protocolMetrics'][0]['currentAPY'],
                            precision=2),
                        style={'text-align': 'center'}
                    ),
                ]),
            ]),
        ], xs=12, sm=12, md=12, lg=3, xl=3),
    ]),
    dbc.Row([
        dbc.Col([dbc.Card([
            dbc.CardHeader([
                dbc.Row([
                    dbc.Col([
                        dbc.Label('Risk Free Value of Treasury Assets: '),
                    ]),
                    dbc.Col([
                        millify(
                            sg.execute(
                                sg.mk_request([
                                    last_metric.treasuryRiskFreeValue
                                ])
                            )[0]['protocolMetrics'][0]['treasuryRiskFreeValue'],
                            precision=2)
                    ]),
                ]),
            ], style={'color': '#FFFFFF',
                      'font-weight': '500',
                      'font-size': '24px',
                      'font-style': 'normal'}),
            dbc.CardBody([
                Graph(Figure(
                    subgrounds=sg,
                    traces=[
                        # Risk free value treasury assets
                        Scatter(
                            name='lusd_rfv',
                            x=protocol_metrics_1year.datetime,
                            y=protocol_metrics_1year.treasuryLusdRiskFreeValue,
                            mode='lines',
                            line={'width': 0.5, 'color': 'rgb(0, 128, 255)'},
                            stackgroup='one',
                        ),
                        Scatter(
                            name='frax_rfv',
                            x=protocol_metrics_1year.datetime,
                            y=protocol_metrics_1year.treasuryFraxRiskFreeValue,
                            mode='lines',
                            line={'width': 0.5, 'color': 'rgb(0, 0, 64)'},
                            stackgroup='one',
                        ),
                        Scatter(
                            name='dai_rfv',
                            x=protocol_metrics_1year.datetime,
                            y=protocol_metrics_1year.treasuryDaiRiskFreeValue,
                            mode='lines',
                            line={'width': 0.5, 'color': 'rgb(255, 128, 64)'},
                            stackgroup='one',
                        ),
                    ],
                    layout={
                        'showlegend': True,
                        'xaxis': {'linewidth': 0.1, 'linecolor': '#31333F', 'color': 'white', 'showgrid': False},
                        'yaxis': {'type': 'linear', 'linewidth': 0.1, 'linecolor': '#31333F', 'color': 'white'},
                        'legend.font.color': 'white',
                        'paper_bgcolor': 'rgba(0,0,0,0)',
                        'plot_bgcolor': 'rgba(0,0,0,0)',
                    }
                ))
            ]),
            dbc.CardFooter('Learn more')
        ], style={'height': '100%'}, color='#273342', inverse=True),
        ], xs=12, sm=12, md=12, lg=6, xl=6),
        dbc.Col([dbc.Card([
            dbc.CardHeader([
                dbc.Row([
                    dbc.Col([
                        dbc.Label('Market Value of Treasury Assets: '),
                    ]),
                    dbc.Col([
                        millify(
                            sg.execute(
                                sg.mk_request([
                                    last_metric.treasuryMarketValue
                                ])
                            )[0]['protocolMetrics'][0]['treasuryMarketValue'],
                            precision=2)
                    ]),
                ]),
            ], style={'color': '#FFFFFF',
                      'font-weight': '500',
                      'font-size': '24px',
                      'font-style': 'normal'}),
            dbc.CardBody([
                Graph(Figure(
                    subgrounds=sg,
                    traces=[
                        # Market value treasury assets
                        Scatter(
                            name='xsushi_mv',
                            x=protocol_metrics_1year.datetime,
                            y=protocol_metrics_1year.treasuryXsushiMarketValue,
                            mode='lines',
                            line={'width': 0.5, 'color': 'rgb(255, 0, 255)'},
                            stackgroup='one',
                        ),
                        Scatter(
                            name='cvx_mv',
                            x=protocol_metrics_1year.datetime,
                            y=protocol_metrics_1year.treasuryCVXMarketValue,
                            mode='lines',
                            line={'width': 0.5, 'color': 'rgb(0, 128, 128)'},
                            stackgroup='one',
                        ),
                        Scatter(
                            name='weth_mv',
                            x=protocol_metrics_1year.datetime,
                            y=protocol_metrics_1year.treasuryWETHMarketValue,
                            mode='lines',
                            line={'width': 0.5, 'color': 'rgb(128, 0, 128)'},
                            stackgroup='one',
                        ),
                        Scatter(
                            name='lusd_mv',
                            x=protocol_metrics_1year.datetime,
                            y=protocol_metrics_1year.treasuryLusdMarketValue,
                            mode='lines',
                            line={'width': 0.5, 'color': 'rgb(0, 128, 255)'},
                            stackgroup='one',
                        ),
                        Scatter(
                            name='frax_mv',
                            x=protocol_metrics_1year.datetime,
                            y=protocol_metrics_1year.treasuryFraxMarketValue,
                            mode='lines',
                            line={'width': 0.5, 'color': 'rgb(0, 0, 64)'},
                            stackgroup='one',
                        ),
                        Scatter(
                            name='dai_mv',
                            x=protocol_metrics_1year.datetime,
                            y=protocol_metrics_1year.treasuryDaiMarketValue,
                            mode='lines',
                            line={'width': 0.5, 'color': 'rgb(255, 128, 64)'},
                            stackgroup='one',
                        )
                    ],
                    layout={
                        'showlegend': True,
                        'xaxis': {'linewidth': 0.1, 'linecolor': '#31333F', 'color': 'white', 'showgrid': False},
                        'yaxis': {'type': 'linear', 'linewidth': 0.1, 'linecolor': '#31333F', 'color': 'white'},
                        'legend.font.color': 'white',
                        'paper_bgcolor': 'rgba(0,0,0,0)',
                        'plot_bgcolor': 'rgba(0,0,0,0)',
                    }
                ))
            ]),
            dbc.CardFooter('Learn more')
        ], style={'height': '100%'}, color='#273342', inverse=True),
        ], xs=12, sm=12, md=12, lg=6, xl=6)
    ], style={'padding': '10px'}),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label('OHM Market Cap: '),
                        ]),
                        dbc.Col([
                            millify(
                                sg.execute(
                                    sg.mk_request([
                                        protocol_metrics_1year.marketCap
                                    ])
                                )[0]['protocolMetrics'][0]['marketCap'],
                                precision=2)
                        ]),
                    ]),
                ], style={'color': '#FFFFFF',
                          'font-weight': '500',
                          'font-size': '24px',
                          'font-style': 'normal'}),
                dbc.CardBody([
                    Graph(Figure(
                        subgrounds=sg,
                        traces=[
                            Scatter(
                                name='OHM Market Cap',
                                x=protocol_metrics_1year.datetime,
                                y=protocol_metrics_1year.marketCap
                            )
                        ],
                        layout={
                            'showlegend': True,
                            'xaxis': {'linewidth': 0.1, 'linecolor': '#31333F', 'color': 'white', 'showgrid': False},
                            'yaxis': {'type': 'linear', 'linewidth': 0.1, 'linecolor': '#31333F', 'color': 'white'},
                            'legend.font.color': 'white',
                            'paper_bgcolor': 'rgba(0,0,0,0)',
                            'plot_bgcolor': 'rgba(0,0,0,0)',
                        }
                    ))
                ]),
                dbc.CardFooter('Learn more')
            ], style={'height': '100%'}, color='#273342', inverse=True)
        ], xs=12, sm=12, md=12, lg=6, xl=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label('Staked OHM (%)'),
                        ]),
                    ]),
                ], style={'color': '#FFFFFF',
                      'font-weight': '500',
                      'font-size': '24px',
                      'font-style': 'normal'}),
                dbc.CardBody([
                    Graph(Figure(
                        subgrounds=sg,
                        traces=[
                            Scatter(
                                name='staked_supply_percent',
                                x=protocol_metrics_1year.datetime,
                                y=protocol_metrics_1year.staked_supply_percent,
                                mode='lines',
                                line={'width': 0.5, 'color': 'rgb(0, 255, 0)'},
                                stackgroup='one',
                            ),
                            Scatter(
                                name='unstaked_supply_percent',
                                x=protocol_metrics_1year.datetime,
                                y=protocol_metrics_1year.unstaked_supply_percent,
                                mode='lines',
                                line={'width': 0.5, 'color': 'rgb(255, 0, 0)'},
                                stackgroup='one',
                            )
                        ],
                        layout={
                            'title': {'text': 'Staked OHM (%)'},
                            'yaxis': {
                                'type': 'linear',
                                'range': [1, 100],
                                'ticksuffix': '%',
                                'linewidth': 0.1, 'linecolor': '#31333F', 'color': 'white'
                            },
                            'showlegend': True,
                            'xaxis': {'linewidth': 0.1, 'linecolor': '#31333F', 'color': 'white', 'showgrid': False},
                            'legend.font.color': 'white',
                            'paper_bgcolor': 'rgba(0,0,0,0)',
                            'plot_bgcolor': 'rgba(0,0,0,0)',
                        }
                    ))
                ]),
                dbc.CardFooter('Learn more')
            ], style={'height': '100%'}, color='#273342', inverse=True),
        ], xs=12, sm=12, md=12, lg=6, xl=6)
    ], style={'padding': '10px'}),
    html.Footer('Powered by Subgrounds',
                style={'backgrounds-color': '#2e343e',
                       'color': 'white',
                       'font-size': '20px',
                       'padding': '10px'
                       }),
], style={'backgroundColor': '#2e343e'}, fluid=True)


def run_query(query):
    request = requests.post('https://api.thegraph.com/subgraphs/id/QmdXcjjJUpzwRXjQY2XncNoSMgbvtDPTZxaB9k3vRki85L'
                            '',
                            json={'query': query})
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception('Query failed. return code is {}.      {}'.format(request.status_code, query))


@app.callback([
    Output(component_id='main_chart', component_property='figure'),
    Output(component_id='main_chart_2', component_property='figure'),
    Output(component_id='main_chart_3', component_property='figure'),
    Output(component_id='main_chart_4', component_property='figure'),
    Input(component_id='address', component_property='value')
])
def personal_metrics_main(ohmie_address):
    print(ohmie_address)
    # Step 1 Create a query using graph API
    query = """
    {
    ohmieBalances(first: 100, orderBy: timestamp, orderDirection: asc,
    where: {ohmie:"%s"}){
    timestamp
    sohmIndexed
    sohmBalance
    }
    rebases(first: 100, orderBy: timestamp, orderDirection: asc)
    {
    timestamp
    currentIndex
    }
    protocolMetrics(first: 100, orderBy: timestamp, orderDirection: asc) 
    {
    timestamp
    ohmCirculatingSupply
    marketCap
    treasuryRiskFreeValue
    treasuryMarketValue
    }
    }
    """ % ohmie_address
    result = run_query(query)

    # Now we create a function that will query the custom graph schema we have developed specifically for this prototype
    # this will be the user address field
    results_ohmieBalance = result['data']['ohmieBalances']
    results_rebases = result['data']['rebases']
    results_treasury = result['data']['protocolMetrics']

    ohmieBalances_df = pd.DataFrame(results_ohmieBalance)
    rebases_df = pd.DataFrame(results_rebases)
    treasury_df = pd.DataFrame(results_treasury)

    ohmieBalances_df['dateTime'] = pd.to_datetime(ohmieBalances_df.timestamp, unit='s')
    ohmieBalances_df['dateTime'] = ohmieBalances_df['dateTime'].dt.date
    ohmieBalances_df = ohmieBalances_df.set_index('timestamp')
    ohmieBalances_df = ohmieBalances_df.rename(columns=str.lower)

    rebases_df['dateTime'] = pd.to_datetime(rebases_df.timestamp, unit='s')
    rebases_df['dateTime'] = rebases_df['dateTime'].dt.date
    rebases_df = rebases_df.set_index('timestamp')
    rebases_df = rebases_df.rename(columns=str.lower)

    # treasury_df['dateTime'] = pd.to_datetime(rebases_df.timestamp, unit='s')
    # treasury_df['dateTime'] = treasury_df['dateTime'].dt.date
    treasury_df = treasury_df.set_index('timestamp')
    treasury_df = treasury_df.rename(columns=str.lower)

    ohmieBalances_df.index = pd.to_numeric(ohmieBalances_df.index, errors='coerce')
    ohmieBalances_df.sohmindexed = pd.to_numeric(ohmieBalances_df.sohmindexed, errors='coerce')
    ohmieBalances_df.sort_index(ascending=True)

    rebases_df.index = pd.to_numeric(rebases_df.index, errors='coerce')
    rebases_df.currentindex = pd.to_numeric(rebases_df.currentindex, errors='coerce')
    rebases_df.sort_index()
    rebases_df.currentindex = rebases_df.currentindex.shift(1).fillna(1)

    treasury_df.index = pd.to_numeric(treasury_df.index, errors='coerce')
    treasury_df.ohmcirculatingsupply = pd.to_numeric(treasury_df.ohmcirculatingsupply, errors='coerce')
    treasury_df.marketcap = pd.to_numeric(treasury_df.marketcap, errors='coerce')
    treasury_df.treasuryriskfreevalue = pd.to_numeric(treasury_df.treasuryriskfreevalue, errors='coerce')
    treasury_df.treasurymarketvalue = pd.to_numeric(treasury_df.treasurymarketvalue, errors='coerce')

    ohmieInfo_df = pd.merge_asof(rebases_df, ohmieBalances_df[['sohmindexed']].sort_values('timestamp'), on='timestamp')
    ohmieInfo_df['sohmbalance'] = ohmieInfo_df.sohmindexed * ohmieInfo_df.currentindex
    ohmieInfo_df = ohmieInfo_df[['timestamp', 'datetime', 'currentindex', 'sohmindexed', 'sohmbalance']]

    ohmieInfo_df = pd.merge_asof(ohmieInfo_df, treasury_df[['ohmcirculatingsupply', 'marketcap',
                                                            'treasuryriskfreevalue',
                                                            'treasurymarketvalue']].sort_values('timestamp'),
                                 on='timestamp')

    ohmieInfo_df['pctmcap'] = ohmieInfo_df.sohmbalance / ohmieInfo_df.ohmcirculatingsupply
    ohmieInfo_df['pctrfv'] = ohmieInfo_df.pctmcap * ohmieInfo_df.treasuryriskfreevalue
    ohmieInfo_df['pctmv'] = ohmieInfo_df.pctmcap * ohmieInfo_df.treasurymarketvalue

    print(ohmieInfo_df)

    metrics_chart_main = go.Figure()
    metrics_chart_2 = go.Figure()
    metrics_chart_3 = go.Figure()
    metrics_chart_4 = go.Figure()
    metrics_chart_main.add_trace(
        go.Scatter(x=ohmieInfo_df.timestamp, y=ohmieInfo_df.sohmbalance, name='sOHM Balance', fill=None)
    )
    metrics_chart_2.add_trace(
        go.Scatter(x=ohmieInfo_df.timestamp, y=ohmieInfo_df.pctmcap, name='pct_mcap', fill=None)
    )
    metrics_chart_3.add_trace(
        go.Scatter(x=ohmieInfo_df.timestamp, y=ohmieInfo_df.pctrfv, name='pct_rfv', fill=None)
    )
    metrics_chart_3.add_trace(
        go.Scatter(x=ohmieInfo_df.timestamp, y=ohmieInfo_df.pctmv, name='pct_mv', fill=None)
    )
    metrics_chart_4.add_trace(
        go.Scatter(x=ohmieInfo_df.timestamp, y=ohmieInfo_df.pctmv, name='pct_mv', fill=None)
    )

    metrics_chart_main.update_layout(autosize=True, showlegend=True, margin=dict(l=20, r=30, t=10, b=20))
    metrics_chart_main.update_layout({'paper_bgcolor': 'rgba(0,0,0,0)', 'plot_bgcolor': 'rgba(0, 0, 0, 0)'})
    metrics_chart_main.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, ), xaxis_title="Days",
                                     yaxis_title="sOHM Balance")
    metrics_chart_main.update_layout(hovermode='x unified', hoverlabel_bgcolor='#2e343e', hoverlabel_align='auto',
                                     hoverlabel_namelength=-1, hoverlabel_font_size=15)
    metrics_chart_main.update_xaxes(showline=True, linewidth=0.1, linecolor='#31333F', color='white', showgrid=False,
                                    gridwidth=0.01, mirror=True)
    metrics_chart_main.update_yaxes(showline=True, linewidth=0.1, linecolor='#31333F', color='white', showgrid=False,
                                    gridwidth=0.01, mirror=True, zeroline=False)
    metrics_chart_main.layout.legend.font.color = 'white'

    metrics_chart_2.update_layout(autosize=True, showlegend=True, margin=dict(l=20, r=30, t=10, b=20))
    metrics_chart_2.update_layout({'paper_bgcolor': 'rgba(0,0,0,0)', 'plot_bgcolor': 'rgba(0, 0, 0, 0)'})
    metrics_chart_2.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, ), xaxis_title="Days",
                                  yaxis_title="sOHM Balance")
    metrics_chart_2.update_layout(hovermode='x unified', hoverlabel_bgcolor='#2e343e', hoverlabel_align='auto',
                                  hoverlabel_namelength=-1, hoverlabel_font_size=15)
    metrics_chart_2.update_xaxes(showline=True, linewidth=0.1, linecolor='#31333F', color='white', showgrid=False,
                                 gridwidth=0.01, mirror=True)
    metrics_chart_2.update_yaxes(showline=True, linewidth=0.1, linecolor='#31333F', color='white', showgrid=False,
                                 gridwidth=0.01, mirror=True, zeroline=False)
    metrics_chart_2.layout.legend.font.color = 'white'

    metrics_chart_3.update_layout(autosize=True, showlegend=True, margin=dict(l=20, r=30, t=10, b=20))
    metrics_chart_3.update_layout({'paper_bgcolor': 'rgba(0,0,0,0)', 'plot_bgcolor': 'rgba(0, 0, 0, 0)'})
    metrics_chart_3.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, ), xaxis_title="Days",
                                  yaxis_title="sOHM Balance")
    metrics_chart_3.update_layout(hovermode='x unified', hoverlabel_bgcolor='#2e343e', hoverlabel_align='auto',
                                  hoverlabel_namelength=-1, hoverlabel_font_size=15)
    metrics_chart_3.update_xaxes(showline=True, linewidth=0.1, linecolor='#31333F', color='white', showgrid=False,
                                 gridwidth=0.01, mirror=True)
    metrics_chart_3.update_yaxes(showline=True, linewidth=0.1, linecolor='#31333F', color='white', showgrid=False,
                                 gridwidth=0.01, mirror=True, zeroline=False)
    metrics_chart_3.layout.legend.font.color = 'white'

    metrics_chart_4.update_layout(autosize=True, showlegend=True, margin=dict(l=20, r=30, t=10, b=20))
    metrics_chart_4.update_layout({'paper_bgcolor': 'rgba(39,51,66,255)', 'plot_bgcolor': 'rgba(39,51,66,255)'})
    metrics_chart_4.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, ), xaxis_title="Days",
                                  yaxis_title="sOHM Balance")
    metrics_chart_4.update_layout(hovermode='x unified', hoverlabel_bgcolor='#2e343e', hoverlabel_align='auto',
                                  hoverlabel_namelength=-1, hoverlabel_font_size=15)
    metrics_chart_4.update_xaxes(showline=True, linewidth=0.1, linecolor='#31333F', color='white', showgrid=False,
                                 gridwidth=0.01, mirror=True)
    metrics_chart_4.update_yaxes(showline=True, linewidth=0.1, linecolor='#31333F', color='white', showgrid=False,
                                 gridwidth=0.01, mirror=True, zeroline=False)
    metrics_chart_4.layout.legend.font.color = 'white'

    return metrics_chart_main, metrics_chart_2, metrics_chart_3, metrics_chart_4


if __name__ == '__main__':
    app.run_server(debug=True)
