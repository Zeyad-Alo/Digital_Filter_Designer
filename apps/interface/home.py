from dash import dcc, ctx
from dash import html
from apps.navbar import create_navbar
import dash_bootstrap_components as dbc
import plotly.express as px
from app import app
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import numpy as np
from apps.interface.designtab import design_tab_layout
from apps.interface.implementtab import implement_tab_layout
from apps.interface.correcttab import correct_tab_layout



#   CREATES A TAB WIDGET WITH ALL THREE TABS LAYOUT CREATED IN THEIR SEPARATE FILES
def create_home_page():
    layout = html.Div([
        dbc.Tabs(
            [
                dbc.Tab(label="Design!", tab_id="design_tab"),
                dbc.Tab(label="Correct!", tab_id="correct_tab"),
                dbc.Tab(label="Implement!", tab_id="implement_tab"),
            ],
            id="tabs",
            active_tab="design_tab",
        ),
        html.Div(id="tab-content", className="p-4"),
        ],
          className="mx-4"          
                      )
    return layout



#   CALLBACK FOR THE DIFFERENT TABS
#   PS: CALLBACK ARE LIKE CONNECTORS
@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "active_tab"),
)
def render_tab_content(active_tab):
    if active_tab == "design_tab":
        return design_tab_layout()
        print("design")
    elif active_tab == "correct_tab":
        return correct_tab_layout()
    elif active_tab == "implement_tab":
        return implement_tab_layout()

