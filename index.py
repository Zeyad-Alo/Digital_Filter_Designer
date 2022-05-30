from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from apps.interface.home import create_home_page
from apps.page_2 import create_page_2
from apps.page_3 import create_page_3
from app import app

server = app.server
app.config.suppress_callback_exceptions = True

app.layout = dbc.Container(
    [
        html.H5(
                    "Digital Filter Designer",
                    className="text-center bg-dark text-white p-2",
                ),
        create_home_page(),dcc.Store(id='store_num'),dcc.Store(id='store_den')
    ],
    className="p-0",
    
    fluid=True,
                      )


if __name__ == '__main__':
    app.run_server(debug=True)
