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
from plotly.subplots import make_subplots

from app import app

markercolor = "#8B0000"
color_patterns = ["#FF5733","#8E44AD","#2236A0","#252525","#1B6311"]
pcolor = "#FFFAFA"
pcolor_home = "#E6E6E6"
cardbody_style = {"background-color":pcolor}

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data/").resolve()

sero_data = pd.read_excel(DATA_PATH.joinpath("KWTRP_serosurveillance_data_Dashboard_09Sep2022.xlsx"))
daily_cases = pd.read_csv(DATA_PATH.joinpath("covid_daily_data.csv"))

class sero_prevalence:
        def __init__(self):
                sero_data["Period"] = sero_data[["Month(s)", "Year"]].astype(str).agg(" ".join, axis=1)
                data = sero_data[["Population","Region", "start","finish", "Anti-spike_perc"]]
                self.data_period = data.groupby(["start","finish","Population",])["Anti-spike_perc"].mean()
                self.data_period = self.data_period.to_frame().reset_index()
                self.data_period["start"] = pd.to_datetime(self.data_period["start"])
                self.data_period["finish"] = pd.to_datetime(self.data_period["finish"])

        def seroplot(self):
                fig = make_subplots(specs = [[{"secondary_y":True}]], shared_xaxes=True)
                line_fig = px.timeline(self.data_period, x_start="start", x_end = "finish", y = "Anti-spike_perc", color = "Population", 
                                        hover_name="Population", range_y = [0,1], hover_data={"Population":False, "Anti-spike_perc":":0%"}, 
                                        color_discrete_sequence= color_patterns )
                line_fig.update_traces(width=0.01, type = "bar", textposition = "outside")
                cum_fig = px.line(daily_cases, x = "Date",  y = "Cum_Cases", color_discrete_sequence=[markercolor]) 
                cum_fig.update_traces(yaxis="y2")
                fig.add_traces(cum_fig.data + line_fig.data)
                fig.update_yaxes(title_text = "Cumulative Cases",ticks="outside", secondary_y = True, linecolor = "black")
                fig.update_yaxes(title_text = "Average % Anti IgG seroprevalence",linecolor = "black",ticks="outside",col=1,nticks=20,secondary_y = False,range = [0,1])
                fig.update_xaxes(dtick="M1",tickformat="%b\n%Y",linecolor = "black",ticks="outside")
                fig.update_layout(plot_bgcolor = pcolor,paper_bgcolor = pcolor, width = 1200, height = 600,
                                legend = dict(yanchor  = "top",y=1,x=0.01,xanchor="left"),legend_orientation ="h")
                
                return fig

        def population_plot(self, population):
                self.population = population
                fig = make_subplots(specs = [[{"secondary_y":True}]], shared_xaxes=True)
                pop_data = self.data_period[self.data_period["Population"] == population]
                line_fig = px.timeline(pop_data, x_start="start", x_end = "finish", y = "Anti-spike_perc", color = "Population", 
                    hover_name="Population", range_y = [0,1], hover_data={"Population":False, "Anti-spike_perc":":0%"}, 
                    color_discrete_sequence= color_patterns)
                line_fig.update_traces(width=0.01, type = "bar", textposition = "outside")
                cum_fig = px.line(daily_cases, x = "Date",  y = "Cum_Cases", color_discrete_sequence=['black',"red"]) 
                cum_fig.update_traces(yaxis="y2")
                fig.add_traces(cum_fig.data + line_fig.data)
                fig.update_yaxes(title_text = "cumulative COVID-19 cases", linecolor = "black", secondary_y = True, range = [0,400000])
                fig.update_yaxes(title_text = "Average % Anti IgG seroprevalence",linecolor = "black",ticks="outside",col=1,nticks=20,secondary_y = False,range = [0,1])
                fig.update_xaxes(dtick="M1",tickformat="%b\n%Y",linecolor = "black",ticks="outside")
                fig.update_layout(width = 900,height = 600,plot_bgcolor = pcolor,paper_bgcolor = pcolor,legend_orientation ="h")
                return fig
sero_class = sero_prevalence()
subfig = sero_class.seroplot()

class blood_donor_strat:
        """
        Returns population-based plots relative to Age of the studied group, gender (Male/Female) and regions.

        """
        def __init__(self):
                
                self.data = sero_data[sero_data["Population"] == "Blood donors"]

        def age_plot(self):
                age_data = self.data[self.data["Age in years"].isin(["15 - 24","25 - 34", "35 - 44","45 - 54","55 - 64"])]
                age_fig = px.timeline(age_data, x_start="start", x_end = "finish", y = "Anti-spike_perc", color = "Age in years", 
                                        color_discrete_sequence= color_patterns,hover_name="Age in years", range_y = [0,.6], hover_data={"Anti-spike_perc":":0%"})
                age_fig.update_layout(title = "Seroprevalence in Blood donors based on Age",plot_bgcolor = pcolor, paper_bgcolor = pcolor)
                age_fig.update_xaxes(dtick="M1",tickformat="%b\n%Y",linecolor = "black",ticks="outside")
                age_fig.update_yaxes(title_text = "Average % Anti IgG seroprevalence",linecolor = "black",ticks="outside")
                return age_fig
        
        def gender_plot(self):
                gender_data = self.data[self.data["Sex"].isin(["Female","Male"])]
                gender_fig = px.timeline(gender_data, x_start="start", x_end = "finish", y = "Anti-spike_perc", color = "Sex", 
                                        hover_name="Sex", range_y = [0,.6], hover_data={"Anti-spike_perc":":0%"})
                gender_fig.update_layout(title = "Seroprevalence in Blood donors based on gender",plot_bgcolor = pcolor, paper_bgcolor = pcolor)
                gender_fig.update_xaxes(dtick="M1",tickformat="%b\n%Y",linecolor = "black",ticks="outside")
                gender_fig.update_yaxes(title_text = "Average % Anti IgG seroprevalence",linecolor = "black",ticks="outside")
                return gender_fig
        def region_plot(self):
                region_data = self.data.loc[(self.data["Age in years"] == "15 - 64") & (self.data["Sex"]=="All")]
                region_fig = px.timeline(region_data, x_start="start", x_end = "finish", y = "Anti-spike_perc", color = "Region", 
                                        hover_name="Region", range_y = [0,0.3], hover_data={"Anti-spike_perc":":0%"})
                region_fig.update_layout(title = "Seroprevalence in Blood donors based on regions sampled",width = 900, height = 800,plot_bgcolor = pcolor, paper_bgcolor = pcolor)
                region_fig.update_traces(width = 0.003)
                region_fig.update_xaxes(dtick="M1",tickformat="%b\n%Y",linecolor = "black",ticks="outside")
                region_fig.update_yaxes(title_text = "Average % Anti IgG seroprevalence",linecolor = "black",ticks="outside")
                return region_fig

class health_workers_strat:
    """
    Returns population-based plots relative to Age of the health workers group, gender (Male/Female) and regions.
    """
    def __init__(self):
        health_workers = sero_data[sero_data["Population"] == "Health workers"]
        self.health_workers_age = health_workers[health_workers["Age in years"].isin(["18 - 30","31 - 40", "41 - 50","51 - 60"])]
        self.health_workers_gender = health_workers[health_workers["Sex"].isin(["Male","Female"])]
        self.health_workers_region =  health_workers.loc[(health_workers["Sex"] == "All") & (health_workers["Age in years"] == "≥18") ]
    
    def age_plot(self):
        fig=px.timeline(self.health_workers_age, x_start="start", x_end = "finish", y = "Anti-spike_perc", color = "Age in years", 
                                                hover_name="Age in years",range_x = ["2020-06-01", "2021-07-01"], range_y = [0,.3], hover_data={"Anti-spike_perc":":0%"})
        fig.update_traces(width=0.01)
        fig.update_layout(title = "Seroprevalence in health workers based on Age",plot_bgcolor = pcolor, paper_bgcolor = pcolor)
        fig.update_xaxes(dtick="M1",tickformat="%b\n%Y",linecolor = "black",ticks="outside")
        fig.update_yaxes(title_text = "Average % Anti IgG seroprevalence",linecolor = "black",ticks="outside")
        return fig

    def gender_plot(self):
        fig=px.timeline(self.health_workers_gender, x_start="start", x_end = "finish", y = "Anti-spike_perc", color = "Sex", 
                                                hover_name="Sex",range_x = ["2020-06-01", "2021-07-01"], range_y = [0,.3], hover_data={"Anti-spike_perc":":0%"})
        fig.update_traces(width=0.01)
        fig.update_layout(title = "Seroprevalence in health workers based on gender",plot_bgcolor = pcolor, paper_bgcolor = pcolor)
        fig.update_xaxes(dtick="M1",tickformat="%b\n%Y",linecolor = "black",ticks="outside")
        fig.update_yaxes(title_text = "Average % Anti IgG seroprevalence",linecolor = "black",ticks="outside")
        return fig

    def region_plot(self):
        fig=px.timeline(self.health_workers_region, x_start="start", x_end = "finish", y = "Anti-spike_perc", color = "Region", 
                                                hover_name="Region",range_x = ["2020-06-01", "2021-02-01"], range_y = [0,.6], hover_data={"Anti-spike_perc":":0%"})
        fig.update_traces(width=0.01)
        fig.update_layout(title = "Seroprevalence in Blood donors based on region sampled",plot_bgcolor = pcolor, paper_bgcolor = pcolor)
        fig.update_xaxes(dtick="M1",tickformat="%b\n%Y",linecolor = "black",ticks="outside")
        fig.update_yaxes(title_text = "Average % Anti IgG seroprevalence",linecolor = "black",ticks="outside")

        return fig



layout_summary = html.Div([

        dbc.Card([
            dbc.Row([
                html.H6("Summary of the average anti-IgG seroprevalence by population",className = "text-dark"),
                dbc.Col(
                        dbc.CardBody([html.H4("47.9%",className = "fw-bold", style = {"color":markercolor}), html.H6(["Blood Donors",html.Br(),"June 2021"])])
                ),
                dbc.Col(
                        dbc.CardBody([html.H4("4.6%",className = "fw-bold", style = {"color":markercolor}), html.H6(["ANC Attendees",html.Br(),"November 2020"])])
                ),
                dbc.Col(
                        dbc.CardBody([html.H4("29.7%",className = "fw-bold", style = {"color":markercolor}), html.H6(["Healthcare Workers",html.Br(),"December 2020"])])
                ),
                dbc.Col(
                        dbc.CardBody([html.H4("46.7%",className = "fw-bold", style = {"color":markercolor}), html.H6(["Trucking Crew",html.Br(),"October 2020"])])
                ),
                dbc.Col(
                        dbc.CardBody([html.H4("90.3%",className = "fw-bold", style = {"color":markercolor}), html.H6(["HDSS Residents",html.Br(),"June 2022"])])
                ),
            ])
        ],style = cardbody_style,className = "ms-3 mt-5 me-3 border-0 pt-5"),
        
        html.Hr(className = "ms-3 me-3"),
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure = subfig)
            ],className = "ms-5")
        ],justify="around",className = "ms-3 mt-3 me-3",style = cardbody_style),
        
        html.Hr(className = "ms-3 me-3"),
])
        



sero_by_population = html.Div([
    dbc.Row([
        dbc.Col([
            
                dbc.CardBody([
                    html.H6("Select population"),
                    dcc.RadioItems(
                        id = "sero_pop",
                        options = ["Blood donors","Health workers"],
                        value = "Blood donors",
                        labelStyle = {"display":"inline-block"},
                        #inputStyle = {"margin-top":"1px"}
                    )        
                ],style = cardbody_style)  
            
        ],width = 2),#className = "mt-1 ms-2"), #h-10 
        dbc.Col([
            dbc.Card([
                
                dbc.CardBody([
                    html.P("Summary of seropositivity."),
                    html.Div(dcc.Graph("graph"),className = "ml-3"),
                ],style = cardbody_style),
                html.Hr(),
                dbc.CardBody([
                    html.Div(dcc.Graph("graph2"),className = "ml-3"),
                ],style = cardbody_style),
                html.Hr(),
                dbc.CardBody([
                    html.Div(dcc.Graph("graph3"),className = "ml-3"),
                ],style = cardbody_style),
                html.Hr(),
                dbc.CardBody([
                    html.Div(dcc.Graph("graph4"),className = "ml-3")
                ],style = cardbody_style),
                
            ],className = "border-0")
                
            
            
        ],width = 8,className = "mt-3"),
    ],align = "center", className = "ms-3 me-3 mt-5 pt-5")
])

@app.callback([Output("graph", "figure"),
               Output("graph2", "figure"),
               Output("graph3", "figure"),
               Output("graph4", "figure")],
              [Input("sero_pop", "value")])

def render(population):
        if population == "Blood donors":
               
                fig1 = sero_class.population_plot(population)
                fig2 = blood_donor_strat().age_plot()
                fig3 = blood_donor_strat().gender_plot()
                fig4 = blood_donor_strat().region_plot()
                return fig1, fig2, fig3, fig4

        elif population == "Health workers":
                fig1 = sero_class.population_plot(population)
                fig2 = health_workers_strat().age_plot()
                fig3 = health_workers_strat().gender_plot()
                fig4 = health_workers_strat().region_plot()
                return fig1, fig2, fig3, fig4