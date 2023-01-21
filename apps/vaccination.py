import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.graph_objects import Layout
import pathlib
from datetime import datetime as datetime
import numpy as np

from app import app


#set variables
pcolor = "#FFFAFA"
pcolor_home = "#E6E6E6"
axis_color = "black"
fillcolor = "#6baed6"
markercolor = "#8B0000"
layout = Layout(plot_bgcolor = pcolor,paper_bgcolor=pcolor)
cardbody_style = {"background-color":pcolor}
cardbody_style_home = {"background-color":pcolor_home}
cardbody_style_vac = {"background-color":pcolor_home, "height":"200%"}
color_patterns = ["#FF5733","#8E44AD","#2236A0","#252525","#1B6311"]

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data/").resolve()

county_vaccination = pd.read_csv(DATA_PATH.joinpath("county_vaccination.csv"))
vaccination_updates = pd.read_csv(DATA_PATH.joinpath("vaccination_metadata_october.csv"), index_col="Group")
daily_updates_moh =  pd.read_excel(DATA_PATH.joinpath("daily_updates_metadata.xlsx"))
vaccination_updates.columns = pd.to_datetime(vaccination_updates.columns)#, format="%d/%m/%Y")

vaccine_last_updated = vaccination_updates.columns[-1].strftime(format="%d-%B-%Y")
total_vaccine_doses = vaccination_updates.iloc[0][-1] #first rowlast column
fully_vaccinated_adults = vaccination_updates[vaccination_updates.index == "Fully vaccinated adult population (18 years and above)"].iloc[0][-1]
partially_vaccinated_adults = vaccination_updates[vaccination_updates.index == "Partially vaccinated adult population (18 years and above)"].iloc[0][-1]
booster_doses_total = vaccination_updates[vaccination_updates.index == "Total Booster Doses"].iloc[0][-1]
teenage_12_18_yrs = vaccination_updates[vaccination_updates.index == "Total doses administered to children (12yrs to below 18yrs)"].iloc[0][-1]
fully_vaccinated_teens = vaccination_updates[vaccination_updates.index == "Fully vaccinated children (12yrs to below 18yrs)"].iloc[0][-1]
partially_vaccinated_teens = vaccination_updates[vaccination_updates.index == "Partially vaccinated children (12yrs to below 18yrs)"].iloc[0][-1]
last_7_days_df = vaccination_updates.iloc[:,-7:]
last_7_days_df =  last_7_days_df.loc[["Total doses administered","Fully vaccinated adult population (18 years and above)"]]
total_doses_7_days = int(last_7_days_df.loc[["Total doses administered"]].iloc[-1].iat[-1].replace(",","")) - int(last_7_days_df.loc[["Total doses administered"]].iloc[0].iat[0].replace(",",""))
fully_vaccinated_last_7 = int(last_7_days_df.loc[["Fully vaccinated adult population (18 years and above)"]].iloc[-1].iat[-1].replace(",","")) - int(last_7_days_df.loc[["Fully vaccinated adult population (18 years and above)"]].iloc[0].iat[0].replace(",",""))

vac_fig = go.Figure(layout=layout)
vac_fig.add_trace(go.Bar(x = county_vaccination["Proportion_vaccinated"],
                                        y = county_vaccination["County"], \
                                        orientation = "h",text = county_vaccination["Proportion_vaccinated"], textposition = "outside"))
vac_fig.update_layout(uniformtext_minsize = 3, font_color = "#000000", bargap =0.2,font_size=10,autosize=False, width = 600, height=800)
vac_fig.update_traces( marker_color =  "#1F77B4")
vac_fig.update_xaxes(title = "Proportion Vaccinated", showgrid=True,showline=True, linewidth = 0.1, linecolor = axis_color, gridcolor = "gainsboro")


layout = html.Div([
            dbc.Row([
                html.H4("Vaccination in Kenya", className = "text-dark fw-bold ms-5"),
                html.P("Vaccination data extracted from Ministry of Health website", className = "text-dark ms-5"),
                #html.P(f"Last Updated : {vaccine_last_updated}",className = "text-info ms-5"),
            ]),
            
            dbc.Row([                             
                dbc.Col([
                        dbc.CardBody([
                                html.H5(f"{total_vaccine_doses}",style = {"color":markercolor},className = "fw-bold"),
                                html.P("Vaccines Received"),
                                html.Hr()
                                ])]),
                dbc.Col([
                        dbc.CardBody([
                                html.H5(f"{fully_vaccinated_adults}",style = {"color":markercolor},className = "fw-bold"),
                                html.P("Fully vaccinated adults"),
                                html.Hr()]),]),
                dbc.Col([
                        dbc.CardBody([
                                html.H5(f"{partially_vaccinated_adults}",style = {"color":markercolor},className = "fw-bold"),
                                html.P("Partially vaccinated adults"),
                                html.Hr()]),]),
                dbc.Col([
                        dbc.CardBody([
                                html.H5(f"{teenage_12_18_yrs}",style = {"color":markercolor},className = "fw-bold"),
                                html.P("Doses administered to teenages"),
                                html.Hr()]),]),
                dbc.Col([
                        dbc.CardBody([
                                html.H5(f"{fully_vaccinated_teens}",style = {"color":markercolor},className = "fw-bold"),
                                html.P("Fully vaccinated teenages"),
                                html.Hr()]),]),
                dbc.Col([
                        dbc.CardBody([
                                html.H5(f"{partially_vaccinated_teens}",style = {"color":markercolor},className = "fw-bold"),
                                html.P("Partially vaccinated teenages"),
                                html.Hr()]),]),
                dbc.Col([
                        dbc.CardBody([
                                html.H5(f"{booster_doses_total}",style = {"color":markercolor},className = "fw-bold"),
                                html.P("Booster Doses"),
                                html.Hr()]),]),             
            ],className = "border-0 ms-4 mb-3 me-3" ,style = cardbody_style),
        
        
            dbc.Card([
                dbc.CardBody([
                        html.H5("Proportion of fully vaccinated persons by county", className = "text-dark ms-5"),
                        dcc.Graph(figure = vac_fig)
                ]),                        
            ],className = "border-0 ms-4 me-3",style = cardbody_style)
])