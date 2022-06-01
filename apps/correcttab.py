from dash import dcc, ctx
from dash import html, MATCH, ALL
import dash_bootstrap_components as dbc
import plotly.express as px
from app import app
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import numpy as np
import cmath
from scipy import signal as sg



fig = go.FigureWidget(layout=dict(template='plotly_dark', height = 300, margin_b = 40, margin_l = 40, margin_r = 40, margin_t = 40))
fig2= go.FigureWidget(layout=dict(template='plotly_dark', height = 300, margin_b = 40, margin_l = 0, margin_r = 20, margin_t = 40))
fig3= go.FigureWidget(layout=dict(template='plotly_dark', height = 400, margin_b = 40, margin_l = 40, margin_r = 40, margin_t = 40))

all_pass_filters_ids = []



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
    fig.update_xaxes(scaleanchor="y")
  
    # data 1 for zeros points
    fig.add_scatter(x=[],y=[],mode="markers")
    fig.data[1].marker.symbol = 'circle-open'
    #data 2 for poles points
    fig.add_scatter(x=[],y=[],mode="markers")
    fig.data[2].marker.symbol = 'x-open'
    fig.update(layout_showlegend=False)
    # this is returned in the 'figure=' of the zplane plot (look for the z plane card)
    return fig


#---------------------------------------------------------------------------------------------------------------------






#---------------------------------------------PHASE RESPONSE------------------------------------------------------------------
# SHOULD SHOW PAHSE RESPONSE OF SELECTED ALL PASS FILTER
def plot_2():
    fig2.add_scatter(x=[],y=[])
    fig2.update(layout_showlegend=False)
    return fig2


#------------------------------------------------------------------------------------------------------------------------------


custom_card = dbc.Collapse(
            dbc.Input(placeholder="Enter desired 'a' value", id="custom_allpass_input", type="text", style={'background-color':'black'}),
            id="custom_allpass",
            is_open=False,
        )




#---------------------------------------------LIBRARY SELECTION AND APPLIED ALL PASS FILTERS------------------------------------------------------------------
allpass_filters_lib_card = dbc.Card(
    [
        dbc.CardHeader(dbc.Row([
            dbc.Col(dbc.Select(
                    id="allpass_dropdown",
                    size="sm",
                    placeholder="Select desired all pass",
                    style={'background-color':'black'},
                    options=[
                        {"label": "-0.9", "value": "-0.9"},
                        {"label": "-0.5", "value": "-0.5"},
                        {"label": "0.0", "value": "0.0"},
                        {"label": "0.5", "value": "0.5"},
                        {"label": "0.9", "value": "0.9"},
                        {"label": "0.5 + 0.5j", "value": "0.5+0.5j"},
                        {"label": "1 + 0.5j", "value": "1+0.5j"},
                        {"label": "1 + 1j", "value": "1+1j"},
                        {"label": "1 + 2j", "value": "1+2j"},
                        {"label": "2 + 0.5j", "value": "2+0.5j"},
                        {"label": "2 + 2j", "value": "2+2j"},
                        {"label": "Custom", "value": "custom"},
                    ],
                )),
            dbc.Col(dbc.Button("Add!", id = 'add_allpass_button', color="primary", size='sm'), width = 2),
            dbc.Col(dbc.Button(html.I(className="bi bi-trash-fill"), id = 'delete_button', color="dark", size='sm'), width = 1),
            ]),),
        dbc.CardBody([custom_card, dbc.ListGroup([], id="allpass_list")], style={'padding-right': '0', 'padding-left': '0', 'padding-top': '0', 'padding-bottom': '0'}),
    ],
    style={'padding-right': '0', 'padding-left': '0', 'margin-left': '0'},
)

all_pass_card = dbc.Card(
    [
        dbc.CardHeader("All Pass Filter"),
        dbc.CardBody([
            dbc.Row([dbc.Col(dcc.Graph(id='allpass_zplane', figure=allpass_zplane_plot()), style={'padding-left':'0', 'padding-right':'0', 'padding-top':'0', 'margin-top':'0'}),dbc.Col(dcc.Graph(id='allpass_phase', figure=plot_2()), style={'padding-left':'0', 'padding-right':'0'})]),
            dbc.Row(allpass_filters_lib_card),
            dbc.Row(dbc.Button("Apply!", id = 'apply_button', color="dark", size='sm'))
            ], style={'padding-top':'0', 'padding-right':'12px', 'padding-left':'12px'}),
    ],
)



# SHOULD RECIEVE OLD PHASE RESPONSE FROM DESIGN TAB AND APPEND ANY ADDED ALL PASS FILTERS TO IT
def plot_3():
    fig3.add_scatter(x=[],y=[])
    return fig3

corrected_phase_card = dbc.Card(
    [
        dbc.CardHeader("Corrected Phase Response"),

        dbc.CardBody(dcc.Graph(id='original_signal', figure=plot_3()), className = "p-0")
    ],
    style={'padding-right': '0', 'padding-left': '0'}
)




def correct_tab_layout():
    layout = html.Div([
        dbc.Row([
            dbc.Col(all_pass_card),
            dbc.Col(corrected_phase_card)
            ])
        ],)
    return layout


@app.callback(
    Output("custom_allpass", "is_open"),
    Output("allpass_zplane", "figure"),
    Output("allpass_phase", "figure"),
    State("custom_allpass", "is_open"),
    Input("allpass_dropdown", "value"),
    Input("custom_allpass_input", "value"),
)
def add_allpass_to_list(is_open, value, custom_value):
    button_id = ctx.triggered_id
    if value != "custom":
        create_allpass(complex(value))
        if is_open: return not is_open, fig, fig2
        else: return is_open, fig, fig2
    elif value == "custom" and button_id == "allpass_dropdown":
        return not is_open, fig, fig2
    elif value == "custom" and button_id == "custom_allpass_input":
        create_allpass(complex(custom_value))
        return is_open, fig, fig2




list_id = 0

@app.callback(
    Output("allpass_list", "children"),
    State("allpass_dropdown", "value"),
    Input("add_allpass_button", "n_clicks"),
    Input("custom_allpass_input", "value"),
    Input("delete_button", "n_clicks"),
    #Input(str(list_id), "active"),
    #State("delete_button", "n_clicks"),
    State("allpass_list", "children")
    )
def add_allpass_to_list(value, n_clicks, custom_value, delete_n_clicks, children) :
    button_id = ctx.triggered_id

    if value == "custom" and button_id == "add_allpass_button":
        children.append(dbc.ListGroupItem(custom_value, id={'item':str(n_clicks)}, style={'color':'black'}, action=True, active=False))
    elif value != "custom" and button_id == "add_allpass_button":
        children.append(dbc.ListGroupItem(value, id={'item':str(n_clicks)}, style={'color':'black'}, action=True, active=False))
        print("3ayel")
    if button_id == "delete_button":
        assassin_child = []
        print(children)
        for i in children:
            print(i['props']['active'])
            if i['props']['active']:
                assassin_child.append(i)
        for i in assassin_child:
            children.remove(i)


    print(n_clicks)
    return children



def create_allpass(a) :
    #factors = np.linspace(-0.99, 0.99, 5)
    z, p, k = sg.tf2zpk([-a, 1.0], [1.0, -a])

    w, h = sg.freqz([-a, 1.0], [1.0, -a])

    fig.data[1].x = np.real(z)
    fig.data[1].y = np.imag(z)
    fig.data[2].x = np.real(p)
    fig.data[2].y = np.imag(p)

    scatter = fig2.data[0]
    scatter.x = w/max(w)
    scatter.y = np.unwrap(np.angle(h))



@app.callback(
    Output({"item": MATCH}, "active"),
    Input({"item": MATCH}, "n_clicks"),
    State({"item": MATCH}, "active"),
    prevent_initial_call=True
    )
def select_allpass(n, active) :
    return not active
