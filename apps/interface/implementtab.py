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
                dbc.Col(dcc.Slider(1, 100, value=100, marks=None, id = 'speed_slider',
    tooltip={"placement": "bottom", "always_visible": False}, className="p-0"), style={'padding-top':'8px'})
                ]),
            )
    ],
    style={'padding-right': '0', 'padding-left': '0'}

)



nav = dbc.Nav(
    [
        dbc.NavItem(dcc.Upload(dbc.Button('Upload File',id='upload', size="sm")),
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
            'There was an error processing this file not csv or xls.'
        ])
    print(df.loc[:,0].to_numpy())
    print(df.loc[:,1].to_numpy())
    return  df.loc[:,0].to_numpy() , df.loc[:,1].to_numpy()


#callback for uploading data
@app.callback(
    Output("original_signal", "figure"),
    Output("filtered_signal", "figure"),
   


    Input('upload', 'contents'),
    State('upload', 'filename'),
    State('upload', 'last_modified'),

    Input("store_num_real", "data"),
    Input("store_num_imag", "data"),
    Input("store_den_real", "data"),
    Input("store_den_imag", "data"),

    Input("speed_slider", "value"),
    

)

def Signal_update(contents,filename,last_modified,num_real,num_imag,den_real,den_imag,speed):
    #TODO DONT FORGET TIME PROGRESS
    num=[]
    den=[]
    print("here")
    if contents is not None:
        print("there is data")
        time,mag = [
            parse_contents(c, n, d) for c, n, d in
            zip(contents, filename, last_modified)]
        print(time)
        print(mag)

        for i,r in enumerate(num_real):
            num.append(r + num_imag[i]*1j)
      
        for i,r in enumerate(den_real):
            den.append(r + den_imag[i]*1j)

        print(num)
        print(den)
        filterd_signal=sg.lfilter(num,den,mag)
        # len(time) will tell me how many sampels do i have 
        print(len(time))
        self.pointsToAppend += 50*speed
        updating_fig4(0,time[:pointsToAppend],mag[:pointsToAppend])
        updating_fig5(0,time[:pointsToAppend],filterd_signal[:pointsToAppend])
    print("here2")
    return  fig4,fig5



