from gc import callbacks
from logging.handlers import TimedRotatingFileHandler
from pickle import TRUE
from pydoc import classname
from statistics import multimode
from datetime import datetime as dt
from tkinter.tix import ExFileSelectBox

import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.graph_objects import Layout
import base64
import os
from plotly.subplots import make_subplots

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
#app.config.suppress_callback_exceptions=True

#data load and preprocessing
county_daily_data = pd.read_csv("county_daily_data.csv",dtype='unicode', low_memory=False)
county_daily_data["date_of_lab_confirmation"] = pd.to_datetime(county_daily_data["date_of_lab_confirmation"])
county_daily_data["Date"] = county_daily_data["date_of_lab_confirmation"]#.dt.date
county_daily_data.set_index("Date", inplace = True)

covid_data = pd.read_csv("covid_data_processed.csv", index_col=False, low_memory=False)
total_cases = covid_data[covid_data["lab_results"] == "Positive"]["lab_results"].value_counts().sum()
discharged = covid_data[covid_data["outcome_death_Discharge_still_in_hospital_"] \
                        == "Discharge"]["outcome_death_Discharge_still_in_hospital_"].value_counts().sum()
dead = covid_data[covid_data["outcome_death_Discharge_still_in_hospital_"] \
                        == "Dead"]["outcome_death_Discharge_still_in_hospital_"].value_counts().sum()
##plots-----------------------------------------------------------------------------------------------------------------------------
pcolor = "#FFFAFA"
layout = Layout(plot_bgcolor = pcolor,paper_bgcolor=pcolor)
cardbody_style = {"background-color":pcolor}

daily_cases = pd.read_csv("covid_daily_data.csv")
def daily_plots(observation):
        fig = go.Figure(layout=layout)
        fig.add_trace(go.Scatter( x = daily_cases["Date"],  y = daily_cases[observation], 
                        fill = "tonext",marker = dict(color ="#3D59AB" )))
        fig.update_traces(mode="markers+lines", hovertemplate=None),
        fig.update_layout(font_color = "#4F4F4F", height = 500,hovermode="x unified")
        fig.update_yaxes( showline=True, linewidth = 0.2, linecolor = "gray", gridcolor = "gainsboro")
        fig.update_xaxes(title = "Period", showgrid=False)
        return fig

fig2 = daily_plots("Reported_Cases") #plot of daily reported infections
fig5 = daily_plots("death_cases") #plot of daily death cases

##plot for cumulative cases----------------------------------------------------------------------------------------------------------
def cumulative_cases(observation):
        fig = go.Figure(layout=layout)
        fig.add_trace(go.Scatter(x = daily_cases["Date"],  y = daily_cases[observation],fill = "tozeroy",marker = dict(color ="#3D59AB" )))
        fig.update_traces(mode="markers+lines", hovertemplate=None)
        fig.update_layout(font_color = "#4F4F4F", height = 500,hovermode="x unified")
        fig.update_yaxes( showline=True, linewidth = 0.2, linecolor = "gray", gridcolor = "gainsboro")
        fig.update_xaxes(title = "Period", showgrid=False)
        return fig

cumilative_cases_figure = cumulative_cases("Cum_Cases")
cumilative_death_figure = cumulative_cases("Cum_Deaths")

#plot2 monthly cases----------------------------------------------------------------------------------------------------------------------------
Monthly_cases = pd.read_csv("covid_monthly_data.csv")
#plotting for cases and deaths. Recovered there is alot of missing data
def monthly_plot(observation):
        fig = go.Figure(layout=layout)
        fig.add_trace(go.Scatter( x = Monthly_cases["Month_year"],  y = Monthly_cases[observation],
                            fill = 'tonext', marker = dict(color = "#3D59AB")))
        fig.update_traces(mode="markers+lines", hovertemplate=None),
        fig.update_layout(font_color = "#4F4F4F",hovermode="x unified")
        fig.update_yaxes(title =  "Counts", showline=True, linewidth = 1, linecolor = "gray", gridcolor = "gainsboro")
        fig.update_xaxes(title = "Period", showgrid=False,linewidth = 1, linecolor = "gray")
        return fig
fig1 = monthly_plot("Reported_cases")
fig6 = monthly_plot("Death_cases")

#plot3 County level prevalence cases------------------------------------------------------------------------------------------------------------
county_prevalence = pd.read_csv("cases_per_county.csv") #county names, covid-cases, death cases and recoveries
def plot_county_based(observation):
        data = county_prevalence[["County", observation]].sort_values(observation, ascending = False)
        fig = go.Figure(layout=layout)
        fig.add_trace(go.Bar(x = data["County"], y = data[observation]))
        fig.update_layout(uniformtext_minsize = 3, font_color = "#4F4F4F", bargap =0.05)
        fig.update_traces(marker_color = "#7086CE")
        fig.update_yaxes(title =  f"Total {observation}", showline=True, linewidth = 0.2, linecolor = "gray", gridcolor = "gainsboro")
        fig.update_xaxes(title = "County", showgrid=False)
        return fig

fig3 = plot_county_based("cases")
fig7 = plot_county_based("Death_cases")

#plot4 Region level prevalence cases------------------------------------------------------------------------------------------------------------
province_cases = pd.read_csv("provice_level_cases.csv")
def plot_province(observation):
    data = province_cases[["province", observation]].sort_values(observation, ascending = True)
    fig = go.Figure(layout=layout)
    fig.add_trace(go.Bar(x = data[observation], y = data["province"], orientation = "h"))
    fig.update_layout(uniformtext_minsize = 3, font_color = "#4F4F4F", bargap =0.05)
    fig.update_traces(marker_color = "#7086CE")
    fig.update_yaxes(title = "Region", showline=True, linewidth = 0.2, linecolor = "gray", gridcolor = "gainsboro")
    fig.update_xaxes(title = "Counts", showgrid=False)
    return fig

fig4 = plot_province("cases") #regional covid_cases
fig8 = plot_province("Death_cases") #plot of death cases by region

#plot4 County level prevalence cases------------------------------------------------------------------------------------------------------------
county_cases_image = base64.b64encode(open('plot_county_covid_cases.png', 'rb').read())
county_death_image = base64.b64encode(open('plot_county_death_cases.png', 'rb').read())

#vaccinated proportion------------------
county_vaccination = pd.read_csv("county_vaccination.csv")
vac_fig = go.Figure(layout=layout)
vac_fig.add_trace(go.Bar(x = county_vaccination["Proportion_vaccinated"],
                                        y = county_vaccination["County"], \
                                        orientation = "h",text = county_vaccination["Proportion_vaccinated"], textposition = "outside"))
vac_fig.update_layout(uniformtext_minsize = 3, font_color = "#000000", bargap =0.2,font_size=10,autosize=False, width = 600, height=800)
vac_fig.update_traces( marker_color =  "#1F77B4")
vac_fig.update_xaxes(title = "Proportion Vaccinated", showgrid=True,showline=True, linewidth = 0.1, linecolor = "gray", gridcolor = "gainsboro")


#age gender plots-----------------------------------------------------------------------------------------------------------------------------
age_gender_cases = pd.read_csv("age_gender_cases_data.csv")
age_gender_deaths = pd.read_csv("age_gender_death_cases_data.csv")

def age_gender_plots(data):
        total_female = data["Female"].sum()
        total_male = data["Male"].sum()
        perc_female = total_female/(total_male+total_female)
        perc_male = total_male/(total_male+total_female)
        fig = px.bar(data, x = "age_groups", y = ["Female","Male"], barmode="group")
        fig.update_layout(uniformtext_minsize = 3, font_color = "#4F4F4F", bargap =0.2, paper_bgcolor=pcolor, 
                    plot_bgcolor = pcolor, legend_title = "Gender")
        fig.update_yaxes(title = "No of Cases", showline=True, linewidth = 0.2, linecolor = "gray", gridcolor = "gainsboro")
        fig.update_xaxes(title = "Age categories", showgrid=False)
        return fig, total_female, total_male, perc_female,perc_male

age_gender_cases_plot, total_female_cases, total_male_cases, perc_female_cases,perc_male_cases = age_gender_plots(age_gender_cases)
age_gender_death_plot, total_female_death,total_male_death,perc_female_deaths,perc_male_deaths = age_gender_plots(age_gender_deaths)
#-----------------------------------------------------------------------------------------------------------------------------------------------
# #what contents to link with sidebar
classname = "p-3 ps-4 pb-0 border rounded-top rounded-bottom bg-light bg-opacity-10" #formatting columns in rows

#still under development for unupdated links
under_development = html.H3("Sorry still under development", className = "text-xxl-center align-middle text-danger")

#image cards to set the side bar for selecting multiple counties from the dataset

image_card = html.Div([
                dbc.Row([
                        dbc.Col([                                
                                html.H6("Filter by county", className = "text-info"),                         
                                dcc.Dropdown(
                                   id = "county_chosen" , 
                                   options = [{"label" : name, "value" : name} for name in county_daily_data["county"].sort_values().unique()],
                                   value = [ "Nairobi"] ,  multi = True, style = {"color":"#000000"}),                                      
                        ],width = 4),
                        dbc.Col([                                     
                                html.H6("Filter by date",className = "text-info" ),
                                dcc.DatePickerRange(
                                     id = "my-date-picker",
                                     calendar_orientation = "horizontal", day_size=30,# placeholder = "Return",with_portal = False,
                                     first_day_of_week = 0,with_portal=False,start_date_placeholder_text="1/3/2020",end_date_placeholder_text = ("4/2/2022"), #(0 = sunday)
                                     reopen_calendar_on_clear = False,is_RTL = False, clearable = True, number_of_months_shown = 2,
                                     min_date_allowed = dt(2020, 3, 1),max_date_allowed  = dt(2022, 2, 4),initial_visible_month = dt(2021,2,1),
                                     start_date = dt(2020, 3, 1),end_date = dt(2022, 2, 4),minimum_nights = 2,persistence = True,
                                     persisted_props = ["start_date"],persistence_type = "session",updatemode = "singledate", show_outside_days = True,                        
                                )     
                        ],width = 6)
                ], justify = "end", className = "mb-1"),
 ])
 
#Graph cards for plotting line graphs for each county
graph_card_2 = html.Div([
        dbc.Row([
                dbc.Col([dcc.Graph(id = "line_chart", figure = {})], width = 11)
        ], className = "ms-5 mt-3", style = {"background-color":pcolor})
])
sidebar_style = {"background-color": "#F8F6F0","position":"fixed","padding":"3rem 2rem"}

sidebar = html.Div([
        html.Div([html.H6("Select to view"),html.Hr(),                           
                dbc.Nav([
                        dbc.NavLink("Country-wide ", href = "/", active = "exact"),
                        dbc.NavLink("County Level", href = "/county_cases", active = "exact"),
                ],vertical = True, pills = True),                                                                                       
        ],style = sidebar_style),
])

#seroprevalence data processing and figures-------------------------------------------------------------------------------------------------------------------
sero_data = pd.read_excel("KWTRP_serosurveillance_data_Dashboard_09Sep2022.xlsx") #read in the data
sero_data["Period"] = sero_data[["Month(s)", "Year"]].astype(str).agg(" ".join, axis=1) #create the period column for processing


population = sero_data["Population"].value_counts().to_frame()
population["%"] = round(population["Population"]/population["Population"].sum() * 100, 2)
population_chart = px.pie(population, values = "%",names=population.index, hole = .4)
population_chart.update_layout(autosize=False,height = 300, width = 300, margin = dict(t=10,l=1,r=10),
                                font = dict(size=9),  legend_orientation = "h",
                                plot_bgcolor = pcolor, paper_bgcolor = pcolor,)

gender = sero_data["Sex"].value_counts().to_frame()
gender["%"] = round(gender["Sex"]/gender["Sex"].sum() * 100, 2 )
gender_chart = px.pie(gender, values = "%", names = gender.index, hole = .4)
gender_chart.update_layout(autosize=False,height = 300, width = 300,legend_orientation = "h", 
                                margin = dict(t=20,l=1,r=10),plot_bgcolor = pcolor, paper_bgcolor = pcolor,
                                )

#population relative to age
Health_workers = sero_data[sero_data["Population"] == "Health workers"][["Population","Age in years"]]
Health_workers = Health_workers.groupby("Age in years").count().reset_index()
Truck_crews = sero_data[sero_data["Population"] == "Trucking crews"][["Population","Age in years"]]
Truck_crews = Truck_crews.groupby("Age in years").count().reset_index()
anc_attendees = sero_data[sero_data["Population"] == "ANC attendees"][["Population","Age in years"]]
anc_attendees = anc_attendees.groupby("Age in years").count().reset_index()
HDSS = sero_data[sero_data["Population"] == "HDSS residents"][["Population","Age in years"]]
HDSS = HDSS.groupby("Age in years").count().reset_index()
HDSS = HDSS.rename(columns={"Population":"Frequency"})
HDSS["Values"] = [3,4,5,6,7,2,1,8]
HDSS = HDSS.sort_values(by="Values")
blood_donors = sero_data[sero_data["Population"] == "Blood donors"][["Population","Age in years"]]
blood_donors = blood_donors.groupby("Age in years").count().reset_index()
blood_donors = blood_donors.rename(columns={"Population":"Frequency"})

age_pop_chart = make_subplots(rows = 2,cols=3, vertical_spacing = 0.2, 
                                subplot_titles = ("Blood donors","HDSS","Health workers","Truck crews","ANC Attendees"))
age_pop_chart.add_trace(go.Bar(x = blood_donors["Age in years"], y = blood_donors["Frequency"],name = "Blood donors"), row=1,col=1)
age_pop_chart.add_trace(go.Bar(x = HDSS["Age in years"], y = HDSS["Frequency"], name = "HDSS"), row=1,col=2)
age_pop_chart.add_trace(go.Bar(x = Health_workers["Age in years"], y = Health_workers["Population"],name = "Health workers"), row=1,col=3)
age_pop_chart.add_trace(go.Bar(x = Truck_crews["Age in years"], y = Truck_crews["Population"],name = "Truck crews"), row=2,col=1)
age_pop_chart.add_trace(go.Bar(x = anc_attendees["Age in years"], y = anc_attendees["Population"],name = "ANC Attendees"), row=2,col=2)
age_pop_chart.update_yaxes( showline=True, linewidth = 0.2, linecolor = "gray", gridcolor = "gainsboro")
age_pop_chart.update_xaxes( showline=True, linewidth = 0.2,linecolor = "gray")
age_pop_chart.update_traces(width = 0.5)
age_pop_chart.update_layout(height=500, width=500,bargap = 0.005, plot_bgcolor = pcolor, paper_bgcolor = pcolor, 
                                font = dict(size=9),showlegend = False,margin = dict(t=20,l=1,r=10))
age_pop_chart.update_annotations(font = dict(size=10))      

period = sero_data[["Population","Period"]].groupby(["Period","Population"])["Period"].count().to_frame()
period.index.names = ["Periods","Population"]
period = period.reset_index()
period = period.rename(columns = {"Periods" :"Period", "Period":"Frequency"})
period_chart = px.bar(period, x = "Period", y = "Frequency", barmode="group", color = "Population")
period_chart.update_traces(width = 0.5)
period_chart.update_layout(height = 400, width = 500, bargap = 0.005,plot_bgcolor = pcolor,showlegend=True, 
                        paper_bgcolor = pcolor,font = dict(size=9),legend_orientation ="v")
period_chart.update_yaxes( showline=True, linewidth = 0.2, linecolor = "gray", gridcolor = "gainsboro")
period_chart.update_xaxes(showline=True, linewidth = 0.2,linecolor = "gray")

#serology plot
sero_plot = px.box(sero_data, x = "Population", y = "Anti-spike IgG seroprevalence",color="Population", points="all")
sero_plot.update_yaxes( showline=True, linewidth = 0.2, linecolor = "gray", gridcolor = "gainsboro")
sero_plot.update_xaxes(showline=True, linewidth = 0.2,linecolor = "gray")
sero_plot.update_layout(height = 400, width = 600, bargap = 0.005,plot_bgcolor = pcolor,showlegend=True, 
                        paper_bgcolor = pcolor,font = dict(size=10))

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

app.layout = html.Div([
        html.H2("Coronavirus (COVID-19) in Kenya", className="bg-dark h-1 text-start text-light p-1"),

        dbc.Row([               
               dbc.Col([dbc.Alert([ 
               html.H6("Last updated:", className = "alert-heading"),html.H3("May 2022",className = "alert-heading"),html.Hr(className="my-0"),
               ])], width=3),
       
               dbc.Col([dbc.Alert([
                       html.H6("Total Reported Cases"), html.H2(f"{total_cases:,}"), html.Hr(className="my-0")
               ], color = "secondary" )], width = 3),

               dbc.Col([dbc.Alert([
               html.H6("Discharged", className = "text-success"), html.H2(f"{discharged:,}",className = "text-success"), html.Hr(className="my-0 ")], color = "secondary",  ),
               ],width=3),
       
               dbc.Col([ dbc.Alert([
               html.H6("Reported Deaths",className = "text-danger"), 
               html.H2(f"{dead:,}",className = "text-danger"), 
               html.Hr(className="my-0 ")], color = "secondary" )
               ],width=3),
        ], justify="around", className = "p-5 ps-5 pb-0 bg-secondary bg-opacity-10 g-1"),

        dbc.Tabs([
                dbc.Tab(label = "Cases", children = [
                        html.H6("Cases data is available at country and county levels", className = "text-dark ms-4"),
                        html.Hr(),
                        dcc.Location(id = "cases_url"),
                        sidebar,
                        html.Div(id = "cases-content", children=[], 
                        style ={"margin-left" : "14rem", "margin-right":"2rem"}),
                ],labelClassName = "fw-bold", activeLabelClassName="text-light bg-dark"),

                dbc.Tab(label = "Deaths", children = [
                        html.H6("Only reported death cases data is available at country and county levels", className = "text-dark ms-4"),
                        html.Hr(),
                        dcc.Location(id = "deaths_url"),
                        sidebar,
                        html.Div(id = "deathes-content", children=[], 
                                style ={"margin-left" : "14rem", "margin-right":"2rem"}),

                ],labelClassName = "fw-bold",activeLabelClassName="text-light bg-danger bg-opacity-75"),
                dbc.Tab(label = "Vaccination", children = [
                        html.H4("Vaccination in Kenya", className = "text-dark fw-bold ms-5"),
                                html.P("Vaccination data extracted from Ministry of Health website", className = "text-dark ms-5"),
                                html.P("Last Updated : 29 Aug 2022",className = "text-info ms-5"),
                        dbc.Card([
                                html.H5("Countrywide Summary:", className = "text-info fw-bold ms-2 mt-2"),
                                dbc.Row([
                                        
                                        dbc.Col([
                                                dbc.CardBody([
                                                        html.H5("27,087,910",className = "text-dark fw-bold"),
                                                        html.P("Vaccines Received"),
                                                        html.Hr()
                                                        ])]),
                                        dbc.Col([
                                                dbc.CardBody([
                                                        html.H5("9,404,881",className = "text-dark fw-bold"),
                                                        html.P("Fully vaccinated adults"),
                                                        html.Hr()]),]),
                                        dbc.Col([
                                                dbc.CardBody([
                                                        html.H5("2,281,111",className = "text-dark fw-bold"),
                                                        html.P("Partially vaccinated adults"),
                                                        html.Hr()]),]),
                                        dbc.Col([
                                                dbc.CardBody([
                                                        html.H5("1,911,578",className = "text-dark fw-bold"),
                                                        html.P("Doses administered to teenages"),
                                                        html.Hr()]),]),
                                        dbc.Col([
                                                dbc.CardBody([
                                                        html.H5("516,229",className = "text-dark fw-bold"),
                                                        html.P("Fully vaccinated teenages"),
                                                        html.Hr()]),]),
                                        dbc.Col([
                                                dbc.CardBody([
                                                        html.H5("882,062",className = "text-dark fw-bold"),
                                                        html.P("Partially vaccinated teenages"),
                                                        html.Hr()]),]),
                                        dbc.Col([
                                                dbc.CardBody([
                                                        html.H5("1,118,174",className = "text-dark fw-bold"),
                                                        html.P("Booster Doses"),
                                                        html.Hr()]),]),             
                                ]),
                        ],className = "border-0 ms-4 mb-3 me-3" ,style = cardbody_style),

                        dbc.Card([
                                dbc.CardBody([
                                        html.H5("Proportion of fully vaccinated persons by county", className = "text-dark ms-5"),
                                        dcc.Graph(figure = vac_fig)
                                ]),                        
                        ],className = "border-0 ms-4 me-3",style = cardbody_style)

                ],labelClassName = "fw-bold", activeLabelClassName="text-dark bg-warning"),
                dbc.Tab(label = "Seroprevalence", children = [ 
                        html.Hr(),
                        dcc.Location(id = "seroprevalence_url"),
                        html.Div([html.H6("Select to view"),html.Hr(),                           
                                dbc.Nav([
                                        dbc.NavLink("Overview", href = "/", active = "exact"),
                                        dbc.NavLink("Serology by Population", href = "/sero_population", active = "exact"),
                                ],vertical = True, pills = True),                                                                                       
                        ],style = sidebar_style),

                        html.Div(id = "sero-content", children=[], 
                                style ={"margin-left" : "14rem", "margin-right":"2rem"}),

                ],labelClassName = "fw-bold", activeLabelClassName="text-dark bg-info"),
                dbc.Tab(label = "Genomics", children = [

                        dcc.Location(id = "url"),
                        html.Div([
                        dbc.Nav([
                                dbc.NavLink("summary", href = "/", active = "exact"),
                                dbc.NavLink("civet report", href = "/civet_report", active = "exact"),
                                dbc.NavLink("Nexstrain report", href = "/nexstrain_report", active = "exact"), 
                                dbc.NavLink("Other reports", href = "/other_report", active = "exact")
                        ],vertical = True, pills = True),                      
                        ],style = sidebar_style),

                        html.Div(id = "page-content", children=[], style ={"margin-left" : "14rem", "margin-right":"2rem"})  

                                        
                ],className = "bgcolor-dark",labelClassName = "fw-bold", activeLabelClassName="text-dark bg-info"),
                dbc.Tab(label = "Special Reports", children = [
                        under_development
                ],labelClassName = "fw-bold", activeLabelClassName="text-dark bg-info"),     
                image_card,graph_card_2,
        ], class_name = "gap-5 pb-1 ps-1 ms-4 mb-2 sticky-top"),
])

#Content for countrywide cases tab--------------------------------------------------------------------------------------------------------
seq_metadata = pd.read_table("sequence_metadata_region.tsv")
countrywide = html.Div([

        dbc.Card([
                dbc.CardBody([
                        html.H5("COVID-19 Cumulative Cases across Kenya", className = "text-dark fw-bold"),
                        dcc.Graph(figure = cumilative_cases_figure)
                ],className = "mt-3",style = cardbody_style),
                dbc.CardBody([
                        html.H5("COVID-19 Daily Cases across Kenya", className = "text-dark fw-bold"),
                        dcc.Graph( figure = fig2)
                ],className = "mt-3",style = cardbody_style),
                
                dbc.CardBody([
                        html.H5("COVID-19 Monthly Cases across Kenya", className = "text-dark fw-bold"),
                        dcc.Graph(figure = fig1)
                ], className = "mt-3",style = cardbody_style),

                dbc.CardBody([
                        html.H5("COVID-19 Cases across Kenya by county", className = "text-dark fw-bold"),
                        dcc.Graph( figure = fig3)
                ], className = "mt-3",style = cardbody_style), 

                dbc.CardBody([
                        dbc.Row([
                                dbc.Col([html.H5("Cases by Region",className = "text-dark fw-bold"),
                                        dcc.Graph(figure = fig4)],width = 9),
                                #dbc.Col([html.Img(src='data:image/png;base64,{}'.format(county_cases_image.decode()), height = 350)])                                                        
                        ],justify = "around"),
                ], className = "mt-3",style = cardbody_style),

                dbc.CardBody([
                        html.H5("Cases  by Age and Gender", className = "text-dark fw-bold"),
                        html.P("Total number of cases since the beginning of pandemic by age and sex",className = "text-dark"),
                        html.H6(f"Female-{total_female_cases}({perc_female_cases:.2f}%)",  className = "text-end text-primary"),
                        html.H6(f"Male-{total_male_cases}({perc_male_cases:.2f}%)",className = "text-end text-danger"),
                        dcc.Graph(figure = age_gender_cases_plot)
                ], className = "mt-3",style = cardbody_style),
        ],className = "ms-5 border-0")
        ])
countywide = html.Div([ image_card, graph_card_2])

@app.callback(Output("cases-content", "children"),[Input("cases_url", "pathname")])

def render_cases_content(pathname):
        if pathname == "/":
                return countrywide

        elif pathname == "/county_cases":
                return countywide
        else:
                return countrywide
#callback to link county image to graph card 
@app.callback( Output("line_chart", "figure"),[Input("county_chosen", "value"), Input("my-date-picker" , "start_date"),Input("my-date-picker" , "end_date")]
)
def update_graph_card(county, start_date, end_date):
    if len(county) == 0:
        return dash.no_update
    else:
        data = county_daily_data[county_daily_data["county"].isin(county)]
        data = data.sort_index().loc[start_date : end_date]
        data = data[["county","lab_results", "date_of_lab_confirmation"]].groupby(["county","date_of_lab_confirmation"]).count().reset_index()

        fig = px.line(data, x="date_of_lab_confirmation" , y = "lab_results" , color = "county")
        fig.update_yaxes(title = "Reported Cases", showline=True, linewidth = 0.2, linecolor = "gray", gridcolor = "gainsboro")
        fig.update_xaxes(title = "Date Reported", showgrid=False)
        fig.update_traces(mode = 'lines', marker_color = "#7086CE")
        fig.update_layout(paper_bgcolor="#FFF6F9",plot_bgcolor = "#FFF6F9",uniformtext_minsize = 3, font_color = "#4F4F4F", bargap =0.05)     
        return fig

#call back functions for the deaths tab------------------------------------------------------------------------------------------------------
countrywide_deaths = html.Div([
        dbc.Card([
                dbc.CardBody([
                        html.H5("COVID-19 cumulative death cases across Kenya", className = "text-dark fw-bold"),
                        dcc.Graph(figure=cumilative_death_figure)
                                ],className = "mt-3",style = cardbody_style),     
                dbc.CardBody([
                        html.H5("COVID-19 daily death cases across Kenya", className = "text-dark fw-bold"),
                        dcc.Graph(figure = fig5)],className = "mt-3",style = cardbody_style),
                dbc.CardBody([dcc.Graph(figure = fig6)],className = "mt-3",style = cardbody_style),
                dbc.CardBody([dcc.Graph(figure = fig7)],className = "mt-3",style = cardbody_style),                               
                dbc.CardBody([
                        dbc.Row([
                                dbc.Col([html.H5("Fatalities by Region",className = "text-dark fw-bold"),
                                        dcc.Graph(figure = fig8)], width=9),
                                #dbc.Col([html.Img(src='data:image/png;base64,{}'.format(county_death_image.decode()), height = 350)]),
                        ]) ],className = "mt-3",style = cardbody_style),
                dbc.CardBody([
                        html.H5("Fatalities  by Age and Gender", className = "text-dark fw-bold"),
                        html.P("Total number of fatalities since the beginning of pandemic by age and sex",className = "text-dark"),
                        html.H6(f"Female-{total_female_death}({perc_female_deaths:.2f}%)",  className = "text-end text-primary"),
                        html.H6(f"Male-{total_male_death}({perc_male_deaths:.2f}%)",className = "text-end text-danger"),
                        dcc.Graph(figure = age_gender_death_plot)
                ], className = "mt-3",style = cardbody_style)
        ],className = "ms-5 border-0")              
])

@app.callback(Output("deathes-content", "children"),[Input("deaths_url", "pathname")]
)
def render_deaths_content(pathname):
        if pathname == "/":
                return countrywide_deaths
        elif pathname == "/county_cases":
                return under_development
        else:
                return countrywide_deaths

#genomics summary and civet report--------------------------------------------------------------------------------------------------------

civet_report = html.Div([
        html.Iframe(src="assets/civet.html", style = {"height":"1067px","width" : "100%"})
])
seq_daily = pd.read_table("sequence_metadata.tsv") #number of sequences generated on a daily basis

def daily_seq(observation):
        fig = go.Figure(layout=layout)
        fig.add_trace(go.Scatter( x = seq_daily["collection_date"],  y = seq_daily[observation], 
                        fill = "tozeroy",marker = dict(color ="#3D59AB" )))
        fig.update_traces(mode="markers+lines", hovertemplate=None),
        fig.update_layout(font_color = "#4F4F4F", height = 500,hovermode="x unified")
        fig.update_yaxes( showline=True, linewidth = 0.2, linecolor = "gray", gridcolor = "gainsboro")
        fig.update_xaxes(title = "collection date", showgrid=False)
        return fig

daily_sequences_plot = daily_seq("sequences")
cumilative_sequences_plot  = daily_seq("cum_sequences")


#chart figure--------------------------------------------
labels = ["sequenced", "Not sequenced"]
values = [seq_metadata["sequences"].sum(),total_cases - seq_metadata["sequences"].sum()] #proportion of sequenced samples uses number of sequences vs total positive cases
chart_fig = go.Figure(layout = layout)
chart_fig.add_trace(go.Pie(labels = labels, values = values, hole = .4, hoverinfo="label + value + percent"))
chart_fig.update_layout(height = 300, width = 300,margin = dict(t=50,b=1,l=1,r=1), legend_orientation = "h")
#--------------------------------------------------------
#returns data for genomics tab
sample_bar = go.Bar(x = county_prevalence["County"], 
                    y = county_prevalence["cases"],name= "Cases",
                    yaxis = "y1", offsetgroup=1,marker_color = "#FF7F0E",width = 0.3 )

sequenced_bar = go.Bar(x = seq_metadata["County"], 
                        y = seq_metadata["sequences"],
                        name  = "sequenced", yaxis = "y2",
                        offsetgroup=2, marker_color = "#1F77B4", width = 0.3)
data = [sample_bar, sequenced_bar]
layout = go.Layout( barmode = "group",hovermode="closest",
                        xaxis = dict(showline = True, ticks = "outside",tickfont = dict(size = 10)),
                        yaxis=dict(title='total samples collected',showgrid=True,showline=True, linewidth = 0.1, linecolor = "gray", gridcolor = "gainsboro"),
                        yaxis2=dict(title='proportion sequenced', side='right',overlaying='y',showgrid=False,showline=True, linewidth = 0.2, linecolor = "gray", gridcolor = "gainsboro"), 
                        paper_bgcolor=pcolor, plot_bgcolor = pcolor,
                        legend = dict(x=0.3, y=1, traceorder="normal",orientation = "h"))

count_fig= go.Figure(data = data, layout= layout)

genomics_chart = html.Div([
                html.H5("Overview of Genomics data processing and analysis countrywide", className = "text-dark"),
                dbc.Row([
                        dbc.Col([
                                html.P("Overview of samples collected and those that were sequenced", className = "text-dark"),
                                dcc.Graph(figure = chart_fig)
                        ],width = 3, style = cardbody_style),
                        dbc.Col([
                                html.P("Cumulative number of samples sequenced relative to collection date"),
                                dcc.Graph(figure = cumilative_sequences_plot)
                        ],width=4, style = cardbody_style),
                        dbc.Col([
                                html.P("Number of samples sequenced relative to the collection date", className = "text-dark"),
                                dcc.Graph(figure = daily_sequences_plot)
                        ],width=4, style = cardbody_style)                              
                ],justify = "around", className = "ms-2 mt-1"),
                html.P("Summary of samples collected and those sequenced in each county across the country", className = "text-dark"),
                dcc.Graph(figure = count_fig),
                           
])

@app.callback(
        Output("page-content", "children"),
        [Input("url", "pathname")]
)
def render_content(pathname):
        if pathname == "/":
                return genomics_chart

        elif pathname == "/civet_report":
                return civet_report

        elif pathname == "/nexstrain_report":
                return under_development
        elif pathname == "/other_report":
                return under_development
        else:
                return genomics_chart


#age_gender graph------------------------------------------------------------------------------------------------------------------
age_graph = dcc.Graph(figure = age_gender_cases_plot)
 
#Content for seroprevalence data---------------------------------------------------------------------------------------------------------------
overview = html.Div([
                        dbc.Row([
                                dbc.Col([
                                        html.H6("Summarty of the participants"),
                                        dcc.Graph(figure = population_chart),
                                        html.Hr(),
                                        html.H6("Distribution of participants by Gender"),
                                        dcc.Graph(figure=gender_chart)
                                ], width =3,style = cardbody_style,className = "m-2 bg-light border-light"),
                                dbc.Col([                                       
                                        html.H6("Distribution of participants based on Age and Gender"),
                                        dcc.Graph(figure = age_pop_chart)                                        
                                ],width = 4,style = cardbody_style,className = "m-2 bg-light border-light"),

                                dbc.Col([                                        
                                        html.H6("Distribution of participants based on Age and Gender"),
                                        dcc.Graph(figure = period_chart)                                        
                                ],width=4,style = cardbody_style,className = "m-2 bg-light border-light"),

                        ],justify = "around", className = "ms-4"),
])
sero_population = html.Div([
                dbc.Row([                
                        dbc.Col([                                
                                html.H6("Observed Sero-prevalence levels among the studied populations"),
                                dcc.Graph(figure = sero_plot)                                        
                        ],width = 5,style = cardbody_style,className = "m-2 bg-light border-light")
                ],justify = "centre", className = "ms-5 mt-1"),
        ])

@app.callback(Output("sero-content","children"), [Input("seroprevalence_url","pathname")])

def render_sero_content(pathname):
        if pathname == "/sero_population":
                return sero_population
        else:
                return overview
        
if __name__ == "__main__":
    app.run_server(debug = True,host = "0.0.0.0",port = "3042")