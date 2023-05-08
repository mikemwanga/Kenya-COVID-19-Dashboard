import dash
from dash import dcc, html,dash_table,callback
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
load_figure_template("sandstone") #cerulean,flatly,journal,litera,pulse,sandstone,minty
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
markercolor = "#bdbdbd"#cccccc"#"#3C565B"
style = {"height":"200px", "width":"300px"}
margin = dict(l=10, r=10, t=5, b=5)
layout = Layout(plot_bgcolor = pcolor,paper_bgcolor=pcolor)
cardbody_style = {"background-color":pcolor}
cardbody_style_home = {"background-color":pcolor_home}
cardbody_style_vac = {"background-color":pcolor_home, "height":"200%"}
color_patterns = ["#d95f02","#377eb8","#4daf4a","#984ea3","#073763"]  #e41a1c
tickfont = 9
titlefont = 12

tickfont_dict = dict(size=9)

card_class = "text-center"
classname_col = "bg-secondary bg-opacity-10 g-1 justify-content-center p-2 m-2" 
class_style = "shadow-sm bg-light border rounded g-1"
col_title = "text-center text-secondary fw-bold mb-0"

col_style  = {"margin-left":"15px","margin-right":"0px"}
style_label={"font-size":35, "align":"center"}
style_text ={"font-size":14,"text-align":"center","color" :"#566573" }
classname_shadow = "shadow border rounded-2 justify-content-center"
col_class = "bg-white align-self-center"
hr_style = {"height":"3vh", "align":"center"}
hr_class = "bg-secondary bg-opacity-10 justify-content-center mb-0 pb-0"
col1_class = "ms-2"
val_class = "fs-4 fw-normal ms-3"
pcolor_vaccination = "#5D6D7E"
bg_color = "rgba(0,0,0,0)"
gridcolor = "#e0e0e0"
margin_size = "1px"

div = "bg-secondary bg-opacity-10"
#margin = dict(l=5, r=5, t=5, b=5)

marker_text = "#67001f"

#intervals
interval = dcc.Interval(id = "interval-component", interval = 3600 * 24 *1000, n_intervals = 0)

#acknowledgment section
reference = dbc.Row([
                dbc.Col([
                    html.Img(src= "../assets/kwtrp_logo.png",style = {"width":"8vw","height":"7vh"})
                ],width=1,style = {"margin-right":"10px",
                                   "display":"flex","align-items": "center","justify-content": "center",}),
                dbc.Col([
                    html.Img(src= "../assets/moh_kenya.png",style = {"width":"6vw","height":"10vh"})
                ],width=1, style = {"margin-left":"10px","display":"flex","align-items": "center","justify-content": "center",}),
                dbc.Col([
                    html.Img(src= "../assets/fcdo_logo.png",style = {"width":"10vw","height":"11vh"})
                ],width=1, style = {"display":"flex","align-items": "center","justify-content": "center",}),

                dbc.Col([

                    html.P("Other Information",className = "fw-bolder text-decoration-underline mb-0 pb-0",style = {"font-size":12}),
                    html.Label(["Developed and maintained by KEMRI-Wellcome Trust, in collaboration with National Public Health Surveillance Laboratory \
                        at Ministry of Health, Kenya. Bayesian Model for Early Warning estimation was developed by ", \
                            html.A("Laura et al.,2022", href="https://doi.org/10.1101/2022.01.01.21268131")," \
                            Funding support from Foreign Commonwealth and Development Office (FCDO)."],
                        style = {"font-size":10}),

                    html.P("Data Source",className = "fw-bolder text-decoration-underline mb-0 pb-0",style = {"font-size":12}),
                    dcc.Link("Ministry of Health,Kenya (NPHL)",href="https://www.health.go.ke/",
                             style = {"font-size":10, "margin-right":"10px"}),
                    dcc.Link("Global Science Initiative(GISAID)",href="https://gisaid.org", 
                             style = {"font-size":10,"margin-right":"10px"}),
                    dcc.Link("Sero-study", href = "https://www.nature.com/articles/s41467-021-24062-3",
                             style = {"font-size":10}),

                    html.P("Contact Us",className = "fw-bolder text-decoration-underline mb-0 pb-0 mt-2",style = {"font-size":12}),
                    dcc.Link("jmwanga@kemri-wellcome.org",title="email_me",href="mailto:jmwanga@kemri-wellcome.org",target="_blank",
                             style = {"font-size":10,"margin-right":"10px"}),
                    dcc.Link("ggithinji@kemri-wellcome.org",title="email_me",href="mailto:ggithinji@kemri-wellcome.org",target="_blank",
                             style = {"font-size":10})

                ], width = {"size":7,"offset":1})
        ],className = "bg-secondary bg-opacity-10 border-top border-1 shadow justify-content-center ms-2 ps-2 mt-4 pt-4")
