from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from apps.home import create_home_page
from app import app

#FINAL TODO LIST
#TODO CHANGE STORE TO GET FROM ALLPASS TO FILTER
#TODO FIX ALL PASS DATA PIPELINE
#TODO APPLY FILTER NOT FILTERING
#TODO APPLY FILTER X RANGE AUTO RANGING
#TODO SPEED NOT WORKING?
#TODO IMPLEMENT DRAGGING IN Z PLOT
#TODO UI TWEAKING (CHANGE LAPTOP)
#TODO SAMPLING FREQUENCY INPUT?
#TODO TIME RANGE OF PLOTTING
#TODO FIX ADDING CONJUGATES?


server = app.server
app.config.suppress_callback_exceptions = True

app.layout = dbc.Container(
    [
        html.H5(
                    "Digital Filter Designer",
                    className="text-center bg-dark text-white p-2",
                ),
        create_home_page(),dcc.Store(id='store_num_real'),dcc.Store(id='store_den_real'),dcc.Store(id='store_num_imag'),dcc.Store(id='store_den_imag'),
        dcc.Store(id='store_zeros'), dcc.Store(id='store_poles'), dcc.Store(id='store_corrected_zeros'), dcc.Store('store_corrected_poles')
    ],
    className="p-0",
    
    fluid=True,
    )


if __name__ == '__main__':
    app.run_server(debug=True)
    