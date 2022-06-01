from dash import dcc, ctx
from dash import html
from apps.navbar import create_navbar
import dash_bootstrap_components as dbc
import plotly.express as px
from app import app
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import numpy as np




fig = go.FigureWidget(layout=dict(template='plotly_dark', height = 200, margin_b = 40, margin_l = 40, margin_r = 40, margin_t = 40))
fig2= go.FigureWidget(layout=dict(template='plotly_dark', height = 200, margin_b = 40, margin_l = 40, margin_r = 40, margin_t = 40))
fig3= go.FigureWidget(layout=dict(template='plotly_dark', height = 300, margin_b = 40, margin_l = 40, margin_r = 40, margin_t = 40))


#---------------------------------------------ZPLANE------------------------------------------------------------------
# SHOULD SHOW ZERO AND POLE OF SELECTED ALL PASS
def allpass_zplane_plot():
    #labels={'x':'t', 'y':'cos(t)'}
    # drawing the circle
    t = np.linspace(0, 2*np.pi, 100)
    radius = 1
    x = radius * np.cos(t)
    y = radius * np.sin(t)
    # these data are added to a scatter plt(to make points)
    #data 0 for the unit circle 
    fig.add_scatter(x=x,y=y,mode="lines")
    
    # data 1 for zeros points
    fig.add_scatter(x=[0],y=[0],mode="markers")
    fig.data[1].marker.symbol = 'circle-open'
    #data 2 for poles points
    fig.add_scatter(x=[0],y=[0],mode="markers")
    fig.data[2].marker.symbol = 'x-open'
    fig.update(layout_showlegend=False)
    # this is returned in the 'figure=' of the zplane plot (look for the z plane card)
    return fig


#---------------------------------------------------------------------------------------------------------------------






#---------------------------------------------PHASE RESPONSE------------------------------------------------------------------
# SHOULD SHOW PAHSE RESPONSE OF SELECTED ALL PASS FILTER
def plot_2():
    fig2.add_scatter(x=[1],y=[1])
    return fig2


#------------------------------------------------------------------------------------------------------------------------------






#---------------------------------------------LIBRARY SELECTION AND APPLIED ALL PASS FILTERS------------------------------------------------------------------
allpass_filters_lib_card = dbc.Card(
    [
        dbc.CardHeader(dbc.Row([
            dbc.Col(dcc.Dropdown(['New York City', 'Montreal', 'San Francisco'], 'Montreal', style={'background-color':'black', 'color':'white'})),
            dbc.Col(dbc.Button("Add!", id = 'apply_button', color="primary", size='sm')),
            ]),),
        dbc.CardBody([dbc.ListGroup(
    [
        dbc.ListGroupItem(["Item 1", dbc.Button(html.I(className="bi bi-trash-fill"), id = 'apply_button', color="dark", size='sm')], className="d-flex w-100 justify-content-between", style={'color':'black'}),
    ]
),], style={'padding-right': '0', 'padding-left': '0', 'padding-top': '0', 'padding-bottom': '0'}),

    ],
    style={'padding-right': '0', 'padding-left': '0', 'margin-left': '0'},
)
#-----------------------------------------------------------------------------------------------------------------------------------------





all_pass_card = dbc.Card(
    [
        dbc.CardHeader("All Pass Filter"),
        dbc.CardBody([
            dbc.Row([dbc.Col(dcc.Graph(id='allpass_zplane', figure=allpass_zplane_plot()), style={'padding-left':'0', 'padding-right':'0', 'padding-top':'0', 'margin-top':'0'}),dbc.Col(dcc.Graph(id='allpass_phase', figure=plot_2()), style={'padding-left':'0', 'padding-right':'0'})]),
            dbc.Row(allpass_filters_lib_card),
            dbc.Row(dbc.Button("Apply!", id = 'apply_button', color="dark", size='sm'))
            ], className = "p-2", style={'padding-top':'0'}),
    ],
)



# SHOULD RECIEVE OLD PHASE RESPONSE FROM DESIGN TAB AND APPEND ANY ADDED ALL PASS FILTERS TO IT
def plot_3():
    fig3.add_scatter(x=[0],y=[0])
    return fig3

corrected_phase_card = dbc.Card(
    [
        dbc.CardHeader("Corrected Phase Response"),
        dbc.CardBody(dcc.Graph(id='original_signal', figure=plot_2()), className = "p-0"),
    ],
    style={'padding-right': '0', 'padding-left': '0'}
)




def correct_tab_layout():
    layout = html.Div([
        dbc.Row([
            dbc.Col(all_pass_card, width=4),
            dbc.Col(corrected_phase_card)
            ])
        ],            
                      )
    return layout