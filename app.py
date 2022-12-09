import dash
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUMEN], # LUX, FLATLY LUMEN SPACELAB YETI
                suppress_callback_exceptions=True,prevent_initial_callbacks=False,
                meta_tags=[{"name":"viewport","content":"width=device-width,initial-scale=1.0"}])



server = app.server
