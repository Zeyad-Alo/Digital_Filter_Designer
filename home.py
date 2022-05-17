from dash import dcc
from dash import html
from apps.navbar import create_navbar
import dash_bootstrap_components as dbc
import plotly.express as px
from app import app
from dash.dependencies import Input, Output
import plotly.graph_objects as go


zplane_card = dbc.Card(
    [
        dbc.CardHeader("Z-Plane"),
        dbc.CardBody(dcc.Graph(id='z_plane')),
    ]
    )

options_card = dbc.Card(
    [
        dbc.CardHeader("Preferences"),
        dbc.CardBody("help"),
    ],
    #className="mt-4",
)

mag_card = dbc.Card(
    [
        dbc.CardHeader("Magnitude Response"),
        dbc.CardBody(dcc.Graph(id='mag_response')),
    ],
    #className="mt-4",
)

phase_card = dbc.Card(
    [
        dbc.CardHeader("Phase Response"),
        dbc.CardBody(dcc.Graph(id='phase_response')),
    ],
    #className="mt-4",
)


def design_tab_layout():
    layout = html.Div([
        dbc.Row([
            dbc.Col([zplane_card, html.Br(), options_card], lg=4),
            dbc.Col([mag_card, html.Br(), phase_card])
            ])
        ],            
                      )
    return layout


def create_page_home():
    layout = html.Div([
        dbc.Tabs(
            [
                dbc.Tab(label="Design!", tab_id="design_filter"),
                dbc.Tab(label="Implement!", tab_id="apply_implement"),
            ],
            id="tabs",
            active_tab="design_filter",
        ),
        html.Div(id="tab-content", className="p-4"),
        ],
          className="mx-4"          
                      )
    return layout


@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "active_tab"),
)
def render_tab_content(active_tab):
    if active_tab == "design_filter":
        return design_tab_layout()
        print("design")
    else:
        pass