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

# Reading the data
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data/").resolve()

daily_cases = pd.read_csv(DATA_PATH.joinpath("covid_daily_data.csv"))
county_prevalence = pd.read_csv(DATA_PATH.joinpath("cases_per_county.csv"))
Monthly_cases = pd.read_csv(DATA_PATH.joinpath("covid_monthly_data.csv"))
province_cases = pd.read_csv(DATA_PATH.joinpath("provice_level_cases.csv"))
age_gender_cases = pd.read_csv(DATA_PATH.joinpath("age_gender_cases_data.csv"))
age_gender_deaths = pd.read_csv(DATA_PATH.joinpath("age_gender_death_cases_data.csv"))

county_daily_data = pd.read_csv(DATA_PATH.joinpath("county_daily_data.csv"),dtype='unicode', low_memory=False)
county_daily_data["date_of_lab_confirmation"] = pd.to_datetime(county_daily_data["date_of_lab_confirmation"])
county_daily_data["Date"] = county_daily_data["date_of_lab_confirmation"]#.dt.date
county_daily_data.set_index("Date", inplace = True)

def daily_plots(observation1, observation2):
        fig = go.Figure(layout=layout)
        fig.add_trace(go.Scatter( x = daily_cases["Date"],mode='none', y = daily_cases[observation1],fill = 'tozeroy',fillcolor = fillcolor,name="daily cases"))
        fig.add_trace(go.Scatter(x = daily_cases["Date"], y = daily_cases[observation2],marker = dict(color =markercolor),name="7-day average"))
        fig.update_layout(font_color = "#4F4F4F", height = 500,hovermode="x unified")
        fig.update_yaxes( showline=True, linewidth = 0.2, linecolor = axis_color, gridcolor = "gainsboro")
        fig.update_xaxes(title = "Period", showgrid=False,showline=True,linecolor = axis_color)
        return fig
#plot of daily reported infections
fig5 = daily_plots("death_cases","moving_average_deaths")

def cumulative_cases(observation):
        fig = go.Figure(layout=layout)
        fig.add_trace(go.Scatter(x = daily_cases["Date"], y = daily_cases[observation],fill = "tozeroy",marker = dict(color =markercolor),fillcolor = fillcolor))
        fig.update_layout(font_color = "#4F4F4F", height = 500,hovermode="x unified")
        fig.update_yaxes( showline=True, linewidth = 0.2, linecolor = axis_color, gridcolor = "gainsboro")
        fig.update_xaxes(title = "Period", showgrid=False,linecolor = axis_color)
        return fig

cumilative_death_figure = cumulative_cases("Cum_Deaths")

def monthly_plot(observation):
        fig = go.Figure(layout=layout)
        fig.add_trace(go.Scatter( x = Monthly_cases["Month_year"],  y = Monthly_cases[observation],
                            fill = 'tozeroy',fillcolor = fillcolor, marker = dict(color =markercolor)))
        #fig.update_traces(mode="markers+lines", hovertemplate=None),
        fig.update_layout(font_color = "#4F4F4F",hovermode="x unified")
        fig.update_yaxes(title =  "Counts", showline=True, linewidth = 1, linecolor = "black", gridcolor = "gainsboro")
        fig.update_xaxes(title = "Period", showgrid=False,linewidth = 1, linecolor = "black")
        return fig
fig6 = monthly_plot("Death_cases")

def plot_county_based(observation):
        data = county_prevalence[["County", observation]].sort_values(observation, ascending = False)
        fig = go.Figure(layout=layout)
        fig.add_trace(go.Bar(x = data["County"], y = data[observation]))
        fig.update_layout(uniformtext_minsize = 3, font_color = "#4F4F4F", bargap =0.05)
        fig.update_traces(marker_color = fillcolor)
        fig.update_yaxes(title =  f"Total {observation}", showline=True, linewidth = 0.2, linecolor = axis_color, gridcolor = "gainsboro")
        fig.update_xaxes(title = "County", showgrid=False, showline = True)
        return fig

fig7 = plot_county_based("Death_cases")

def plot_province(observation):
    data = province_cases[["province", observation]].sort_values(observation, ascending = True)
    fig = go.Figure(layout=layout)
    fig.add_trace(go.Bar(x = data[observation], y = data["province"], orientation = "h"))
    fig.update_layout(uniformtext_minsize = 3, font_color = "#4F4F4F", bargap =0.05)
    fig.update_traces(marker_color = fillcolor)
    fig.update_yaxes(title = "Region", showline=True, linewidth = 0.2, linecolor = axis_color, gridcolor = "gainsboro")
    fig.update_xaxes(title = "Counts", showgrid=False, linecolor = axis_color,showline = True)
    return fig

fig8 = plot_province("Death_cases") #plot of death cases by region
def age_gender_plots(data):
        total_female = data["Female"].sum()
        total_male = data["Male"].sum()
        perc_female = total_female/(total_male+total_female)
        perc_male = total_male/(total_male+total_female)
        fig = px.bar(data, x = "age_groups", y = ["Female","Male"], barmode="group", color_discrete_sequence = ["#998ec3","#f1a340"])
        fig.update_layout(uniformtext_minsize = 3, font_color = "#4F4F4F", bargap =0.2, paper_bgcolor=pcolor, 
                    plot_bgcolor = pcolor, legend_title = "Gender")
        fig.update_yaxes(title = "No of Cases", showline=True, linewidth = 0.2, linecolor = "gray", gridcolor = "gainsboro")
        fig.update_xaxes(title = "Age categories", showgrid=False)
        return fig, total_female, total_male, perc_female,perc_male
age_gender_death_plot, total_female_death,total_male_death,perc_female_deaths,perc_male_deaths = age_gender_plots(age_gender_deaths)


countrywide_deaths = html.Div([
        dbc.Card([
                dbc.CardBody([
                        html.H5("COVID-19 daily death cases across Kenya", className = "text-dark fw-bold"),
                        dcc.Graph(figure = fig5)],className = "mt-3",style = cardbody_style),
                             
                dbc.CardBody([
                        html.H5("COVID-19 cumulative death cases across Kenya", className = "text-dark fw-bold"),
                        dcc.Graph(figure=cumilative_death_figure)
                                ],className = "mt-3",style = cardbody_style),

                #dbc.CardBody([dcc.Graph(figure = fig6)],className = "mt-3",style = cardbody_style),
                
                dbc.CardBody([
                    html.H5("COVID-19 death cases across counties", className = "text-dark fw-bold"),
                    dcc.Graph(figure = fig7)
                    ],className = "mt-3",style = cardbody_style),                               
                
                dbc.CardBody([
                        dbc.Row([
                                dbc.Col([html.H5("Fatalities by Region",className = "text-dark fw-bold"),
                                        dcc.Graph(figure = fig8)], width=9),
                                #dbc.Col([html.Img(src='data:image/png;base64,{}'.format(county_death_image.decode()), height = 350)]),
                        ]) ],className = "mt-3",style = cardbody_style),
                dbc.CardBody([
                        html.H5("Fatalities  by Age and Gender", className = "text-dark fw-bold"),
                        html.P("Total number of fatalities since the beginning of pandemic by age and sex",className = "text-dark"),
                        html.H6(f"Female-{total_female_death}({perc_female_deaths:.2f}%)",  className = "text-end",style = {"color":"#998ec3"}),
                        html.H6(f"Male-{total_male_death}({perc_male_deaths:.2f}%)",className = "text-end",style = {"color":"#f1a340"}),
                        dcc.Graph(figure = age_gender_death_plot)
                ], className = "mt-3",style = cardbody_style)
        ],className = "ms-5 border-0 mt-5 pt-5")              
])

data = county_daily_data[county_daily_data["outcome"] == "Dead"]
data = data[data["county"] == "Nairobi"]#.isin("Nairobi")]
data = data[["county","lab_results", "date_of_lab_confirmation"]].groupby(["county","date_of_lab_confirmation"]).count().reset_index()
fig_nai = px.line(data, x="date_of_lab_confirmation" , y = data["lab_results"].cumsum())# , color = "county",
                                #color_discrete_map ="#e7d4e8")


countywide_deaths = html.Div([
    html.Br(),
    dbc.Row([
        html.H6("A visualization of fatalities caused by COVID-19 at county level", className = "ms-3"),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.A("Filter by county", className = "text-dark"),
                    dcc.Dropdown(
                        id = "county_chosen" , 
                        options = [{"label" : name, "value" : name} for name in county_daily_data["county"].sort_values().unique()],
                        value = ["Nairobi","Mombasa"] ,  multi = True, style = {"color":"#000000"}),
                    html.Br(),html.Br(),
                    html.H6("Filter by date",className = "text-dark" ),

                    dcc.DatePickerRange(
                        id = "my-date-picker",
                        calendar_orientation = "horizontal", day_size=30,# placeholder = "Return",with_portal = False,
                        first_day_of_week = 0,with_portal=False,start_date_placeholder_text="1/3/2020",end_date_placeholder_text = ("4/2/2022"), #(0 = sunday)
                        reopen_calendar_on_clear = False,is_RTL = False, clearable = True, number_of_months_shown = 2,
                        min_date_allowed = datetime(2020, 3, 1),max_date_allowed  = datetime(2022, 11, 30),initial_visible_month = datetime(2021,2,1),
                        start_date = datetime(2020, 3, 1),end_date = datetime(2022, 11, 30),minimum_nights = 2,persistence = True,
                        persisted_props = ["start_date"],persistence_type = "session",updatemode = "singledate", show_outside_days = True,
                                          
                        )
                ]), 
            ],className="h-0",color="#FFFAFA")
        
        ],width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("Reported death cases per selected county", className = "text-dark fw-bold"),
                    dcc.Graph(id = "line_chart_deaths", figure = {}),
                    html.Br(),html.Hr(),html.Br(),
                    html.H6("Cumulative death cases per selected county", className = "text-dark fw-bold"),
                    dcc.Graph(id = "line_chart_deaths2", figure = {}),
                ], style= cardbody_style)
            ])
            
        ],width = 9),
    ], align="stretch", justify="around", className = "m-3 border-0 pt-4")
     
])


colors_pellete = {"Baringo":"#e7d4e8","Bomet":"#de77ae","Bungoma":"#6E2C00","Busia":"#3288bd","Elgeyo Marakwet":"#8E44AD ","Embu":"#67001f",
                        "Garissa":"#fde0ef","Homa Bay":"#fdae61","Isiolo":"#8e0152","Kajiado":"#8c510a","Kakamega":"#c7eae5","Kericho":"#f4a582",
                        "Kiambu":"#fee08b","Kilifi":"#F51720","Kirinyaga":"#b8e186","Kisii":"#212F3D","Kisumu":"black","Kitui":"#80cdc1",
                        "Kwale":"#dfc27d","Laikipia":"#fddbc7","Lamu":"#40004b","Machakos":"#c51b7d","Makueni":"#e6f598","Mandera":"#01665e",
                        "Marsabit":"#bababa","Meru":"#e6f5d0","Migori":"#abdda4","Mombasa":"green","Murang'a":"#d6604d","Nairobi":"blue",
                        "Nakuru":"#35978f","Nandi":"#ffffff","Narok":"#878787","Nyamira":"#4d4d4d","Nyandarua":"#762a83","Nyeri":"#b2182b",
                        "Samburu":"#b35806","Siaya":"#f46d43","Taita Taveta":"#f1b6da","Tana River":"#c2a5cf","Tharaka Nithi":"#9970ab",
                        "Trans Nzoia":"#7fbc41","Turkana":"#276419","Uasin Gishu":"#d53e4f","Vihiga":"#1a1a1a","Wajir":"#ffffbf","West Pokot":"#7f3b08"}

def seven_day_average(data,column):
    window_size = 7
    moving_average = []
    data_col = data[column]
    for i in range(len(data)):
        if i + window_size < len(data_col):
            moving_average.append(round(np.mean(data_col[i:i+window_size]),1))
        else:
            moving_average.append(np.mean(data_col[i:len(data_col)])) 
    data["moving_average"] = moving_average
    return data

@app.callback( [Output("line_chart_deaths", "figure"),
                Output("line_chart_deaths2", "figure")],
                [Input("county_chosen", "value"), 
                Input("my-date-picker" , "start_date"),
                Input("my-date-picker" , "end_date")])

def update_graph_card(county, start_date, end_date):
    if len(county) == 0:
        return dash.no_update
    else:
        data = county_daily_data[county_daily_data["outcome"] == "Dead"]
        data = data[data["county"].isin(county)]
        data = data.sort_index().loc[start_date : end_date]
        data = data[["county","lab_results", "date_of_lab_confirmation"]].groupby(["county","date_of_lab_confirmation"]).count().reset_index()
        
        fig2 = px.line(data, x="date_of_lab_confirmation" , y = data["lab_results"].cumsum() , color = "county",
                                color_discrete_map =colors_pellete)
        fig2.update_yaxes(title = "Cumulative Deaths", showline=True, linewidth = 0.2, linecolor = "gray", gridcolor = "gainsboro")
        fig2.update_xaxes(title = "Date Reported",linecolor = "gray", showline=True,showgrid=False)
        fig2.update_traces(mode = 'lines', marker_color = "#7086CE")
        fig2.update_layout(hovermode="x unified",paper_bgcolor=pcolor,plot_bgcolor = pcolor,uniformtext_minsize = 3, font_color = "#4F4F4F", bargap =0.05) 

        data_average = seven_day_average(data, "lab_results")
        fig = px.line(data_average, x="date_of_lab_confirmation" , y = data["moving_average"],range_y = [0,15], color = "county",
                        color_discrete_map =colors_pellete)
        fig.update_yaxes(title = "7-day average death cases", showline=True, linewidth = 0.2, linecolor = "black", gridcolor = "gainsboro")
        fig.update_xaxes(title = "Date Reported", showline=True,showgrid=False,linecolor = "black",)
        fig.update_traces(mode = 'lines', marker_color = "#7086CE")
        fig.update_layout(height = 500,hovermode="x unified",paper_bgcolor=pcolor,plot_bgcolor = pcolor,uniformtext_minsize = 3, font_color = "#4F4F4F", bargap =0.05)
        return fig,fig2