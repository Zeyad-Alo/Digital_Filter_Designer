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
from apps.modules.filtercreator import Filter
signal_fig= go.FigureWidget(layout=dict(template='plotly_dark', height = 300, margin_b = 40, margin_l = 40, margin_r = 40, margin_t = 40))
filterd_signal_fig= go.FigureWidget(layout=dict(template='plotly_dark', height = 300, margin_b = 40, margin_l = 40, margin_r = 40, margin_t = 40))



original_signal_card = dbc.Card(
    [
        dbc.CardHeader("Signal"),
        dbc.CardBody(dcc.Graph(id='original_signal', figure=signal_fig.add_scatter(x=[],y=[])), className = "p-0"),
    ],
    style={'padding-right': '0', 'padding-left': '0'}
)


filtered_signal_card = dbc.Card(
    [
        dbc.CardHeader("Filtered Signal"),
        dbc.CardBody(dcc.Graph(id='filtered_signal', figure=filterd_signal_fig.add_scatter(x=[],y=[])), className = "p-0"),
        dbc.CardFooter(
            dbc.Row([
                dbc.Col(dcc.Markdown('Speed', className="p-0"), width=1),
                dbc.Col(dcc.Slider(0, 50, value=0, marks=None, id = 'speed_slider',
    tooltip={"placement": "bottom", "always_visible": False}, className="p-0"), style={'padding-top':'8px'})
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
        ]),multiple=False)
),
    ]
)



def implement_tab_layout():
    layout = html.Div([
        dbc.Row(nav),
        dbc.Row(original_signal_card),
        html.Br(),
        dbc.Row(filtered_signal_card),dcc.Interval(
            id='interval_component',
            interval=1*1000, # in milliseconds
            n_intervals=0,disabled=False
        ),dcc.Store(id='time_data'),dcc.Store(id='mag_data')
        ],            
                      )
    return layout



def updating_figure_implement(figure=None,data_index=0,x=[],y=[]):
    scatter=figure.data[data_index]
    scatter.x=list(x)
    scatter.y=list(y)


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
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return df



#callback for uploading data
@app.callback(
    Output("time_data", "data"),
    Output("mag_data", "data"),
    

    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified'),
    

)

def Signal_update(contents,filenames,last_modified):
    #TODO DONT FORGET TIME PROGRESS
    print("DATA FROM FILE")
    mag=[]
    time=[]
    if contents is not None:
        print("there is data")
        dff = parse_contents(contents,filenames,last_modified)
        print("dataframe")
        print(dff)
        time=dff.iloc[:,0]
        mag=dff.iloc[:,1]
        time_np=time.to_numpy()
        mag_np=mag.to_numpy()
        time=time_np.tolist()
        mag=mag_np.tolist()
    print(len(time))
    print(len(mag))


    return  time,mag




#callback for UPDATING data
@app.callback(
    Output("original_signal", "figure"),
    Output("filtered_signal", "figure"),
    Output('upload-data', 'interval'),

    Input("store_zeros", "data"),
    Input("store_poles", "data"),
    Input("speed_slider", "value"),
    Input("interval_component", "n_intervals"),
    Input("interval_component", "disabled"),
    Input("time_data", "data"),
    Input("mag_data", "data"),
    State('upload-data', 'interval'),
    
)

def Signal_update(zeros,poles, speed,n,disabled,time,mag,interval):
    #TODO DONT FORGET TIME PROGRESS
    time=np.array(time)
    mag=np.array(mag)
    
    filter=Filter()

    for i in zeros:
            filter.add_pole_zero(complex(i),filter.filter_zeros)
    for i in poles:
        filter.add_pole_zero(complex(i),filter.filter_poles)
    print ("interval")
    print(interval)
    print("store") 
    if speed >0:
        interval= int(1000*speed)


    
    if len(time)!=0:
       
        print("UPDATING FIGURE")
       
        print("time length")
        print(len(time))
  
        

        pointsToAppend  = 500*n
        pointsToAppendOld= pointsToAppend - 500*n

        #delay_start= pointsToAppendOld -filter.get_delay_count()

        #if delay_start<0:

            #mag_delay=[]
        #else:
            #mag_delay=mag[delay_start:pointsToAppendOld]

        filtred_mag=filter.filter_samples(mag[pointsToAppendOld:pointsToAppend])


        

        time_x=time[pointsToAppendOld:pointsToAppend]
        updating_figure_implement(figure=signal_fig,x=time_x,y=mag[pointsToAppendOld:pointsToAppend])
        updating_figure_implement(figure=filterd_signal_fig,x=time_x,y=filtred_mag[pointsToAppendOld:pointsToAppend])
        
            

    elif len(time)==0:
        
        print("lasa mad5lsh 7aga")
    return  signal_fig,filterd_signal_fig,interval

