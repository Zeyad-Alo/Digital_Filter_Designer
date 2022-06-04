from dash import dcc, ctx
from dash import html
from dash import callback_context
from zmq import SCATTER
import dash_bootstrap_components as dbc
import plotly.express as px
from app import app
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import numpy as np
import cmath
import math
import json
from apps.modules import filtercreator
from scipy import signal as sg
from numpy import conjugate
from apps.modules.utility import print_debug

zeros_all_conj = []
poles_all_conj = []
# object
filter = filtercreator.Filter()

# intializing figures in order to update them later(their layouts)

z_plane_fig = go.FigureWidget(layout=dict(
    template='plotly_dark', height=300, margin_b=40, margin_l=40, margin_r=40, margin_t=40))
magnitude_fig = go.FigureWidget(layout=dict(
    template='plotly_dark', height=300, margin_b=40, margin_l=40, margin_r=40, margin_t=40))
phase_fig = go.FigureWidget(layout=dict(
    template='plotly_dark', height=300, margin_b=40, margin_l=40, margin_r=40, margin_t=40))


def init_zplane_plot():
    # labels={'x':'t', 'y':'cos(t)'}
    # drawing the circle
    t = np.linspace(0, 2*np.pi, 100)
    radius = 1
    x = radius * np.cos(t)
    y = radius * np.sin(t)
    # these data are added to a scatter plt(to make points)
    # data 0 for the unit circle
    z_plane_fig.add_scatter(x=x, y=y, mode="lines")

    # data 1 for zeros points
    z_plane_fig.add_scatter(x=[], y=[], mode="markers")
    z_plane_fig.data[1].marker.symbol = 'circle-open'

    # data 2 for poles points
    z_plane_fig.add_scatter(x=[], y=[], mode="markers")
    z_plane_fig.data[2].marker.symbol = 'x-thin-open'
    z_plane_fig.update_xaxes(scaleanchor="y")

    z_plane_fig.update(layout_showlegend=False)
    # this is returned in the 'figure=' of the zplane plot (look for the z plane card)
    return z_plane_fig

####################################### ADDED FUNCTIONS (AS :) ) #######################################


def updating_figure_desgin(figure=None, data_index=0, x=[], y=[], symbol='circle-open'):
    scatter = figure.data[data_index]
    scatter.x = list(x)
    scatter.y = list(y)
    print_debug("updated")
    if figure == z_plane_fig:
        scatter.marker.symbol = symbol


def updating_all_figures():

    updating_figure_desgin(figure=z_plane_fig, data_index=1, x=np.real(
        filter.filter_zeros), y=np.imag(filter.filter_zeros), symbol='circle-open')
    updating_figure_desgin(figure=z_plane_fig, data_index=2, x=np.real(
        filter.filter_poles), y=np.imag(filter.filter_poles), symbol='x-thin-open')

    updating_figure_desgin(figure=magnitude_fig, data_index=0,
                           x=filter.w, y=filter.filter_magnitude_response)
    updating_figure_desgin(figure=phase_fig, data_index=0,
                           x=filter.w, y=filter.filter_phase_response)


#   PS: CARDS ARE UI ELEMENTS ONLY THE ORGANIZE FUNCTIONAL CONTENT
zplane_card = dbc.Card(
    [
        dbc.CardHeader("Z-Plane"),
        dbc.CardBody(dcc.Graph(id='z_plane', figure=init_zplane_plot(), config={
            'editable': True,
            'edits': {
                'shapePosition': True
            }
        }), className="p-0"
        )],
)


#   CONTENT INSIDE COLLAPSE CARD
collapse_content = html.Div(
    [
        dbc.Row([
            dbc.Col(dcc.Markdown(['Mag'], className="p-0", style={
                    'margin-top': '0px'}), width=3, style={'margin-top': '0px'}),
            dbc.Col(dcc.Slider(0, 2, value=0, marks=None, id='mag_slider',
                               tooltip={"placement": "bottom", "always_visible": True}, className="p-0"), style={'padding-top': '8px'})
        ],
        ),
        html.Br(),
        dbc.Row([
            dbc.Col(dcc.Markdown('$Theta$', mathjax=True, className="p-0",
                    style={'margin-top': '0px'}), width=3, style={'margin-top': '0px'}),
            dbc.Col(dcc.Slider(0, 180, value=0, marks=None, id='theta_slider',
                               tooltip={"placement": "bottom", "always_visible": True}, className="p-0"), style={'padding-top': '8px'})
        ],
        ),
        dbc.Row([
            dbc.Col(),
            dbc.Col(dbc.Button("Add!", id='add_button', n_clicks=0,
                    color="primary", size='sm'), width=3),
        ]),
    ])

#   CREATES COLLAPSE CARD HOLDING USER INPUTS
collapse = html.Div(
    [
        html.Div(
            [
                dbc.ButtonGroup(
                    [dbc.Button("Zeros", id='zeros_button', outline=True, color="primary"), dbc.Button("Poles", id='poles_button', outline=True, color="primary"),
                     dbc.DropdownMenu(
                        [dbc.DropdownMenuItem("Zeros", id="dropdown_zeros"), dbc.DropdownMenuItem(
                            "Poles", id="dropdown_poles"), dbc.DropdownMenuItem("All", id="dropdown_all")],
                        label="Clear",
                        group=True)],
                )
            ],
        ),

        dbc.Collapse(
            dbc.Card(dbc.CardBody(collapse_content, style={
                     'padding-left': '8px', 'padding-bottom': '10px'}), style={'margin-top': '10px'}),
            id="collapse",
            is_open=False,
        ),
    ]
)

#   OPTIONS (PREFERENCES) CARD BELOW ZPLANE
options_card = dbc.Card(
    [
        dbc.CardHeader("Preferences"),
        dbc.CardBody(collapse, style={'margin-left': '-1px'}, className="p-1"),
        dbc.CardFooter(
            dbc.Row([
                dbc.Col(dbc.Switch(id='conj_checklist', label="Add Conjugates")),
                dbc.Col(dbc.Button(html.I(className="bi bi-trash-fill"),
                        id='delete_button', color="dark", size='sm'), width=1),
            ]),
            style={'padding-left': '10px', 'margin-right': '20px'}
        )],
)

mag_card = dbc.Card(
    [
        dbc.CardHeader("Magnitude Response"),
        dbc.CardBody(dcc.Graph(id='mag_response', figure=magnitude_fig.add_scatter(
            x=[], y=[])), className="p-0"),
    ],
)


phase_card = dbc.Card(
    [
        dbc.CardHeader("Phase Response"),
        dbc.CardBody(dcc.Graph(id='phase_response',
                     figure=phase_fig.add_scatter(x=[], y=[])), className="p-0"),

    ],
)


#   PUTS EVERYTHING IN DESIGN TAB TOGETHER IN A LAYOUT
def design_tab_layout():
    layout = html.Div([
        dbc.Row([
            dbc.Col([zplane_card, html.Br(), options_card],
                    className="col-lg-3"),
            dbc.Col([mag_card, html.Br(), phase_card], className="col-lg-9")
        ]),
        html.Pre(id='relayout-data')
    ], className="container")
    return layout

#   CALLBACK FOR COLLAPSE BUTTONS (ZEROS BUTTON AND POLES BUTTON)


@ app.callback(
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


SAMPLING_FREQ = 44100
#   CALLBACK FOR Mag and Theta
# call backs should have atleast one output and one input it takes 2 arguments first the id of the card and second the type of the date
# that will be returned


@ app.callback(
    Output("z_plane", "figure"),
    Output("mag_response", "figure"),
    Output("phase_response", "figure"),
    Output("store_num_real", "data"),
    Output("store_num_imag", "data"),
    Output("store_den_real", "data"),
    Output("store_den_imag", "data"),
    Output("store_zeros", "data"),
    Output("store_poles", "data"),
    Input("add_button", "n_clicks"),
    Input("mag_slider", "value"),
    Input("theta_slider", "value"),
    State("zeros_button", "active"),
    State("poles_button", "active"),
    Input("delete_button", "n_clicks"),
    Input("conj_checklist", "value"),
    Input("dropdown_zeros", "n_clicks"),
    Input("dropdown_poles", "n_clicks"),
    Input("dropdown_all", "n_clicks"),
    Input("z_plane", "clickData"),
    [Input('z_plane', 'relayoutData')]
)
def zplane_mag_phase_update(nclicks, mag_value, theta_value, z_active, p_active, delete_click, activated, zclicks, pclicks, allclicks, clicked_data, relayoutData):
    num = []
    den = []
    real_num = []
    imag_num = []
    real_den = []
    imag_den = []

    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    # theta value and mag value are taken from the sliders
    z_axis = cmath.rect(mag_value, (theta_value*np.pi/180))
    # this loop is entred when both the zeros button is open and the user pressed add
   
    if z_active and 'add_button' in changed_id:
        # print_debug("zeros")
        filter.add_pole_zero(z_axis, filter=filter.filter_zeros,filter_check=filter.filter_poles)

        updating_figure_desgin(figure=z_plane_fig, data_index=1, x=np.real(
            filter.filter_zeros), y=np.imag(filter.filter_zeros), symbol='circle-open')
        updating_figure_desgin(figure=z_plane_fig, data_index=2, x=np.real(
            filter.filter_poles), y=np.imag(filter.filter_poles), symbol='x-thin-open')
        # this loop is entred when both the poles button is open and the user pressed add
    elif p_active and 'add_button' in changed_id:
        # print_debug("poles")
        filter.add_pole_zero(z_axis, filter=filter.filter_poles,filter_check=filter.filter_zeros)
        print_debug("THHHHHHHHHe filter")
        # print_debug(filter.get_filter_dict())
        updating_figure_desgin(figure=z_plane_fig, data_index=1, x=np.real(
            filter.filter_zeros), y=np.imag(filter.filter_zeros), symbol='circle-open')
        updating_figure_desgin(figure=z_plane_fig, data_index=2, x=np.real(
            filter.filter_poles), y=np.imag(filter.filter_poles), symbol='x-thin-open')

    if 'add_button' in changed_id:
        # print_debug("phase and mag resp")
        # magnitude_response,phase_response,w,num,den = filter.get_magnitude_phase_response()
        # updating_figure_desgin(figure=magnitude_fig,data_index=0,x=w,y=magnitude_response)

        # updating_figure_desgin(figure=phase_fig,data_index=0,x=w,y=phase_response)
        updating_figure_desgin(figure=magnitude_fig, data_index=0,
                               x=filter.w, y=filter.filter_magnitude_response)
        updating_figure_desgin(
            figure=phase_fig, data_index=0, x=filter.w, y=filter.filter_phase_response)

    if 'conj_checklist' in changed_id and activated:

        print_debug("enabled  TRUE")
        filter.enable_conjugates(True)
        updating_all_figures()

    elif 'conj_checklist' in changed_id and not activated:
        # TODO mosh by-plot fel state deee lazm y-activate first Check why ??!!
        print_debug("enabled  FALSE")
        filter.enable_conjugates(False)
        updating_all_figures()

    if 'dropdown_zeros' in changed_id:

        filter.clear_zeros()
        updating_all_figures()

    elif 'dropdown_poles' in changed_id:

        filter.clear_poles()
        updating_all_figures()

    elif 'dropdown_all' in changed_id:

        filter.clear_filter()
        updating_all_figures()

    # for storing DASH CANNOT PROCESS COMPLEX NUMBERS
    # if len(num) == 0 and len(den) ==0:

    #     real_num=np.real(num)
    #     imag_num=np.imag(num)

    #     real_den=np.real(den)
    #     imag_den=np.imag(den)

    #     real_num=real_num.tolist()
    #     imag_num=imag_num.tolist()

    #     real_den=real_den.tolist()
    #     imag_den=imag_den.tolist()

        # print_debug(type(real_num))
        # print_debug(type(real_den))
        # print_debug(real_num)
        # print_debug(real_den)
        # print_debug(imag_num)
        # print_debug(imag_den)

    if clicked_data is not None and ctx.triggered[0]['value'] != None and ctx.triggered[0]['value'] != {'autosize': True}:
        print_debug(clicked_data)
        # TODO: handle if the arrays of zeros and poles are empty
        data = clicked_data['points'][0]['curveNumber']
        y = clicked_data['points'][0]['y']
        x = clicked_data['points'][0]['x']

        # TODO modify the array in index 0
        z_plane_fig.plotly_relayout({'shapes': [{'type': 'circle', 'fillcolor': '#7f7f7f', 'line': {
                                    'width': 0}, 'opacity': 0.3, 'x0': x-0.07, 'x1': x+0.07, 'y0': y-0.07, 'y1': y+0.07}]})
        if data == 1 and 'delete_button' in changed_id:
            filter.remove_pole_zero(x+y*1j, filter.filter_zeros)
            z_plane_fig.plotly_relayout({'shapes': []})
            updating_all_figures()
        elif data == 2 and 'delete_button' in changed_id:
            filter.remove_pole_zero(x+y*1j, filter.filter_poles)
            z_plane_fig.plotly_relayout({'shapes': []})
            updating_all_figures()
            # if 'conj_checklist' in changed_id and activated:
            #     filter.remove_conjugate(polezero='pole',input=conjugate(x+y*1j))

        if ctx.triggered[0]['value'] != None and ctx.triggered[0]['value'] != {'autosize': True} and ctx.triggered_id == 'z_plane' and 'shapes[0].y0' in ctx.triggered[0]['value']:
            x_new = (ctx.triggered[0]['value']['shapes[0].x0'] +
                     ctx.triggered[0]['value']['shapes[0].x1']) / 2
            y_new = (ctx.triggered[0]['value']['shapes[0].y0'] +
                     ctx.triggered[0]['value']['shapes[0].y1']) / 2
            if data == 1:
                filter.edit_zero(x+y*1j, x_new + y_new*1j)
            elif data == 2:
                filter.edit_pole(x+y*1j, x_new + y_new*1j)
            z_plane_fig.plotly_relayout({'shapes': []})
            updating_all_figures()

    clicked_data = None
    if ctx.triggered_id != "z_plane":
        z_plane_fig.plotly_relayout({'shapes': []})
    # we return the figure in the "figure =" of zplot (find z plot card)
    # changing the array to list so the data in store id is right
    zeros = []
    poles = []
    for i in filter.get_filter_dict()['filter_zeros']:
        zeros.append(str(i))
    for i in filter.get_filter_dict()['filter_poles']:
        poles.append(str(i))
    return z_plane_fig, magnitude_fig, phase_fig, real_num, imag_num, real_den, imag_den, zeros, poles
