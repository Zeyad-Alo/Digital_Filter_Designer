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
from apps.modules import filtercreator



zeros_reals=[0]
zeros_imags=[0]
poles_reals=[0]
poles_imags=[0]
z_plane=[]
mag_zeros=[]
mag_imag=[]
# intializing figures in order to update them later(their layouts)

fig = go.FigureWidget(layout=dict(template='plotly_dark', height = 300, margin_b = 40, margin_l = 40, margin_r = 40, margin_t = 40))
fig2= go.FigureWidget(layout=dict(template='plotly_dark', height = 300, margin_b = 40, margin_l = 40, margin_r = 40, margin_t = 40))
#   PLOT FUNCTIONS
#THIS IS A PLACEHOLDER IN ORDER TO INITIALIZE OUR CARDS 
def plot():
    fig = go.Figure(layout=dict(template='plotly_dark', height = 300, margin_b = 40, margin_l = 40, margin_r = 40, margin_t = 40))
    return fig
# for the second plot TO INITIALIZE THE MAGNITUDE CARD
def plot_2():
    fig2.add_scatter(x=[1],y=[1],mode="markers")
    return fig2


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
    fig.add_scatter(x=[zeros_reals],y=[zeros_imags],mode="markers")
    #data 2 for poles points
    fig.add_scatter(x=[poles_reals],y=[poles_imags],mode="markers")
    # this is returned in the 'figure=' of the zplane plot (look for the z plane card)
    return fig

#   PS: CARDS ARE UI ELEMENTS ONLY THE ORGANIZE FUNCTIONAL CONTENT
zplane_card = dbc.Card(
    [
        dbc.CardHeader("Z-Plane"),
        dbc.CardBody(dcc.Graph(id='z_plane', figure= zplane_plot(), className = "p-0"),
    )],
    )


#   CONTENT INSIDE COLLAPSE CARD
collapse_content = html.Div(
    [
        dbc.Row([
            dbc.Col(dcc.Markdown(['Mag'], className="p-0", style={'margin-top':'0px'}), width=3, style={'margin-top':'0px'}),
            dbc.Col(dcc.Slider(0, 0.99, value=0, marks=None, id = 'mag_slider',
    tooltip={"placement": "bottom", "always_visible": True}, className="p-0"), style={'padding-top':'8px'})
            ],
            ),
        html.Br(),
        dbc.Row([
            dbc.Col(dcc.Markdown('$Theta$', mathjax=True, className="p-0", style={'margin-top':'0px'}), width=3, style={'margin-top':'0px'}),
            dbc.Col(dcc.Slider(0, 179, value=0, marks=None,id = 'theta_slider',
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
                    [dbc.DropdownMenuItem("Zeros"), dbc.DropdownMenuItem("Poles"), dbc.DropdownMenuItem("All")],
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
        dbc.CardBody(dcc.Graph(id='phase_response', figure=plot()), className = "p-0"),
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


#symbol = 'x-open' symbol = 'circle-dot' symbol = 'circle-open-dot'  symbol = 'x-open-do'
#   CALLBACK FOR Mag and Theta
#call backs should have atleast one output and one input it takes 2 arguments first the id of the card and second the type of the date 
#that will be returned
@app.callback(
    Output("z_plane", "figure"),

    Input("add_button","n_clicks"),
    Input("mag_slider", "value"),
    Input("theta_slider", "value"),
    State("zeros_button", "active"),
    State("poles_button", "active"),

)

def zplane_update(nclicks,mag_value,theta_value,z_active,p_active):
 # this is initialized in order to know which button is pressed
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    # theta value and mag value are taken from the sliders
    z_axis=cmath.rect(mag_value,(theta_value*np.pi/180))
    #this loop is entred when both the zeros button is open and the user pressed add
    if z_active and 'add_button' in changed_id:
        print("zeros")
        zeros_reals.append( z_axis.real)
        zeros_imags.append( z_axis.imag)
        
        scatter_zero = fig.data[1]
        scatter_zero.x = list(zeros_reals)
        scatter_zero.y = list(zeros_imags)
        scatter_zero.marker.symbol = 'circle-open'
#this loop is entred when both the poles button is open and the user pressed add
    elif p_active and 'add_button' in changed_id:
        print("poles")
        poles_reals.append( z_axis.real)
        poles_imags.append( z_axis.imag)
        
        scatter_poles = fig.data[2]
        scatter_poles.x = list(poles_reals)
        scatter_poles.y = list(poles_imags)
        scatter_poles.marker.symbol = 'x-open'

    print("here")
    

    # we return the figure in the "figure =" of zplot (find z plot card)
    return fig

#kol ali ta7t dah shelo
#CALL BACKS FOR MAGNITUDE GRAPH
mag1=[]
mag2=[0]
mag_zeros=[]
mag_poles=[]
multplication =1
SAMPLING_FREQ=44100
@app.callback(
    Output("mag_response", "figure"),
    Input("add_button","n_clicks"),

)
def sampling_freq(nclicks):
    fmax=SAMPLING_FREQ/2
    f=np.linspace(0, fmax, num=3)
    w=f*np.pi/fmax #changed tp pi
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'add_button' in changed_id:    
        for freq in w:
            print("w:")
            print(freq)
            for i,r in enumerate(poles_reals):
                x1=r
                y1=poles_imags[i]
                radius = 1
                x2= radius * np.cos(freq)
                y2= radius * np.sin(freq)
                dist = np.sqrt( (x2 - x1)**2 + (y2 - y1)**2 )
                mag_poles.append(dist)
                print("poles_distance")
                print(dist)
            for i,r in enumerate(zeros_reals):
                x1=r
                y1=zeros_imags[i]
                radius = 1
                x2= radius * np.cos(freq)
                y2= radius * np.sin(freq)
                dist = np.sqrt( (x2 - x1)**2 + (y2 - y1)**2 )  
                mag_zeros.append(dist)
                print("zeros_distance")
                print(dist)
            for z,p in enumerate(mag_poles):
                mag1.append(mag_zeros[z]/p)
                print("z/p")
                print(mag1)
            for q in mag1:
                multiplication=q*multplication 
            mag2.append(multplication)             
        scatter_mag = fig2.data[0]
        scatter_mag.x = list(w)
        scatter_mag.y = list(mag2)
    return fig2


