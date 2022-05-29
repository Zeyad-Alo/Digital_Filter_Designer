from dash import dcc, ctx
from dash import html
from dash import callback_context
from apps.navbar import create_navbar
import dash_bootstrap_components as dbc
import plotly.express as px
from app import app
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import numpy as np
import cmath
import math 
from apps.modules import filtercreator
from scipy import signal as sg


zeros_reals=[0]
zeros_imags=[0]
poles_reals=[0]
poles_imags=[0]
zeros_all=[]
poles_all=[]
zeros_all_conj=[]
poles_all_conj=[]
z_plane=[]
mag_zeros=[]
mag_imag=[]
SAMPLING_FREQ=44100
# intializing figures in order to update them later(their layouts)

fig = go.FigureWidget(layout=dict(template='plotly_dark', height = 300, margin_b = 40, margin_l = 40, margin_r = 40, margin_t = 40))
fig2= go.FigureWidget(layout=dict(template='plotly_dark', height = 300, margin_b = 40, margin_l = 40, margin_r = 40, margin_t = 40))
fig3= go.FigureWidget(layout=dict(template='plotly_dark', height = 300, margin_b = 40, margin_l = 40, margin_r = 40, margin_t = 40))
#   PLOT FUNCTIONS
#THIS IS A PLACEHOLDER IN ORDER TO INITIALIZE OUR CARDS 
def plot():
    fig = go.Figure(layout=dict(template='plotly_dark', height = 300, margin_b = 40, margin_l = 40, margin_r = 40, margin_t = 40))
    return fig
# for the second plot TO INITIALIZE THE MAGNITUDE CARD
def plot_2():
    fig2.add_scatter(x=[0],y=[0])
    return fig2

# for the third plot TO INITIALIZE THE MAGNITUDE CARD
def plot_3():
    fig3.add_scatter(x=[0],y=[0])
    return fig3
  
#   TO INITIALIZE THE ZPLANE CARDS 

def zplane_plot():
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


# 

def appending_zeros(zeros):
    print("appending zeros")
    zeros_all.append(zeros)
    print(zeros_all)
    zeros_reals.append(zeros.real)
    print(zeros_reals)
    zeros_imags.append(zeros.imag)
    print(zeros_imags)
    print("appending done")

def appending_poles(poles):
    print("appending poles")
    poles_all.append(poles)
    poles_reals.append(poles.real)
    poles_imags.append(poles.imag)

def updating_fig(data,x,y,symbol):
    print("updating zplot")
    scatter = fig.data[data]
    scatter.x = list(x)
    scatter.y = list(y)
    scatter.marker.symbol = symbol
    print("updating done")

def updating_fig2(data,x,y):
    scatter = fig2.data[data]
    scatter.x = list(x)
    scatter.y = list(y)

def updating_fig3(data,x,y):
    scatter = fig3.data[data]
    scatter.x = list(x)
    scatter.y = list(y)

#   PS: CARDS ARE UI ELEMENTS ONLY THE ORGANIZE FUNCTIONAL CONTENT
zplane_card = dbc.Card(
    [
        dbc.CardHeader("Z-Plane"),
        dbc.CardBody(dcc.Graph(id='z_plane', figure= zplane_plot()), className = "p-0"
    )],
    )


#   CONTENT INSIDE COLLAPSE CARD
collapse_content = html.Div(
    [
        dbc.Row([
            dbc.Col(dcc.Markdown(['Mag'], className="p-0", style={'margin-top':'0px'}), width=3, style={'margin-top':'0px'}),
            dbc.Col(dcc.Slider(0, 2, value=0, marks=None, id = 'mag_slider',
    tooltip={"placement": "bottom", "always_visible": True}, className="p-0"), style={'padding-top':'8px'})
            ],
            ),
        html.Br(),
        dbc.Row([
            dbc.Col(dcc.Markdown('$Theta$', mathjax=True, className="p-0", style={'margin-top':'0px'}), width=3, style={'margin-top':'0px'}),
            dbc.Col(dcc.Slider(0, 180, value=0, marks=None,id = 'theta_slider',
    tooltip={"placement": "bottom", "always_visible": True}, className="p-0"), style={'padding-top':'8px'})
            ],
            ),
        dbc.Row([
            dbc.Col(),
            dbc.Col(dbc.Button("Add!", id = 'add_button',n_clicks=0, color="primary", size='sm'), width=3),
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
                    [dbc.DropdownMenuItem("Zeros", id="dropdown_zeros"), dbc.DropdownMenuItem("Poles",id="dropdown_poles"), dbc.DropdownMenuItem("All", id="dropdown_all")],
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
        dbc.CardBody(dcc.Graph(id='mag_response', figure=plot_2()), className = "p-0"),
    ],
)



phase_card = dbc.Card(
    [
        dbc.CardHeader("Phase Response"),
        dbc.CardBody(dcc.Graph(id='phase_response', figure=plot_3()), className = "p-0"),
    ],
)




#   PUTS EVERYTHING IN DESIGN TAB TOGETHER IN A LAYOUT
def design_tab_layout():
    layout = html.Div([
        dbc.Row([
            dbc.Col([zplane_card,html.Br(), options_card], width=3),
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


SAMPLING_FREQ=44100
#   CALLBACK FOR Mag and Theta
#call backs should have atleast one output and one input it takes 2 arguments first the id of the card and second the type of the date 
#that will be returned
@app.callback(
    Output("z_plane", "figure"),
    Output("mag_response", "figure"),
    Output("phase_response", "figure"),


    Input("add_button","n_clicks"),
    Input("mag_slider", "value"),
    Input("theta_slider", "value"),
    State("zeros_button", "active"),
    State("poles_button", "active"),
    Input("apply_button","n_clicks"),
    Input("conj_checklist","value"),
    Input("dropdown_zeros","n_clicks"),
    Input("dropdown_poles","n_clicks"),
    Input("dropdown_all","n_clicks"),

)

def zplane_mag_phase_update(nclicks,mag_value,theta_value,z_active,p_active,apply_click,activated,zclicks,pclicks,allclicks):
    
 # this is initialized in order to know which button is pressed
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    # theta value and mag value are taken from the sliders
    z_axis=cmath.rect(mag_value,(theta_value*np.pi/180))
    #this loop is entred when both the zeros button is open and the user pressed add
    if z_active and 'add_button' in changed_id:
        print("zeros")
        appending_zeros(z_axis)
        
        updating_fig(1,zeros_reals,zeros_imags,'circle-open')
        print(zeros_reals)
        
        #this loop is entred when both the poles button is open and the user pressed add
    elif p_active and 'add_button' in changed_id:
        print("poles")
        appending_poles(z_axis)

        updating_fig(2,poles_reals,poles_imags,'x-open')

    
    if 'add_button' in changed_id:  
        print("phase and mag resp")
        mag=[]
        phase=[]
        num,den=sg.zpk2tf(zeros_all, poles_all, 1)
        w,freq_resp=sg.freqz(num, den, fs=SAMPLING_FREQ)
        for h in freq_resp:
            polar=cmath.polar(h)
            mag.append(polar[0])
            phase.append(polar[1])
        
        updating_fig2(0,w,mag)
        
        updating_fig3(0,w,phase)
    

    if activated and 'apply_button' in changed_id  :  
        #TODO PHASE/MAG RESPONSE GETS UPDATED EVEN IF THERE ALL CONJUGETS ARE PRESENT
        mag=[]
        phase=[]
        print("activated and apply_button")
        for z1 in zeros_all:
            for z2 in zeros_all:
                print("z1:")
                print(z1)
                print("z2")
                print(z2)
                #if the conjugets of the elements are present
                if( (z1.real == z2.real )and( z2.imag == - z1.imag) ):
                    print("zeros same")
                    break
                else:
                    print("zeros not same")
                    z_conj=np.conj(z1) 
                    print(z_conj)
                    zeros_all_conj.append(z_conj)
     
        for p1 in poles_all:
            for p2 in poles_all:
                #if the conjugets of the elements are present
                if (p1.real == p2.real )and( p2.imag == - p1.imag):
                    break
                else:
                    p_conj=np.conj(p1)
                    poles_all_conj.append(p_conj)
        
        for z in zeros_all_conj:
            appending_zeros(z)

        for p in poles_all_conj:
            appending_poles(p)

        num,den=sg.zpk2tf(zeros_all, poles_all, 1)
        w,freq_resp=sg.freqz(num, den, fs=SAMPLING_FREQ)
        for h in freq_resp:
            polar=cmath.polar(h)
            mag.append(polar[0])
            phase.append(polar[1])
        
        updating_fig(1,zeros_reals,zeros_imags,'circle-open')
        updating_fig(2,poles_reals,poles_imags,'x-open')
        updating_fig2(0,w,mag)
        updating_fig3(0,w,phase)
    


    #if 'dropdown_zeros' in changed_id:
    #    print("zeros_clear")
    #    print(zeros_all)
    #    zeros_all=[]
    #    zeros_reals=[0]
    #    zeros_imags=[0]
    #    print(zeros_all)
    #    print(zeros_reals)
    #    print(zeros_imags)
    #    print("removed all zeros")
    #    updating_fig(1,zeros_reals,zeros_imags,'circle-open')

    #    mag=[]
    #    phase=[]
    #    num,den=sg.zpk2tf(zeros_all, poles_all, 1)
    #    w,freq_resp=sg.freqz(num, den, fs=SAMPLING_FREQ)
    #    for h in freq_resp:
    #        polar=cmath.polar(h)
    #        mag.append(polar[0])
    #        phase.append(polar[1])
        
    #    updating_fig2(0,w,mag)
        
    #    updating_fig3(0,w,phase)

    #elif 'dropdown_poles' in changed_id:
    #    print("poles_clear")
    #    for p in poles_all:
    #        poles_all.remove(p)
    #    for p in poles_reals:
    #        poles_reals.remove(p)
    #    for p in poles_imags:
    #        poles_imags.remove(p)
    #    updating_fig(2,0,0,'x-open')




    #    mag=[]
    #    phase=[]
    #    num,den=sg.zpk2tf(zeros_all, poles_all, 1)
    #    w,freq_resp=sg.freqz(num, den, fs=SAMPLING_FREQ)
    #    for h in freq_resp:
    #        polar=cmath.polar(h)
    #        mag.append(polar[0])
    #        phase.append(polar[1])
        
    #    updating_fig2(0,w,mag)
        
    #    updating_fig3(0,w,phase)


    #elif 'dropdown_all' in changed_id:
    #    print("clear_all")
    #    for z in zeros_all:
    #        zeros_all.remove(z)
    #    for z in zeros_reals:
    #        zeros_reals.remove(z)
    #    for z in zeros_imags:
    #        zeros_imags.remove(z)
    #    updating_fig(1,0,0,'circle-open')
    #    for p in poles_all:
    #        poles_all.remove(p)
    #    for p in poles_reals:
    #        poles_reals.remove(p)
    #    for p in poles_imags:
    #        poles_imags.remove(p)
    #    pdating_fig(2,0,0,'x-open')
    #    updating_fig2(0,0,0)
    #    updating_fig3(0,0,0)



    print("here")
    

    # we return the figure in the "figure =" of zplot (find z plot card)
    return fig,fig2,fig3




