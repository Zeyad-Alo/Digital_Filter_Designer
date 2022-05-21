from dash import dcc, ctx
from dash import html
from apps.navbar import create_navbar
import dash_bootstrap_components as dbc
import plotly.express as px
from app import app
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import numpy as np


#   PLOT FUNCTION USED TO CREATE ALL GRAPHS (PLACEHOLDER?)
def plot():
    fig = go.Figure(layout=dict(template='plotly_dark', height = 300, margin_b = 40, margin_l = 40, margin_r = 40, margin_t = 40))
    return fig



#   CREATES THE ZPLANE GRAPH
def zplane_plot():
    t = np.linspace(0, 2*np.pi, 100)
    radius = 1
    x = radius * np.cos(t)
    y = radius * np.sin(t)
    fig = px.line(x=x, y=y, labels={'x':'t', 'y':'cos(t)'})
    fig2 = px.scatter(x=[0.3], y=[1])
    fig3 = go.Figure(data=fig.data + fig2.data, layout=dict(template='plotly_dark', height = 300, margin_b = 20, margin_l = 10, margin_r = 10, margin_t = 20))
    return fig3




#   CARD WHERE ZPLANE PLOT LIES
#   PS: CARDS ARE UI ELEMENTS ONLY THE ORGANIZE FUNCTIONAL CONTENT
zplane_card = dbc.Card(
    [
        dbc.CardHeader("Z-Plane"),
        dbc.CardBody(dcc.Graph(id='z_plane', figure= zplane_plot()), className = "p-0"),
    ],
    )



#   CONTENT INSIDE COLLAPSE CARD
collapse_content = html.Div(
    [
        dbc.Row([
            dbc.Col(dcc.Markdown(['Mag'], className="p-0", style={'margin-top':'0px'}), width=3, style={'margin-top':'0px'}),
            dbc.Col(dcc.Slider(0, 1, value=0, marks=None, id = 'mag_slider',
    tooltip={"placement": "bottom", "always_visible": True}, className="p-0"), style={'padding-top':'8px'})
            ],
            ),
        html.Br(),
        dbc.Row([
            dbc.Col(dcc.Markdown('$Theta$', mathjax=True, className="p-0", style={'margin-top':'0px'}), width=3, style={'margin-top':'0px'}),
            dbc.Col(dcc.Slider(0, 180, value=0, marks=None,
    tooltip={"placement": "bottom", "always_visible": True}, className="p-0"), style={'padding-top':'8px'})
            ],
            ),
        dbc.Row([
            dbc.Col(),
            dbc.Col(dbc.Button("Add!", id = 'add_button', color="primary", size='sm'), width=3),
            ]),
        ])



#   CREATES COLLAPSE CARD HOLDING USER INPUTS
collapse = html.Div(
    [
        html.Div(
        [
            dbc.ButtonGroup(
                [dbc.Button("Zeros", id = 'zeros_button', outline = True, color="primary"), dbc.Button("Poles", id = 'poles_button', outline = True, color="primary"),
                 dbc.DropdownMenu(
                    [dbc.DropdownMenuItem("Zeros"), dbc.DropdownMenuItem("Poles"), dbc.DropdownMenuItem("All")],
                    label="Clear",
                    group=True)],
)
        ],
    ),
        
        dbc.Collapse(
            dbc.Card(dbc.CardBody(collapse_content, style={'padding-left':'8px', 'padding-bottom':'10px'}), style={'margin-top':'10px'}),
            id="collapse",
            is_open=False,
        ),
    ]
)



#   OPTIONS (PREFERENCES) CARD BELOW ZPLANE
options_card = dbc.Card(
    [
        dbc.CardHeader("Preferences"),
        dbc.CardBody(collapse, style={'margin-left': '-1px'}, className = "p-1"),
        dbc.CardFooter(
        dbc.Row([
            dbc.Col(dbc.Switch(id = 'conj_checklist', label = "Add Conjugates")),
            dbc.Col(dbc.Button("Apply!", id = 'apply_button', color="primary", size='sm'), width=3),
            ]),
        style={'padding-left': '10px', 'padding-right':'20px'}
    )],
)



mag_card = dbc.Card(
    [
        dbc.CardHeader("Magnitude Response"),
        dbc.CardBody(dcc.Graph(id='mag_response', figure=plot()), className = "p-0"),
    ],
)



phase_card = dbc.Card(
    [
        dbc.CardHeader("Phase Response"),
        dbc.CardBody(dcc.Graph(id='phase_response', figure=plot()), className = "p-0"),
    ],
)



#   PUTS EVERYTHING IN DESIGN TAB TOGETHER IN A LAYOUT
def design_tab_layout():
    layout = html.Div([
        dbc.Row([
            dbc.Col([zplane_card, html.Br(), options_card], width=3),
            dbc.Col([mag_card, html.Br(), phase_card])
            ])
        ],            
                      )
    return layout





#   CALLBACK FOR COLLAPSE BUTTONS (ZEROS BUTTON AND POLES BUTTON)
@app.callback(
    Output("collapse", "is_open"),
    Output("zeros_button", "active"),
    Output("poles_button", "active"),
    [Input("zeros_button", "n_clicks"),
    Input("poles_button", "n_clicks")],
    [State("collapse", "is_open"),
     State("zeros_button", "active"),
     State("poles_button", "active")],
)
def toggle_collapse(n, p_n, is_open, active, p_active):
    button_id = ctx.triggered_id
    if button_id == "zeros_button":
        if n and not p_active:
            return not is_open, not active, p_active
        elif n and p_active:
            return is_open, not active, not p_active
    else:
        if p_n and not active:
            return not is_open, active, not p_active
        elif p_n and active:
            return is_open, not active, not p_active
    return is_open, active, p_active