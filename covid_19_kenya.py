from gc import callbacks
from pickle import TRUE
from pydoc import classname
from statistics import multimode
from turtle import fillcolor, width
from datetime import datetime as dt

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
layout = Layout(plot_bgcolor = "#FFF6F9",paper_bgcolor="#FFF6F9")
daily_cases = pd.read_csv("covid_daily_data.csv")
def daily_plots(observation):
        fig = go.Figure(layout=layout)
        fig.add_trace(go.Scatter( x = daily_cases["Date"],  y = daily_cases[observation], 
                        fill = "tonext",marker = dict(color ="#3D59AB" )))
        fig.update_layout(font_color = "#4F4F4F", height = 500)
        fig.update_yaxes(title =  "National daily cases", showline=True, linewidth = 0.2, linecolor = "gray", gridcolor = "gainsboro")
        fig.update_xaxes(title = "Period", showgrid=False)
        return fig
fig2 = daily_plots("Reported_Cases") #plot of daily reported infections
fig5 = daily_plots("death_cases") #plot of daily death cases

#plot2 monthly cases----------------------------------------------------------------------------------------------------------------------------
Monthly_cases = pd.read_csv("covid_monthly_data.csv")
#plotting for cases and deaths. Recovered there is alot of missing data
def monthly_plot(observation):
        fig = go.Figure(layout=layout)
        fig.add_trace(go.Scatter( x = Monthly_cases["Month_year"],  y = Monthly_cases[observation],
                            fill = 'tonext', marker = dict(color = "#3D59AB")))
        fig.update_layout(title = f"COVID-19 Monthly {observation}", font_color = "#4F4F4F")
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
vac_fig = go.Figure(layout=Layout(paper_bgcolor="#FFF6F9", plot_bgcolor = "#FFF6F9", font_size=10,autosize=False, width = 600, height=800))
vac_fig.add_trace(go.Bar(x = county_vaccination["Proportion_vaccinated"],
                                        y = county_vaccination["County"], \
                                        orientation = "h",text = county_vaccination["Proportion_vaccinated"], textposition = "outside"))
vac_fig.update_layout(uniformtext_minsize = 3, font_color = "#000000", bargap =0.2, paper_bgcolor="#FFF6F9", 
                    plot_bgcolor = "#FFF6F9")
vac_fig.update_traces(marker_color =  "#1F77B4")
vac_fig.update_xaxes(title = "Proportion Vaccinated", showgrid=True,showline=True, linewidth = 0.1, linecolor = "gray", gridcolor = "gainsboro")


#age gender plots-----------------------------------------------------------------------------------------------------------------------------
age_gender = pd.read_csv("age_gender_cases_data.csv")
age_gender_cases_plot= px.bar(age_gender, x = "age_groups", y = ["Female","Male"], barmode="group")
age_gender_cases_plot.update_layout(uniformtext_minsize = 3, font_color = "#4F4F4F", bargap =0.2, paper_bgcolor="#FFF6F9", 
                    plot_bgcolor = "#FFF6F9", legend_title = "Gender")
age_gender_cases_plot.update_yaxes(title = "No of Cases", showline=True, linewidth = 0.2, linecolor = "gray", gridcolor = "gainsboro")
age_gender_cases_plot.update_xaxes(title = "Age categories", showgrid=False)
#-----------------------------------------------------------------------------------------------------------------------------------------------
# #what contents to link with sidebar
classname = "p-3 ps-4 pb-0 border rounded-top rounded-bottom bg-light bg-opacity-10" #formatting columns in rows

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
        ], className = "ms-5 mt-3", style = {"background-color":"#FFF6F9"})
])

sidebar = html.Div([
        html.Div([html.H6("Select to view"),html.Hr(),                           
                dbc.Nav([
                        dbc.NavLink("Country-wide ", href = "/", active = "exact"),
                        dbc.NavLink("County Level", href = "/county_cases", active = "exact"),
                ],vertical = True, pills = True),                                                                                       
        ],style = {"background-color": "#F8F6F0","position":"fixed","padding":"3rem 2rem"}),
])

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
               html.H6("Discharged"), html.H2(f"{discharged:,}"), html.Hr(className="my-0")], color = "secondary",  ),
               ],width=3),
       
               dbc.Col([ dbc.Alert([
               html.H6("Reported Deaths"), html.H2(f"{dead:,}"), html.Hr(className="my-0 ")], color = "secondary" )
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

                                dbc.Row([
                                        dbc.Col([
                                                dbc.CardBody([
                                                        html.H5("Proportion of fully vaccinated persons by county", className = "text-dark ms-5"),
                                                        dcc.Graph(id = "vaccination summary", figure = vac_fig)]),
                                        dbc.Col([

                                        ])
                                ])
                                ]),
                        ],className = "m-5 border rounded-top rounded-bottom",style = {"background-color":"#FFF6F9"})

                ],labelClassName = "fw-bold", activeLabelClassName="text-dark bg-warning"),
                dbc.Tab(label = "Seroprevalence", children = [ 
                ],labelClassName = "fw-bold", activeLabelClassName="text-dark bg-info"),
                dbc.Tab(label = "Genomics", children = [

                        dcc.Location(id = "url"),
                        html.Div([
                        dbc.Nav([
                                dbc.NavLink("summary", href = "/", active = "exact"),
                                dbc.NavLink("civet report", href = "/civet_report", active = "exact"),
                                dbc.NavLink("Nextrain report", href = "/civet_report", active = "exact"), 
                                dbc.NavLink("Other reports", href = "/other_report", active = "exact")
                        ],vertical = True, pills = True),                      
                        
                        ],style = {"background-color": "#F8F6F0", "position":"absolute","width":"12rem"}),
                        html.Div(id = "page-content", children=[], style ={"margin-left" : "8rem", "margin-right":"1rem"})                 
                                                               
                
                
                ],className = "bgcolor-dark",labelClassName = "fw-bold", activeLabelClassName="text-dark bg-info"),
                dbc.Tab(label = "Summary", children = [
                ],labelClassName = "fw-bold", activeLabelClassName="text-dark bg-info"),     
                html.Div([image_card,graph_card_2]), 
        ], class_name = "gap-5 pb-1 ps-1 ms-4 mb-2 sticky-top"),
])
#Content for countrywide cases tab
cardbody_style = {"background-color":"#FFF6F9"}

countrywide = html.Div([

        dbc.Card([
                dbc.CardBody([
                        html.H5("COVID-19 Daily Cases across Kenya", className = "text-dark fw-bold"),
                        dcc.Graph(id = "daily cases", figure = fig2)
                ],className = "mt-3",style = cardbody_style),
                
                dbc.CardBody([
                        html.H5("COVID-19 Monthly Cases across Kenya", className = "text-dark fw-bold"),
                        dcc.Graph(id = "Monthly cases", figure = fig1)
                ], className = "mt-3",style = cardbody_style),

                dbc.CardBody([
                        html.H5("COVID-19 Cases across Kenya by county", className = "text-dark fw-bold"),
                        dcc.Graph(id = "Cases by County", figure = fig3)
                ], className = "mt-3",style = cardbody_style), 

                dbc.CardBody([
                        dbc.Row([
                                dbc.Col([dcc.Graph(id = "Cases by Region", figure = fig4)],width = 8),
                                dbc.Col([html.Img(src='data:image/png;base64,{}'.format(county_cases_image.decode()), height = 350)])                                                        
                        ],justify = "around"),
                ], className = "mt-3",style = cardbody_style),

                dbc.CardBody([
                        html.H5("Cases  by Age and Sex", className = "text-dark fw-bold"),
                        html.P("Total number of cases since the beginning of pandemic by age and sex",className = "text-dark"),
                        dcc.Graph(id = "Cases by Region", figure = age_gender_cases_plot)

                ], className = "mt-3",style = cardbody_style),
                
        ],className = "ms-5 border-0")

        ])

countywide = html.Div([
                image_card,
                graph_card_2])

#Callback to cases try tab--------------------------------------------------------------------------------------------------------
@app.callback(
        Output("cases-content", "children"),
        [Input("cases_url", "pathname")]
)

def render_cases_content(pathname):
        if pathname == "/":
                return countrywide

        elif pathname == "/county_cases":
                return countywide
#callback to link county image to graph card 
@app.callback( 
    Output("line_chart", "figure"),
    [Input("county_chosen", "value"), Input("my-date-picker" , "start_date"),Input("my-date-picker" , "end_date")]
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
                        dcc.Graph(id = "daily Death cases", figure = fig5)
                ],className = "mt-3",style = cardbody_style),
                dbc.CardBody([
                        dcc.Graph(id = "daily Death cases", figure = fig6)
                ],className = "mt-3",style = cardbody_style),
                dbc.CardBody([
                        dcc.Graph(id = "daily Death cases", figure = fig7)
                ],className = "mt-3",style = cardbody_style),                               
                dbc.CardBody([
                        dbc.Row([
                                dbc.Col([dcc.Graph(id = "daily Death cases", figure = fig8)], width=8),
                                dbc.Col([html.Img(src='data:image/png;base64,{}'.format(county_death_image.decode()), height = 350)]),
                        ])                        
                ])
        ],className = "ms-5 border-0")              
])

@app.callback(
        Output("deathes-content", "children"),
        [Input("deaths_url", "pathname")]
)

def render_deaths_content(pathname):
        if pathname == "/":
                return countrywide_deaths
        elif pathname == "/county_cases":
                return html.H4("404 Error:Still under development")
#     Output("line_chart_death", "figure"),
#     [Input("county_chosen", "value"), Input("my-date-picker" , "start_date"),Input("my-date-picker" , "end_date")]
# )
# def update_graph_card(county, start_date, end_date):
#     if len(county) == 0:
#         return dash.no_update
#     else:
#         data = county_daily_data[county_daily_data["outcome"] == "Dead"]
#         data = data[data["county"].isin(county)]
#         data = data.sort_index().loc[start_date : end_date]
#         data = data[["county","lab_results", "date_of_lab_confirmation"]].groupby(["county","date_of_lab_confirmation"]).count().reset_index()

#         fig = px.line(data, x="date_of_lab_confirmation" , y = "lab_results" , color = "county")
#         fig.update_yaxes(title = "Reported Death Cases", showline=True, linewidth = 0.2, linecolor = "gray", gridcolor = "gainsboro")
#         fig.update_xaxes(title = "Date Reported", showgrid=False)
#         fig.update_traces(mode = 'lines', marker_color = "#7086CE")
#         fig.update_layout(paper_bgcolor="#FFF6F9",plot_bgcolor = "#FFF6F9",uniformtext_minsize = 3, font_color = "#4F4F4F", bargap =0.05)     
#         return fig




#genomics summary and civet report--------------------------------------------------------------------------------------------------------
civet_report = html.Div([
        html.Iframe(src="assets/civet.html", style = {"height":"1067px","width" : "100%"})
])




#chart figure-------------------------------------------------------------------------------------------------------------------------------------

labels = ["sequenced", "Not sequenced"]
values = [county_prevalence["sequenced"].sum(),county_prevalence["samples_collected"].sum() - county_prevalence["sequenced"].sum()]
chart_fig = go.Figure(layout = Layout(paper_bgcolor="#FFF6F9", plot_bgcolor = "#FFF6F9",height = 400, width = 500))
chart_fig.add_trace(go.Pie(labels = labels, values = values, hole = .4, hoverinfo="label + value + percent"))
                        #color_discrete_map = {"labels" : "#1F77B4", "values": })

#----------------------------------------------------------------------------------------------------------
#returns data for genomics tab
sample_bar = go.Bar(x = county_prevalence["County"], 
                    y = county_prevalence["samples_collected"],name= "collected",
                    yaxis = "y1", offsetgroup=1,marker_color = "#FF7F0E",width = 0.3 )

sequenced_bar = go.Bar(x = county_prevalence["County"], 
                        y = county_prevalence["Proportion_sequenced"],
                        name  = "sequenced", yaxis = "y2",
                        offsetgroup=2, marker_color = "#1F77B4", width = 0.3)
data = [sample_bar, sequenced_bar]

layout = go.Layout( barmode = "group",hovermode="closest",
                        xaxis = dict(showline = True, ticks = "outside",tickfont = dict(size = 10)),
                        yaxis=dict(title='total samples collected',showgrid=True,showline=True, linewidth = 0.1, linecolor = "gray", gridcolor = "gainsboro"),
                        yaxis2=dict(title='proportion sequenced', side='right',overlaying='y',showgrid=False,showline=True, linewidth = 0.2, linecolor = "gray", gridcolor = "gainsboro"), 
                        paper_bgcolor="#FFF6F9", plot_bgcolor = "#FFF6F9",
                        legend = dict(x=0.3, y=1, traceorder="normal",orientation = "h"))

count_fig= go.Figure(data = data, layout= layout)

genomics_chart = html.Div([
        dbc.Card([
                dbc.Row([
                        dbc.Col([
                                dbc.CardBody([ 
                                        html.P("Overview of samples collected and those that were sequenced", className = "text-dark"),
                                        dcc.Graph(id = "chart", figure = chart_fig)])], width = 4),
                        dbc.Col([
                                dbc.CardBody([                                       
                                        html.P("Geographical representation of samples collected and those sequenced",className = "text-dark"),
                                        dbc.CardImg(
                                                src='data:image/png;base64,{}'.format(county_cases_image.decode())),
                                ]),
                        ], width = 4),
                ],justify = "around"),
                dbc.Row([

                        dbc.Col([
                                dbc.CardBody([
                                        html.P("Summary of samples collected and those sequenced in each county across the country", className = "text-dark"),
                                        dcc.Graph(id = "bar_graph", figure = count_fig)
                                ])                       
                        ]),

                ])
        ],className = "ms-5 border rounded-top rounded-bottom",style = {"background-color":"#FFF6F9"})
        
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

#age_gender graph------------------------------------------------------------------------------------------------------------------
age_graph = dcc.Graph(id = "age_gender casesw", figure = age_gender_cases_plot)
 
# table2 = dash_table.DataTable(
#         columns=[{"name":i, "id":i} for i in age_gender.columns],
#         data = age_gender.to_dict("records"), 
#         style_cell = {"fontSize":20,"align":"centre","padding":"7px"}, 
#         style_as_list_view=True,
#         style_header = {"color":"black", 'fontWeight': 'bold',"fontSize":20},
#         style_data = {"color":"black", "fontweight":"bold", "backgroundColor" :"#FFF6F9" },fixed_rows={'headers': True},
#         page_action = "none", 
#         style_table = {"height" :"300px","width":"800px", "overflow" :"hidden", "textOverflow" :"ellipsis"}
#         )

# @app.callback(
#         Output("age_chart", "children"),
#         Input("url_age_chart", "pathname")
# )
# def render_age_chart(pathname):
#         if pathname == "/":
#                 return age_graph
#         elif pathname == "/data_table":
#                 return table2

#-------------------------------------------------------------------------------------------------------------------------------



if __name__ == "__main__":
    app.run_server(debug = True, port = 3041)