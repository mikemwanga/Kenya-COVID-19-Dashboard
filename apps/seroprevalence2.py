import dash
from dash import dcc, html,dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import pandas as pd
import pathlib
from plotly.subplots import make_subplots
import plotly.express as px
from app import app

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data/").resolve()

sero_data = pd.read_excel(DATA_PATH.joinpath("KWTRP_serosurveillance_data_Dashboard_09Sep2022.xlsx"))
daily_cases = pd.read_csv(DATA_PATH.joinpath("covid_daily_data.csv"))

markercolor = "#8B0000"
color_patterns = ["#FF5733","#8E44AD","#2236A0","#252525","#1B6311"]
#pcolor = "#FFFAFA"
pcolor = "rgba(0,0,0,0)"
pcolor_home = "#E6E6E6"
cardbody_style = {"background-color":pcolor}
tickfont = dict(size=10)
titlefont = 12
gridcolor = "#e0e0e0"

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
                fig.update_yaxes(title_text = "Average % Anti IgG seroprevalence",linecolor = "black",ticks="outside",col=1,nticks=20,
                                 secondary_y = False,range = [0,1],gridcolor = gridcolor)
                fig.update_xaxes(tickfont = tickfont,dtick="M1",tickformat="%b\n%Y",linecolor = "black",ticks="outside",nticks=5)#tickformat="%b\n%Y"
                fig.update_layout(plot_bgcolor = pcolor,paper_bgcolor = pcolor,
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
                fig.update_yaxes(tickfont = tickfont,title_text = "cumulative cases", linecolor = "black", secondary_y = True, range = [0,400000])
                fig.update_yaxes(tickfont = tickfont,title_text = "seroprevalence",linecolor = "black",ticks="outside",col=1,
                                 nticks=10,secondary_y = False,range = [0,1],gridcolor = gridcolor)
                fig.update_xaxes(tickfont = tickfont,dtick="M1",tickformat="%b\n%Y",linecolor = "black",ticks="outside",nticks = 1)
                fig.update_layout(plot_bgcolor = pcolor,paper_bgcolor = pcolor,legend_orientation ="h")
                return fig
sero_class = sero_prevalence()
subfig = sero_class.seroplot()

card_style = "bg-light border rounded-3 shadow"
classname_col = "bg-light bg-opacity-20 g-1 justify-content-center p-2 m-2"
col_title = "text-center text-black fw-bolder" 
style_text ={"font-size":14,"text-align":"center"}


layout = html.Div([
        dbc.Row([
                    dbc.Col([
                        html.H5("Visualization of vaccination across the country", style ={"text-align":"start"}),
                        html.Hr(),
                    ], width = 11, xxl=10),
                    
                    
                    #html.H5("Countrywide Summary"),
        ],justify="center", className = "mb-2 ms-4 me-4 ps-4 pe-4 mt-5 pt-5"),
    
        #html.H4("Summary of the average anti-IgG seroprevalence by population",className = "text-dark, text-center"),
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure = subfig,responsive = True,style = {"width":"1000px","height":"600px"})
            ],width = 8,lg=9,className = card_style)
        ],justify="center",className = classname_col,align = "center"),
        
        
        dcc.RadioItems(
                        id = "sero_pop",
                        options = ["Blood donors","Health workers"],
                        value = "Blood donors",
                        labelStyle = {"display":"inline-block"},
                        #inputStyle = {"margin-top":"1px"}
                    ),
        dbc.Row([
            dbc.Col([
                html.P("Seroprevalence in Blood donors",className = col_title),
                dcc.Graph(id = "graph"),
                html.Br(),
                html.P("Seroprevalence in Blood donors based on gender",className = col_title),
                dcc.Graph(id = "graph3")
            ],width = 5,className = "bg-light"),
            dbc.Col([
                html.P("Seroprevalence in Blood donors based on age",className = col_title),
                dcc.Graph(id = "graph2"),
                html.Br(),
                html.P("Seroprevalence in Blood donors based on region",className = col_title),
                dcc.Graph(id = "graph4")
            ],width = 5,className = "bg-light"),
                
        ],justify="center",className = classname_col,align = "center"),
        
])

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
                age_fig.update_layout(title = None,plot_bgcolor = pcolor, paper_bgcolor = pcolor)
                age_fig.update_xaxes(tickfont = tickfont, dtick="M1",tickformat="%b\n%Y",linecolor = "black",ticks="outside")
                age_fig.update_yaxes(gridcolor = gridcolor,title_text = "seroprevalence",linecolor = "black",ticks="outside")
                return age_fig
        
        def gender_plot(self):
                gender_data = self.data[self.data["Sex"].isin(["Female","Male"])]
                gender_fig = px.timeline(gender_data, x_start="start", x_end = "finish", y = "Anti-spike_perc", color = "Sex", 
                                        hover_name="Sex", range_y = [0,.6], hover_data={"Anti-spike_perc":":0%"})
                gender_fig.update_layout(title = None,plot_bgcolor = pcolor, paper_bgcolor = pcolor)
                gender_fig.update_xaxes(tickfont = tickfont,dtick="M1",tickformat="%b\n%Y",linecolor = "black",ticks="outside")
                gender_fig.update_yaxes(gridcolor = gridcolor,title_text = "seroprevalence",linecolor = "black",ticks="outside")
                return gender_fig
        def region_plot(self):
                region_data = self.data.loc[(self.data["Age in years"] == "15 - 64") & (self.data["Sex"]=="All")]
                region_fig = px.timeline(region_data, x_start="start", x_end = "finish", y = "Anti-spike_perc", color = "Region", 
                                        hover_name="Region", range_y = [0,0.3], hover_data={"Anti-spike_perc":":0%"})
                region_fig.update_layout(title = None
                                         ,plot_bgcolor = pcolor, paper_bgcolor = pcolor)
                region_fig.update_traces(width = 0.003)
                region_fig.update_xaxes(tickfont = tickfont,dtick="M1",tickformat="%b\n%Y",linecolor = "black",ticks="outside")
                region_fig.update_yaxes(gridcolor = gridcolor,title_text = "seroprevalence",linecolor = "black",ticks="outside")
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
                                                hover_name="Age in years",range_x = ["2020-06-01", "2021-07-01"], 
                                                range_y = [0,.3], hover_data={"Anti-spike_perc":":0%"})
        fig.update_traces(width=0.01)
        fig.update_layout(title = None,plot_bgcolor = pcolor, paper_bgcolor = pcolor)
        fig.update_xaxes(tickfont = tickfont,dtick="M1",tickformat="%b\n%Y",linecolor = "black",ticks="outside")
        fig.update_yaxes(gridcolor = gridcolor,title_text = "seroprevalence",linecolor = "black",ticks="outside")
        return fig

    def gender_plot(self):
        fig=px.timeline(self.health_workers_gender, x_start="start", x_end = "finish", y = "Anti-spike_perc", color = "Sex", 
                                                hover_name="Sex",range_x = ["2020-06-01", "2021-07-01"], 
                                                range_y = [0,.3], hover_data={"Anti-spike_perc":":0%"})
        fig.update_traces(width=0.01)
        fig.update_layout(title = None,plot_bgcolor = pcolor, paper_bgcolor = pcolor)
        fig.update_xaxes(tickfont = tickfont,dtick="M1",tickformat="%b\n%Y",linecolor = "black",ticks="outside")
        fig.update_yaxes(gridcolor = gridcolor,title_text = "seroprevalence",linecolor = "black",ticks="outside")
        return fig

    def region_plot(self):
        fig=px.timeline(self.health_workers_region, x_start="start", x_end = "finish", y = "Anti-spike_perc", color = "Region", 
                                                hover_name="Region",range_x = ["2020-06-01", "2021-02-01"], 
                                                range_y = [0,.6], hover_data={"Anti-spike_perc":":0%"})
        fig.update_traces(width=0.01)
        fig.update_layout(title = None,plot_bgcolor = pcolor, paper_bgcolor = pcolor)
        fig.update_xaxes(tickfont = tickfont,dtick="M1",tickformat="%b\n%Y",linecolor = "black",ticks="outside")
        fig.update_yaxes(gridcolor = gridcolor,title_text = "seroprevalence",linecolor = "black",ticks="outside")

        return fig
    


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


