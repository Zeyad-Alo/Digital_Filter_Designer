from dash import dcc, ctx
from dash import html
import dash_bootstrap_components as dbc
import plotly.express as px
from app import app
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import numpy as np
from scipy import signal as sg
import base64
import datetime
import io
import pandas as pd
import cmath
from apps.modules.utility import print_debug

from apps.modules.filtercreator import Filter

signal_fig = go.FigureWidget(layout=dict(
    template='plotly_dark', height=300, margin_b=40, margin_l=40, margin_r=40, margin_t=40))
filterd_signal_fig = go.FigureWidget(layout=dict(
    template='plotly_dark', height=300, margin_b=40, margin_l=40, margin_r=40, margin_t=40))


original_signal_card = dbc.Card(
    [
        dbc.CardHeader("Signal"),
        dbc.CardBody(dcc.Graph(id='original_signal', figure=signal_fig.add_scatter(
            x=[], y=[])), className="p-0"),
    ],
    style={'padding-right': '0', 'padding-left': '0'}
)


filtered_signal_card = dbc.Card(
    [
        dbc.CardHeader("Filtered Signal"),
        dbc.CardBody(dcc.Graph(id='filtered_signal', figure=filterd_signal_fig.add_scatter(
            x=[], y=[])), className="p-0"),
        dbc.CardFooter(
            dbc.Row([
                dbc.Col(dcc.Markdown('Speed', className="p-0"), width=1),
                dbc.Col(dcc.Slider(1, 6, 1, value=1, marks=None, id='speed_slider',
                                   tooltip={"placement": "bottom", "always_visible": False}, className="p-0"), style={'padding-top': '8px'})
            ]),
        )
    ],
    style={'padding-right': '0', 'padding-left': '0'}

)

nav = dbc.Nav(
    [
        dbc.NavItem(dcc.Upload(
            id='upload-data',
            children=html.Div([
                html.A('Select Files')
            ]), multiple=False)
        ),
    ]
)


def implement_tab_layout():
    layout = html.Div([
        dbc.Row(nav),
        dbc.Row(original_signal_card),
        html.Br(),
        dbc.Row(filtered_signal_card), dcc.Interval(
            id='interval_component',
            interval=1*1000,  # in milliseconds
            n_intervals=0, disabled=False
        ), dcc.Store(id='time_data'), dcc.Store(id='mag_data'), dcc.Store(id='counter', data=0)
    ],
    )
    return layout


def updating_figure_implement(figure=None, data_index=0, x=[], y=[]):
    scatter = figure.data[data_index]
    scatter.x = list(x)
    scatter.y = list(y)


def parse_contents(contents, filename, date):
    pd.options.display.max_rows = 10000
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print_debug(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return df


# callback for uploading data
@app.callback(
    Output("time_data", "data"),
    Output("mag_data", "data"),


    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified'),


)
def Signal_update(contents, filenames, last_modified):
    # TODO DONT FORGET TIME PROGRESS
    print_debug("DATA FROM FILE")
    mag = []
    time = []
    if contents is not None:
        print_debug("there is data")
        dff = parse_contents(contents, filenames, last_modified)
        print_debug("dataframe")
        print_debug(dff)
        time = dff.iloc[:, 0]
        mag = dff.iloc[:, 1]
        time_np = time.to_numpy()
        mag_np = mag.to_numpy()
        time = time_np.tolist()
        mag = mag_np.tolist()
    print_debug(len(time))
    print_debug(len(mag))

    return time, mag


# callback for UPDATING data
@app.callback(
    Output("original_signal", "figure"),
    Output("filtered_signal", "figure"),
    Output('interval_component', 'disabled'),
    Output("counter", "data"),


    Input("store_corrected_zeros", "data"),
    Input("store_corrected_poles", "data"),
    Input("speed_slider", "value"),
    Input("interval_component", "n_intervals"),
    Input("interval_component", "disabled"),
    Input("time_data", "data"),
    Input("mag_data", "data"),
    Input("counter", "data"),

)
def Signal_update(zeros, poles, speed, n, disabled, time, mag, counter):
    # TODO DONT FORGET TIME PROGRESS
    time = np.array(time)
    mag = np.array(mag)

    filter = Filter()

    for i in zeros:
        filter.add_pole_zero(complex(i), filter.filter_zeros)
    for i in poles:
        filter.add_pole_zero(complex(i), filter.filter_poles)

    if len(time) != 0:

        print_debug("UPDATING FIGURE")
        counter = counter+1
        pointsToAppend = 10*counter*int(speed)
        pointsToAppendOld = pointsToAppend - 10*counter*int(speed)
        print_debug(pointsToAppendOld)
        if pointsToAppendOld or pointsToAppend >= len(time):
            disabled = True
        else:
            filtred_mag = filter.filter_samples(
                mag[pointsToAppendOld:pointsToAppend])

            updating_figure_implement(
                figure=signal_fig, x=time[pointsToAppendOld:pointsToAppend], y=mag[pointsToAppendOld:pointsToAppend])

            signal_fig.update_layout(
                xaxis_range=[time[pointsToAppendOld], time[pointsToAppend]])

            updating_figure_implement(
                figure=filterd_signal_fig, x=time[pointsToAppendOld:pointsToAppend], y=filtred_mag[pointsToAppendOld:pointsToAppend])

            filterd_signal_fig.update_layout(
                xaxis_range=[time[pointsToAppendOld], time[pointsToAppend]])

            disabled = False

    elif len(time) == 0:

        print_debug("lasa mad5lsh 7aga")
    return signal_fig, filterd_signal_fig, disabled, counter
