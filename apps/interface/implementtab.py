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
from scipy import signal as sg

fig4= go.FigureWidget(layout=dict(template='plotly_dark', height = 300, margin_b = 40, margin_l = 40, margin_r = 40, margin_t = 40))
fig5= go.FigureWidget(layout=dict(template='plotly_dark', height = 300, margin_b = 40, margin_l = 40, margin_r = 40, margin_t = 40))



# for the fourth plot TO INITIALIZE THE signal CARD
def plot_4():
    fig4.add_scatter(x=[0],y=[0])
    return fig4

# for the fifth plot TO INITIALIZE THE filterd signal CARD
def plot_5():
    fig5.add_scatter(x=[0],y=[0])
    return fig5


original_signal_card = dbc.Card(
    [
        dbc.CardHeader("Signal"),
        dbc.CardBody(dcc.Graph(id='original_signal', figure=plot_4()), className = "p-0"),
    ],
    style={'padding-right': '0', 'padding-left': '0'}
)



filtered_signal_card = dbc.Card(
    [
        dbc.CardHeader("Filtered Signal"),
        dbc.CardBody(dcc.Graph(id='filtered_signal', figure=plot_5()), className = "p-0"),
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



def updating_fig4(data,x,y):
    scatter = fig2.data[data]
    scatter.x = list(x)
    scatter.y = list(y)

def updating_fig5(data,x,y):
    scatter = fig3.data[data]
    scatter.x = list(x)
    scatter.y = list(y)

#call back for filterd signal

@app.callback(
    Output("original_signal", "figure"),
    Output("filtered_signal", "figure"),
   
    Input("store_num", "data"),
    Input("store_den", "data"),

)

def Signal_filtered_update(num,den):
 
    filterd_output=sg.lfilter(num,den,signal)
    updating_fig4(data,x,y):
    updating_fig5(0,filterd_output,y):
   
    return fig4,fig5




