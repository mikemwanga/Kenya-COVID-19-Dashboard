import dash
import dash_bootstrap_components as dbc

dbc_css = ("https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css], # LUX, FLATLY LUMEN SPACELAB YETI
                suppress_callback_exceptions=True,prevent_initial_callbacks=False,
                meta_tags=[{"name":"viewport","content":"width=device-width,initial-scale=1.0"}])



server = app.server
