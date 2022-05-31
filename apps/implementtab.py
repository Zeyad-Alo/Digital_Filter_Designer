from dash import dcc, ctx
from dash import html
import dash_bootstrap_components as dbc
import plotly.express as px
from app import app
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import numpy as np
from apps.designtab import plot
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
                dbc.Col(dcc.Slider(1, 100, value=100, marks=None, id = 'speed_slider',
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
        dbc.Row(filtered_signal_card),dcc.Interval(
            id='interval_component',
            interval=1*1000, # in milliseconds
            n_intervals=0
        ),
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

def parse_contents(contents, filename, date):
    pd.options.display.max_rows = 100000

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
            'There was an error processing this file not csv or xls.'
        ])

    return  df.loc[:,0].to_numpy() , df.loc[:,1].to_numpy()


#callback for uploading data
@app.callback(
    Output("original_signal", "figure"),
    Output("filtered_signal", "figure"),
   


    Input("upload_data", "contents"),
    Input("upload_data", "filename"),
    Input("upload_data", "last_modified"),
    Input("store_num", "data"),
    Input("store_den", "data"),
    Input("speed_slider", "value"),
    Input("interval_component", "n_intervals")

)

def Signal_update(contents,filename,last_modified,num,den,speed,n):
    #TODO DONT FORGET TIME PROGRESS
    if contents is not None:
        time,mag = [
            parse_contents(c, n, d) for c, n, d in
            zip(contents, filename, last_modified)]

        num_array=np.asarray(num)
        den_array=np.asarray(den)
        filterd_signal=sg.lfilter(num_array,den_array,mag)
        # len(time) will tell me how many sampels do i have 
        print(len(time))
        self.pointsToAppend += 50*speed
        updating_fig4(0,time[:pointsToAppend],mag[:pointsToAppend])
        updating_fig5(0,time[:pointsToAppend],filterd_signal[:pointsToAppend])
    return  fig4,fig5



