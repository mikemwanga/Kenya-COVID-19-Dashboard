import dash
import dash_bootstrap_components as dbc
from dash import dcc, html,dash_table
from dash.dependencies import Input, Output, State
from dash_bootstrap_templates import load_figure_template
from dash_iconify import DashIconify
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.graph_objects import Layout
import pathlib
import datetime as datetime
import warnings




app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], # LUX, FLATLY LUMEN SPACELAB YETI
                suppress_callback_exceptions=True,prevent_initial_callbacks=False,
                meta_tags=[{"name":"viewport","content":"width=device-width,initial-scale=1.0"}])



server = app.server
