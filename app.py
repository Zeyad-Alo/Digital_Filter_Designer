# Resources
# 1. Docs - https://plotly.com/python/getting-started/
# 2. Great github repo - https://github.com/AnnMarieW/wealthdashboard
# 3. Another one - https://github.com/ann-marie-ward/Local_Govt_Finances
# 4. Charming Data https://www.youtube.com/c/CharmingData/featured
# 5. FreeCodeCamp https://www.freecodecamp.org/news/this-quick-intro-to-dash-will-get-you-to-hello-world-in-under-5-minutes-86f8ae22ca27/
# 6. Beyond Dash - https://brianruizy.com/how-to-create-a-covid-dashboard-web-application-with-python
# 7. Book - Interactive Dashboards and Data Apps with Plotly and Dash
# https://amzn.to/3AtpZH1

import dash
import dash_bootstrap_components as dbc

# Toggle the themes at [dbc.themes.LUX]
# The full list of available themes is:
# CERULEAN, COSMO, CYBORG, DARKLY, FLATLY, JOURNAL, LITERA, LUMEN, LUX, MATERIA, MINTY, PULSE, SANDSTONE,
# SIMPLEX, SKETCHY, SLATE, SOLAR, SPACELAB, SUPERHERO, UNITED, YETI.
# https://dash-bootstrap-components.opensource.faculty.ai/docs/themes/

app = dash.Dash(__name__, suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.LUX])
server = app.server
