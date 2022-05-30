from dash import dcc, ctx
from dash import html
from apps.navbar import create_navbar
import dash_bootstrap_components as dbc
import plotly.express as px
from app import app
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import numpy as np
from apps.interface.designtab import plot





original_signal_card = dbc.Card(
    [
        dbc.CardHeader("Signal"),
        dbc.CardBody(dcc.Graph(id='original_signal', figure=plot()), className = "p-0"),
    ],
    style={'padding-right': '0', 'padding-left': '0'}
)



filtered_signal_card = dbc.Card(
    [
        dbc.CardHeader("Filtered Signal"),
        dbc.CardBody(dcc.Graph(id='filtered_signal', figure=plot()), className = "p-0"),
        dbc.CardFooter(
            dbc.Row([
                dbc.Col(dcc.Markdown('Speed', className="p-0"), width=1),
                dbc.Col(dcc.Slider(0, 100, value=100, marks=None, id = 'speed_slider',
    tooltip={"placement": "bottom", "always_visible": False}, className="p-0"), style={'padding-top':'8px'})
                ]),
            )
    ],
    style={'padding-right': '0', 'padding-left': '0'}

)



nav = dbc.Nav(
    [
        dbc.NavItem(dcc.Upload(dbc.Button('Upload File', size="sm")),
),
    ]
)



def implement_tab_layout():
    layout = html.Div([
        dbc.Row(nav),
        dbc.Row(original_signal_card),
        html.Br(),
        dbc.Row(filtered_signal_card),
        ],            
                      )
    return layout