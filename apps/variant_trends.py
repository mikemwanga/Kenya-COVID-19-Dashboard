import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pathlib

from app import app
# Reading the data
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data/").resolve()

variant_data = pd.read_table(DATA_PATH.joinpath("variant_month_data.txt"))
average_df_clean = pd.read_csv(DATA_PATH.joinpath("average_weekly_submission_to_gsaid.csv"), parse_dates = ["date_sampled"])
variants_kenya = pd.read_table(DATA_PATH.joinpath("variant_data_kenya.tsv"))
variants_kenya["Month"] = pd.to_datetime(variants_kenya["Month"], format = "%Y-%m-%d")
kenya_data = pd.read_table(DATA_PATH.joinpath("kenya.metadata_01_30_11.tsv"))

gridcolor="lightgray"
pcolor = "#FFFAFA"
cardbody_style = {"background-color":pcolor}
fillcolor = "#6baed6"
markercolor = "#8B0000"
margin = dict(l=20, r=25, t=20, b=20)
pcolor_white = "white"


class Variants:
        def __init__(self, percentage):
             self.percentage = percentage
        def variants_prevalence(self):
             fig= px.bar(variant_data, x = "months_period", y = self.percentage, color="variant_type",hover_data={"percentage":":.1%"}, 
                color_discrete_sequence = ["#AC3B3B","#377eb8","#4daf4a","#984ea3","#ff7f00","#E1B113","#6666FF"])
             fig.update_layout(paper_bgcolor = pcolor,plot_bgcolor = pcolor)
             fig.update_xaxes(title = "Time")
             fig.update_yaxes(title = "Proportion")
             return fig

plots = Variants("percentage")
variant_plot = plots.variants_prevalence()

#variants plot
#variant plot
fig_var = px.bar(variants_kenya, x = "Month", y = "percentage", color="variant",range_x=["2020-01-01","2022-12-31"],
                 color_discrete_sequence = ["#1b9e77","#d95f02","#7570b3","#e7298a","#8111A5","#e6ab02","#a6761d"])
#fig_var.update_traces(textfont_size=10,textposition="outside", text = variant_values["Frequency"])
fig_var.update_xaxes(nticks = 10,linecolor = "black",ticks="outside",tickfont = dict(size=10),title = None)
fig_var.update_yaxes(linecolor = "black",ticks="outside",tickfont = dict(size=12),title ="Proportion", title_font = {"size":12})
fig_var.update_layout(legend=dict(itemsizing="constant",title = None,orientation = "h", font=dict(size=10)),plot_bgcolor = pcolor,
                      margin = margin,paper_bgcolor = pcolor,)


kenya_data = kenya_data[["date","pangolin_lineage"]].groupby(["date","pangolin_lineage"])[["pangolin_lineage"]].count().\
    rename(columns = {"pangolin_lineage":"Frequency"}).reset_index()
kenya_data = kenya_data[kenya_data["pangolin_lineage"] != "Unassigned"]
kenya_data["date"] = pd.to_datetime(kenya_data["date"],format = "%Y-%m-%d")
kenya_data["pangolin_lineage"].unique()
fig_kenya = px.scatter(kenya_data, x = "date",y = "pangolin_lineage",size= "Frequency", color = "pangolin_lineage")
fig_kenya.update_xaxes(title = "Collection date", linecolor = "black",tickfont = dict(size=8), title_font = dict(size=10),\
                    gridcolor = gridcolor, gridwidth = 0.5, nticks = 8)
fig_kenya.update_yaxes(title = None, linecolor = "black",tickfont = dict(size=8),gridcolor = gridcolor, gridwidth = 0.5)
fig_kenya.update_layout(plot_bgcolor = pcolor,margin=margin,paper_bgcolor = pcolor,
    legend=dict(itemsizing="constant",title = None,orientation = "v", font=dict(size=8)))    
    
    

def plot_time(data):
        data["date_sampled"] = pd.to_datetime(data["date_sampled"], format="%Y/%m/%d")
        total = len(data)
        fig = px.scatter(data, x = "date_sampled",y = "days_to_submission", 
                                        trendline="lowess", trendline_options=dict(frac=0.3),height=400)
        fig.update_xaxes(nticks = 15,title = "sampling date",linecolor = "black",ticks="outside",tickfont_size=10)
        fig.update_yaxes(title = "average number of days to submission",linecolor = "black",ticks="outside")
        fig.update_layout(xaxis_tickformat='%b\n%Y', paper_bgcolor=pcolor, plot_bgcolor = pcolor)
        fig.update_traces(marker = dict(color = fillcolor),line = dict(color=markercolor))
        return fig,total
fig_submission,all_kenya = plot_time(average_df_clean)


layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.Label("Temporal prevalence of SARS-COV-2 variants in Kenya", 
                   style = {"text-align":"center","font-size":14},className = "fw-bold text-dark ms-4"),
            
            dcc.Graph(figure = fig_var,responsive = True,style = {"height":"300px", "width":"800px"})
        ], width = 8,xxl=10),
    ],justify = "center", className = "ms-5 mt-5 pt-5"),
    
    dbc.Row([
        html.Hr(className = "me-2 ms-2"),
        dbc.Col([
            html.H6(f"SARS-CoV-2 lineages observed in Kenya in the last 30 days (1 - 30 November 2022)",
                    style = {"text-align":"start","font-size":14},className = "fw-bold text-dark ms-4"),
            
            dcc.Graph(figure = fig_kenya, responsive = True, style = {"height":"400px", "width":"800px"})
        ], width = 8,xxl=10)
    ],justify = "center",className = "ms-5 mt-3 pt-3")
])
