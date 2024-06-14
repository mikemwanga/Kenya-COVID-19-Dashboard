import dash
from dash import dcc, html,dash_table,callback
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import dash_mantine_components as dmc
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
load_figure_template(["sketchy", "cyborg", "minty"]) #cerulean,flatly,journal,litera,pulse,sandstone,minty
from app import app
#import geopandas as gpd
from plotly.subplots import make_subplots
from datetime import datetime,date,timedelta
import time


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
margin_county = dict(l=10, r=10, t=35, b=5)
layout = Layout(plot_bgcolor = pcolor,paper_bgcolor=pcolor)
cardbody_style = {"background-color":pcolor}
cardbody_style_home = {"background-color":pcolor_home}
cardbody_style_vac = {"background-color":pcolor_home, "height":"200%"}

color_patterns = ['#0000FF','#1f78b4','#00FF00','#008000','#fb9a99','#e31a1c','#fdbf6f','#ff7f00','#cab2d6','#6a3d9a','#ffff99','#b15928',\
                "#FF00FF",'#800080','#808080'] 

tickfont = 11
titlefont = 12
tickfont_dict = dict(size=9)
card_class = "text-center"
classname_col = "bg-secondary bg-opacity-10 g-1 justify-content-center p-2 m-2" 
class_style = "shadow-sm bg-light border rounded g-1"

col_title = "text-center text-secondary fw-bold mb-0 ms-4"
col_title_start = "text-start text-secondary fw-bold mb-0"
style_title = {"font-size":16}

description_text = "text-start text-secondary mb-2 mt-2 ms-4"
description_style_title = {"font-size":13}

col_style  = {"margin-left":"15px","margin-right":"0px"}
style_label={"font-size":35, "align":"center"}
style_text ={"font-size":14,"text-align":"center","color" :"#566573" }
classname_shadow = "shadow border rounded-2 justify-content-center"
col_class = "bg-white align-self-center"
hr_style = {"height":"3vh", "align":"center"}
hr_class = "bg-secondary bg-opacity-10 justify-content-center mb-0 pb-0"
col1_class = "ms-2"
val_class = "fs-2 fw-normal ms-2"
######hiv status########################
colors = {'Not recorded':'#DEDEDE','Empty':'#DEDEDE','No':'#077c86','Yes':'#e83357','missing':'#db2153',#eeeeee'
          'Negative':'#bfa07f','Positive':'#c93071','Unknown':'#d9a744'}

classname_col = "bg-secondary bg-opacity-10 g-1 justify-content-center p-2 m-2" 

midrow_classname = "g-1 justify-content-center mt-1"# p-2 m-2"
val_class = "fs-4 fw-normal ms-3"
col1_class = "ms-2"

central = '#794d65'
western='#c39054'
coast = '#3182bd'

discrete_color = [central,western,coast]
region_map_color ={'Central':central,'Western':western,'Coast':coast}
col_title = "text-start text-secondary fw-bold mb-0 ms-4 mt-2"
section_title = "text-start text-secondary ms-1 mt-2 text-start fw-bold fs-5"
male_color = '#00698f'# 
female_color = '#de6f1d' # 
gender_color =[female_color,male_color]
gridcolor = '#e5e4e2'
linecolor ='#170B3B'
plot_color = "rgba(0,0,0,0)"
line_class = 'align-items-start mb-0 ms-1'
line_style = {'width':'70%'}

space = html.B(className='mb-4')
line = html.Hr()

ring_color = '#3d86b8'
fill_color='#333338'

tabs_styles = {
    'height': '44px'
}

tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    #'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#87ceeb',# '#119DFF',
    'color': 'black',
    'padding': '6px',
    'fontWeight': 'bold'
}


plotly_display = {'displaylogo': False,'scrollZoom':False,
                'modeBarButtonsToRemove': ['pan','autoScale','resetScale2d','zoom2d','zoomIn2d','zoomOut2d', 'hoverCompareCartesian', 
                                           'resetViewMapbox','hoverClosestCartesian', 'toggleSpikelines']}
    

pcolor_vaccination = "#5D6D7E"
bg_color = "rgba(0,0,0,0)"
gridcolor = "#e0e0e0"
margin_size = "1px"

div = "bg-secondary bg-opacity-10"

plotly_display = {'displaylogo': False,'displayModeBar':False}

hoverlabel=dict(bgcolor="white",font_size=16,font_family="Tahoma")

marker_text = "#67001f"

#intervals
interval = dcc.Interval(id = "interval-component", interval = 60 * 60 * 12 *1000, n_intervals = 0)

#sero content

sero_content_modal = "This is a summary of several serological studies conducted among different populations since the beginning of the pandemic.\
                    This serves to inform the level of COVID-19 infection across the country in \
                        different study populations. Check referenced seroprevalence studies in the footer notes. Use the dropdown menu to view seroprevalence in \
                        specific groups"
                        
vaccination_content = "This page provides overview of reported vaccination metrics of the number of persons vaccinated countrywide and percentage per county. \
                        Data for this section is exrtracted from the Kenya Ministry of Health platform and Ourworld in data. \
                        Reference links: (https://www.health.go.ke/#1621663315215-d6245403-4901 and https://ourworldindata.org/coronavirus/country/kenya). "

county_content = "This is a summary of cases, fatalities and disease budden at county levels. The section allows realtime comparison between selected counties \
                    . Use the dropdown menu to achieve this."
                    
home_content = "The home page provides a summary of COVID-19 prevalence across the country. The top boxes show total metrices on cases, deaths, recoveries and \
                overall positivity.  The testing updates section provides information on last tests results reported by MOH. This includes reported cases, sample size\
                positivity, reported fatalities and reported recoveries. A summary of cases at counties, epidemic waves on cases and fatalities and disease prevalence \
                based on gender and sex is displayed."
#acknowledgment section
reference = dbc.Row([
                dbc.Col(width=1),
                dbc.Col([
                    html.Img(src=dash.get_asset_url("../assets/kwtrp_logo.png"),style = {"width":"20vw","height":"5vh"})
                ],width=2,style = {"margin-right":"10px",
                                   "display":"flex","align-items": "center","justify-content": "center",}),
                dbc.Col([
                    html.Img(src=dash.get_asset_url("../assets/moh_kenya.png"),style = {"width":"6vw","height":"10vh"})
                ],width=1, style = {"margin-left":"10px","display":"flex","align-items": "center","justify-content": "center",}),
                dbc.Col([
                    html.Img(src=dash.get_asset_url("../assets/fcdo_logo.png"),style = {"width":"10vw","height":"11vh"})
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
                    # dcc.Link("jmwanga@kemri-wellcome.org",title="email_me",href="mailto:jmwanga@kemri-wellcome.org",target="_blank",
                    #          style = {"font-size":10,"margin-right":"10px"}),
                    dcc.Link("ggithinji@kemri-wellcome.org",title="email_me",href="mailto:ggithinji@kemri-wellcome.org",target="_blank",
                             style = {"font-size":10})

                ], width = {"size":6,"offset":1},xxl=4, className = "mb-3"),
                dbc.Col(width=1),
        ],className = "bg-secondary bg-opacity-10 border-top border-1 shadow justify-content-center ms-2 ps-2 mt-3 pt-3 mb-4")

