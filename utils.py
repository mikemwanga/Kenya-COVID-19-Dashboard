import dash
from dash import dcc, html,dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from dash_iconify import DashIconify
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.graph_objects import Layout
import pathlib
import datetime as datetime
import warnings
import numpy as np
from dash import dash_table as dt
from apps import home as hm
warnings.filterwarnings('ignore')
load_figure_template("flatly") #cerulean,flatly,journal,litera,pulse,sandstone
from app import app
import geopandas as gpd
from plotly.subplots import make_subplots


#Set path
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("./data/").resolve()

#visuals
pcolor = "#FFFAFA"
plot_color = "rgba(0,0,0,0)"
pcolor_home = "#efedf5"
pcolor_white = "white"
axis_color = "black"
fillcolor = "#6baed6"
markercolor = "#3C565B"
style = {"height":"200px", "width":"300px"}
margin = dict(l=10, r=10, t=5, b=5)
layout = Layout(plot_bgcolor = pcolor,paper_bgcolor=pcolor)
cardbody_style = {"background-color":pcolor}
cardbody_style_home = {"background-color":pcolor_home}
cardbody_style_vac = {"background-color":pcolor_home, "height":"200%"}
color_patterns = ["#e41a1c","#377eb8","#4daf4a","#984ea3","#073763"]
tickfont = 9
titlefont = 12
tickfont_dict = dict(size=10)

card_class = "text-center"
classname_col = "bg-light bg-opacity-20 g-1 justify-content-center p-2 m-2" 
class_style = "shadow-sm bg-light border rounded g-1"
col_title = "text-center text-black fw-normal"
col_style  = {"margin-left":"15px","margin-right":"0px"}
style_label={"font-size":35, "align":"center"}
style_text ={"font-size":15,"text-align":"center"}
classname_shadow = "shadow border rounded-2 justify-content-center"
col_class = "bg-white align-self-center"
hr_style = {"height":"3vh", "align":"center"}
hr_class = "bg-secondary bg-opacity-10 justify-content-center mb-0 pb-0"
col1_class = "ms-2"
val_class = "fs-4 fw-normal ms-3"
pcolor_vaccination = "#5D6D7E"
bg_color = "rgba(0,0,0,0)"
gridcolor = "#e0e0e0"
#margin_size = "1px"