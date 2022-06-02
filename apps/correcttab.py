from dash import dcc, ctx
from dash import html, MATCH, ALL
import dash_bootstrap_components as dbc
import plotly.express as px
from app import app
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import numpy as np
import cmath
from apps.modules import filtercreator
from scipy import signal as sg


allpass_zplane_fig = go.FigureWidget(layout=dict(
    template='plotly_dark', height=300, margin_b=40, margin_l=40, margin_r=40, margin_t=40))
allpass_phase_fig = go.FigureWidget(layout=dict(
    template='plotly_dark', height=300, margin_b=40, margin_l=0, margin_r=20, margin_t=40))
corrected_phase_fig = go.FigureWidget(layout=dict(
    template='plotly_dark', height=400, margin_b=40, margin_l=40, margin_r=40, margin_t=40))

filter = filtercreator.Filter()


# ---------------------------------------------ZPLANE------------------------------------------------------------------
# SHOULD SHOW ZERO AND POLE OF SELECTED ALL PASS
def allpass_zplane_plot():
    #labels={'x':'t', 'y':'cos(t)'}
    # drawing the circle
    t = np.linspace(0, 2*np.pi, 100)
    radius = 1
    x = radius * np.cos(t)
    y = radius * np.sin(t)
    # these data are added to a scatter plt(to make points)
    # data 0 for the unit circle
    allpass_zplane_fig.add_scatter(x=x, y=y, mode="lines")
    allpass_zplane_fig.update_xaxes(scaleanchor="y")

    # data 1 for zeros points
    allpass_zplane_fig.add_scatter(x=[], y=[], mode="markers")
    allpass_zplane_fig.data[1].marker.symbol = 'circle-open'
    # data 2 for poles points
    allpass_zplane_fig.add_scatter(x=[], y=[], mode="markers")
    allpass_zplane_fig.data[2].marker.symbol = 'x-open'
    allpass_zplane_fig.update(layout_showlegend=False)
    # this is returned in the 'figure=' of the zplane plot (look for the z plane card)
    return allpass_zplane_fig


# ---------------------------------------------------------------------------------------------------------------------


custom_card = dbc.Collapse(
    dbc.Input(placeholder="Enter desired 'a' value", id="custom_allpass_input",
              type="text", style={'background-color': 'black'}),
    id="custom_allpass",
    is_open=False,
)


# ---------------------------------------------LIBRARY SELECTION AND APPLIED ALL PASS FILTERS------------------------------------------------------------------
allpass_filters_lib_card = dbc.Card(
    [
        dbc.CardHeader(dbc.Row([
            dbc.Col(dbc.Select(
                    id="allpass_dropdown",
                    size="sm",
                    placeholder="Select desired all pass",
                    style={'background-color': 'black'},
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
            dbc.Col(dbc.Button("Add!", id='add_allpass_button',
                    color="primary", size='sm'), width=2),
            dbc.Col(dbc.Button(html.I(className="bi bi-trash-fill"),
                    id='delete_button', color="dark", size='sm'), width=1),
        ]),),
        dbc.CardBody([custom_card, dbc.ListGroup([], id="allpass_list")], style={
                     'padding-right': '0', 'padding-left': '0', 'padding-top': '0', 'padding-bottom': '0'}),
    ],
    style={'padding-right': '0', 'padding-left': '0', 'margin-left': '0'},
)

all_pass_card = dbc.Card(
    [
        dbc.CardHeader("All Pass Filter"),
        dbc.CardBody([
            dbc.Row([dbc.Col(dcc.Graph(id='allpass_zplane', figure=allpass_zplane_plot()), style={'padding-left': '0', 'padding-right': '0', 'padding-top': '0', 'margin-top': '0'}), dbc.Col(
                dcc.Graph(id='allpass_phase', figure=allpass_phase_fig.add_scatter(x=[], y=[])), style={'padding-left': '0', 'padding-right': '0'})]),
            dbc.Row(allpass_filters_lib_card),
            dbc.Row(dbc.Button("Apply!", id='apply_button',
                    color="dark", size='sm'))
        ], style={'padding-top': '0', 'padding-right': '12px', 'padding-left': '12px'}),
    ],
)


corrected_phase_card = dbc.Card(
    [
        dbc.CardHeader("Corrected Phase Response"),

        dbc.CardBody(dcc.Graph(id='corrected_phase_fig',
                     figure=corrected_phase_fig.add_scatter(x=[], y=[])), className="p-0")
    ],
    style={'padding-right': '0', 'padding-left': '0'}
)


def correct_tab_layout():
    layout = html.Div([
        dbc.Row(dbc.Alert(
            "Your filter is ready! Upload your signal in the next tab!",
            id="alert-auto",
            is_open=False,
            color="success",
            duration=4000,
            style={'height': '50px', 'line-height': '50px', 'padding': '0px 25px'}
        ), style={'padding-left': '12px', 'padding-right': '12px'}),
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
        represent_allpass(complex(value))
        if is_open:
            return not is_open, allpass_zplane_fig, allpass_phase_fig
        else:
            return is_open, allpass_zplane_fig, allpass_phase_fig
    elif value == "custom" and button_id == "allpass_dropdown":
        return not is_open, allpass_zplane_fig, allpass_phase_fig
    elif value == "custom" and button_id == "custom_allpass_input":
        represent_allpass(complex(custom_value))
        return is_open, allpass_zplane_fig, allpass_phase_fig


list_id = 0


@app.callback(
    Output("allpass_list", "children"),
    Output("corrected_phase_fig", "figure"),
    State("allpass_dropdown", "value"),
    Input("add_allpass_button", "n_clicks"),
    Input("custom_allpass_input", "value"),
    Input("delete_button", "n_clicks"),
    State("allpass_list", "children"),
    Input("store_zeros", "data"),
    Input("store_poles", "data"),
)
def add_allpass_to_list(value, n_clicks, custom_value, delete_n_clicks, children, zeros, poles):
    button_id = ctx.triggered_id

    if button_id != "allpass_dropdown" and button_id != "add_allpass_button" and button_id != "custom_allpass_input" and button_id != "delete_button":
        for i in zeros:
            filter.add_zero(complex(i))
        for i in poles:
            filter.add_pole(complex(i))
        print("store")

    if value == "custom" and button_id == "add_allpass_button":
        children.append(dbc.ListGroupItem(custom_value, id={'item': str(
            n_clicks)}, style={'color': 'black'}, action=True, active=False))
        filter.add_allpass_filter(complex(custom_value))
    elif value != "custom" and button_id == "add_allpass_button":
        children.append(dbc.ListGroupItem(value, id={'item': str(n_clicks)}, style={
                        'color': 'black'}, action=True, active=False))
        filter.add_allpass_filter(complex(value))
        print("3ayel")
    if button_id == "delete_button":
        assassin_child = []
        for i in children:
            if i['props']['active']:
                assassin_child.append(i)
        for i in assassin_child:
            children.remove(i)
            filter.remove_allpass_filter(complex(i['props']['children']))
        print(children)

    update_corrected_phase_fig()
    return children, corrected_phase_fig


def represent_allpass(a):

    # GET ZERO AND POLE OF ALLPASS AND PLOT ZPLANE
    z, p, k = sg.tf2zpk([-a, 1.0], [1.0, -a])

    allpass_zplane_fig.data[1].x = np.real(z)
    allpass_zplane_fig.data[1].y = np.imag(z)
    allpass_zplane_fig.data[2].x = np.real(p)
    allpass_zplane_fig.data[2].y = np.imag(p)

    # GET W AND H OF ALLPASS AND PLOT ITS PHASE RESPONSE
    w, h = sg.freqz([-a, 1.0], [1.0, -a])

    scatter = allpass_phase_fig.data[0]
    scatter.x = w/max(w)
    scatter.y = np.unwrap(np.angle(h))


@app.callback(
    Output({"item": MATCH}, "active"),
    Input({"item": MATCH}, "n_clicks"),
    State({"item": MATCH}, "active"),
    prevent_initial_call=True
)
def select_allpass(n, active):
    return not active


def update_corrected_phase_fig():
    phase, w = filter.get_phase_response()
    print(filter.get_filter_dict()['filter_zeros'])
    scatter = corrected_phase_fig.data[0]
    scatter.x = w
    scatter.y = phase


@app.callback(
    Output("alert-auto", "is_open"),
    Output("store_corrected_zeros", "data"),
    Output("store_corrected_poles", "data"),
    [Input("apply_button", "n_clicks")],
    [State("alert-auto", "is_open")],
)
def toggle_alert(n, is_open):
    zeros = []
    poles = []
    for i in filter.get_filter_dict()['filter_zeros']:
        zeros.append(str(i))
    for i in filter.get_filter_dict()['filter_poles']:
        poles.append(str(i))

    if n:
        return not is_open, zeros, poles
    return is_open, zeros, poles
