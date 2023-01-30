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
from app import app
import datetime as datetime
import warnings
warnings.filterwarnings('ignore')

load_figure_template("flatly")
#cerulean,flatly,journal,litera,pulse,sandstone
#import geopandas as gpd

# Reading the data
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data/").resolve()

pcolor = "#FFFAFA"
plot_color = "rgba(0,0,0,0)"
pcolor_home = "#efedf5"
pcolor_white = "white"
axis_color = "black"
fillcolor = "#6baed6"
markercolor = "#3C565B"
style = {"height":"200px", "width":"300px"}
margin = dict(l=20, r=20, t=20, b=20)
layout = Layout(plot_bgcolor = pcolor,paper_bgcolor=pcolor)
cardbody_style = {"background-color":pcolor}
cardbody_style_home = {"background-color":pcolor_home}
cardbody_style_vac = {"background-color":pcolor_home, "height":"200%"}
color_patterns = ["#e41a1c","#377eb8","#4daf4a","#984ea3","#073763"]
tickfont = 9
titlefont = 12
#Load datasets
daily_updates_moh =  pd.read_excel(DATA_PATH.joinpath("daily_updates_metadata.xlsx"))
county_daily_updates = pd.read_excel(DATA_PATH.joinpath("county_daily_updates.xlsx"), parse_dates=["Date"], index_col='Date')
#kenya_county = gpd.read_file(DATA_PATH.joinpath("kenyan-counties/County.shp"))
data = pd.read_csv(DATA_PATH.joinpath("cases_per_county.csv"))
lati_lot = pd.read_csv(DATA_PATH.joinpath("kenya_data_latitude_longitude.csv"))
#county_prevalence = pd.read_csv(DATA_PATH.joinpath("cases_per_county.csv"))

#vaccinated proportion-----------------------------------------------------------------------------------------------------------------------------------------
county_vaccination = pd.read_csv(DATA_PATH.joinpath("county_vaccination.csv"))
vaccination_updates = pd.read_csv(DATA_PATH.joinpath("vaccination_metadata_october.csv"), index_col="Group")
county_prevalence = pd.read_csv(DATA_PATH.joinpath("cases_per_county.csv"))
lati_lot = pd.read_csv(DATA_PATH.joinpath("kenya_data_latitude_longitude.csv"))
daily_cases = pd.read_csv(DATA_PATH.joinpath("covid_daily_data.csv"))
age_gender_cases = pd.read_csv(DATA_PATH.joinpath("age_gender_cases_data.csv"))
age_gender_deaths = pd.read_csv(DATA_PATH.joinpath("age_gender_death_cases_data.csv"))


#processing the datasets
daily_updates_moh.set_index("Date", inplace=True)
new_cases_last_24hrs = daily_updates_moh["new_cases_last_24_hrs"].iat[-1]
previous_case = daily_updates_moh["new_cases_last_24_hrs"].iat[-2]
case_fold_change = (new_cases_last_24hrs/previous_case) - 1

total_cases_last_7  = daily_updates_moh["new_cases_last_24_hrs"].iloc[-7:].sum()

samplesize_last_24hrs = daily_updates_moh["sample_size_last_24_hrs"].iat[-1]
samplesize_previous = daily_updates_moh["sample_size_last_24_hrs"].iat[-2]

total_samples_last_7 = daily_updates_moh["sample_size_last_24_hrs"].iloc[-7:].sum()
posity_last_24 = round((new_cases_last_24hrs/samplesize_last_24hrs)*100,1)
previous_positivity = round((previous_case/samplesize_previous)*100,1)

posity_last_7 = round((total_cases_last_7/total_samples_last_7)* 100,1)

fatalities_last_24 = daily_updates_moh["recorded_deaths_last_24_hrs"].iat[-1]
fatalities_last_7 = daily_updates_moh["recorded_deaths_last_24_hrs"].iloc[-7:].sum()
fatalities_previous = daily_updates_moh["recorded_deaths_last_24_hrs"].iat[-2]


recoveries_last_24 = daily_updates_moh["recoveries_last_24_hrs"].iat[-1]
recoveries_previous = daily_updates_moh["recoveries_last_24_hrs"].iat[-2]

recoveries_last_7 = daily_updates_moh["recoveries_last_24_hrs"].iloc[-7:].sum()

total_cases = daily_updates_moh["total_confirmed_cases"].iat[-1]
total_tests =  daily_updates_moh["cumulative_tests"].iat[-1]
total_deaths = daily_updates_moh["cumulative_fatalities"].iat[-1]
total_recoveries = daily_updates_moh["total_recoveries"].iat[-1]
proportion_fully_vaccntd_adults = daily_updates_moh["proportion_of_fully_vaccinated_adult_population"].iat[-1]

overall_positivity = round(total_cases/total_tests*100,1)
update_date = datetime.date.today().strftime("%B %d, %Y")


##Plots
last_7 = daily_updates_moh[["new_cases_last_24_hrs","positivity_rate_last_24_hrs"]].iloc[-7:].reset_index()
fig_7days = px.line(last_7,x = "Date",y ="new_cases_last_24_hrs", hover_data={"Date":"|%B %d"})
fig_7days.update_layout(width=450,height=350, hovermode = "x unified",plot_bgcolor = pcolor,paper_bgcolor = pcolor)
fig_7days.update_yaxes(title = "cases",linecolor = "black")
fig_7days.update_xaxes(linecolor = "black",ticks="outside",nticks = 7)
fig_7days.update_traces(line_color = markercolor)

fig_7_positivity = px.line(last_7,x = "Date",y ="positivity_rate_last_24_hrs", hover_data={"Date":"|%B %d"})
fig_7_positivity.update_layout(width=450,height=350, hovermode = "x unified",plot_bgcolor = pcolor,paper_bgcolor = pcolor)
fig_7_positivity.update_yaxes(title = "Positivity(%)",linecolor = "black")
fig_7_positivity.update_xaxes(linecolor = "black",ticks="outside",nticks = 7)
fig_7_positivity.update_traces(line_color = markercolor)

#county plot for daily updates
filtered_data = county_daily_updates.iloc[[-1]].fillna(0)
filtered_data =  filtered_data.astype(int)
filtered_data = filtered_data.loc[:,(filtered_data != 0).any(axis=0)].T
filtered_data = filtered_data.rename(columns = {filtered_data.columns[0]:"Cases"})
filtered_data.sort_values("Cases", ascending=True, inplace=True)

fig_county = px.bar(filtered_data, x = "Cases", text_auto=True)#, color_discrete_sequence=[markercolor])
fig_county.update_traces(textposition = "outside", textfont_size=10,cliponaxis=True, width=0.6)
fig_county.update_layout(margin = margin,font_size=10,uniformtext_minsize = 3, yaxis_title = None)
                         #plot_bgcolor = pcolor_home,, paper_bgcolor = pcolor_home)
fig_county.update_xaxes(title = None,linecolor = "black",tickfont = dict(size=10),title_font = {"size":10})
fig_county.update_yaxes(tickfont = dict(size=10),title_font = {"size":10})

#most affected counties plot
affected_counties = px.bar(data.head(n=8).sort_values("cases",ascending=True),x = "cases",y="County",text_auto=True,orientation = "h")
affected_counties.update_yaxes(title = None,tickfont = dict(size=tickfont))
affected_counties.update_xaxes(nticks=8,title = None,linecolor = "black",tickfont = dict(size=tickfont))
affected_counties.update_layout(margin=margin)

county_daily_updates.fillna(0, inplace = True)
county_total_cases =  pd.DataFrame(county_daily_updates.sum(axis=0).reset_index()).rename(columns = {"index":"county",0:"Freq"})
county_plot = px.bar(county_total_cases.sort_values("Freq", ascending=True).tail(n=8), y = "county", 
                     x = "Freq",#orientation = "h",
                     color_discrete_sequence=[markercolor], text_auto=True,)

county_plot.update_traces(textposition = "outside", textfont_size=7,cliponaxis=True,width=0.6)
county_plot.update_layout(plot_bgcolor = pcolor_home,paper_bgcolor = pcolor_home,xaxis_title = None,
                          margin = margin)
county_plot.update_yaxes(title = None, linecolor = "black",title_font = {"size":titlefont},
                         tickfont = dict(size=tickfont))
county_plot.update_xaxes(linecolor = "black",tickfont = dict(size=tickfont),title = "Frequency",
                         title_font = {"size":tickfont})


#trends in kenya plot cases
def daily_plots(observation1, observation2):
        fig = go.Figure()
        fig.add_trace(go.Scatter( x = daily_cases["Date"],mode='none', y = daily_cases[observation1]))
        fig.add_trace(go.Scatter(x = daily_cases["Date"], y = daily_cases[observation2]))
        fig.update_layout(hovermode="x unified",showlegend=False,margin = margin)
        fig.update_xaxes(showgrid=False,showline=True,linecolor = axis_color,tickfont = dict(size=tickfont))
        fig.update_yaxes(tickfont = dict(size=tickfont))
        return fig

cases_trend = daily_plots("Reported_Cases","moving_average_cases") #plot of daily reported infections
deaths_trends = daily_plots("death_cases","moving_average_deaths")

#age gender plots
def age_gender_plots(data):
        total_female = data["Female"].sum()
        total_male = data["Male"].sum()
        perc_female = total_female/(total_male+total_female)
        perc_male = total_male/(total_male+total_female)
        fig = px.bar(data, x = "age_groups", y = ["Female","Male"], barmode="group")#, color_discrete_sequence = ["#998ec3","#f1a340"])
        fig.update_layout(uniformtext_minsize = 3, bargap =0.2, 
                     legend_title = None,margin = margin,
                    legend = dict(orientation = "h",yanchor = "top",y = 1,xanchor = "right",x = 1))
        fig.update_yaxes(title = None,showline=True, linewidth = 0.2, linecolor = "gray",
                         tickfont = dict(size=tickfont))
        fig.update_xaxes(title = None,showgrid=False,tickfont = dict(size=tickfont))
        return fig, total_female, total_male, perc_female,perc_male

age_gender_cases_plot, total_female_cases, total_male_cases, perc_female_cases,perc_male_cases = age_gender_plots(age_gender_cases)
age_gender_death_plot, total_female_death,total_male_death,perc_female_deaths,perc_male_deaths = age_gender_plots(age_gender_deaths)

#function to caculate fold change
class fold_change:
    def __init__(self):
        #classname components
        self.up_fold = "fs-6 text-danger bg-danger bg-opacity-10"
        self.down_fold = "fs-6 text-success bg-success bg-opacity-10"
        self.no_change_fold = "fs-6 text-dark bg-dark bg-opacity-10"
        #arrow to be returned
        self.up_arrow = DashIconify(icon="material-symbols:arrow-circle-up-rounded",width=20,color="red",height=25)#
        self.down_arrow = DashIconify(icon="material-symbols:arrow-circle-down-rounded",width=25,color="green",height=25)
        
        self.no_change = DashIconify(id="no_change",icon="ic:baseline-indeterminate-check-box",width=25,color="black",height=25)
        
        self.rec_up_arrow = DashIconify(icon="material-symbols:arrow-circle-up-rounded",width=25,color="green",height=25)#
        self.rec_down_arrow = DashIconify(icon="material-symbols:arrow-circle-down-rounded",width=25,color="red",height=25)#
        
    
    def case_fold_change(self):
        case_fold_value = round((new_cases_last_24hrs/previous_case)-1,1)
        if case_fold_value > 0:
            return case_fold_value,self.up_arrow,self.up_fold
        elif case_fold_value == 0:
            return case_fold_value,self.no_change,self.no_change_fold
        else:
            return case_fold_value,self.down_arrow, self.down_fold
        
    def pos_change(self):
        pos_change = round((posity_last_24/previous_positivity)-1,1)
        if pos_change >0:
            return pos_change,self.up_arrow,self.up_fold
        elif pos_change == 0:
            return pos_change,self.no_change,self.no_change_fold
        else:
            return pos_change,self.down_arrow, self.down_fold
    def recoveries_change(self):
        rec_change = round((recoveries_last_24/recoveries_previous)-1,1)
        if rec_change >0:
            return rec_change,self.rec_up_arrow,self.down_fold
        elif rec_change == 0:
            return rec_change,self.no_change,self.no_change_fold
        else:
            return rec_change,self.rec_down_arrow, self.up_fold
        
    def fatality_change(self):
        fat_change = round((fatalities_last_24/fatalities_previous)-1,1)
        if fat_change > 0:
            return fat_change,self.up_arrow,self.up_fold
        elif fat_change == 0:
            return fat_change,self.no_change,self.no_change_fold
        else:
            return fat_change,self.down_arrow,self.down_fold
        

cases_fold_value,arrow_type,fold_change_class = fold_change().case_fold_change()
pos_fold_value,pos_arrow_type,pos_fold_change_class =fold_change().pos_change()
rec_fold_value,rec_arrow_type,rec_fold_change_class = fold_change().recoveries_change()
fat_fold_value,fat_arrow_type,fat_fold_change_class  =fold_change().fatality_change()

card_class = "text-center"
classname_col = "bg-light bg-opacity-20 g-1 justify-content-center p-2 m-2" 
class_style = "shadow-sm bg-light border rounded g-1"
card_style = "bg-light border rounded-3 shadow"
col_title = "text-center text-black fw-normal"
col_style  = {"margin-left":"15px","margin-right":"0px"}
style_label={"font-size":35, "align":"center"}
style_text ={"font-size":15,"text-align":"center"}
classname_shadow = "shadow border rounded-2 justify-content-center"
hr_style = {"height":"5vh", "align":"center"}
hr_class = "bg-secondary bg-opacity-10 justify-content-center"
col_class = "bg-white align-self-center"

layout = html.Div([
        dbc.Row([
                    dbc.Col([
                        html.P(f"""Last updated: {update_date}""", className = "text-end fs-6 text-primary"),
                        html.P("This dashboard allows a visualization of COVID-19 disease trends in cases, fatalities, vaccination and variant diversity. \
                        This platform intergrates data from Ministry of Health of Republic of Kenya, GISAID and other SARS-CoV-2 associated studies.",
                        className = "fs-6",style ={"text-align":"start"}),
                        html.Hr(),
                    ], width = 11, lg=10),
                ],justify="center", className = "mb-2 ms-3 me-3 ps-3 pe-3 mt-5 pt-5"),
        dbc.Spinner([
                
                dbc.Row([
                    dbc.Col([
                        dbc.CardBody([
                            html.Label(f"{total_cases:,}",className ="text-danger fs-3"),
                            html.P("Total reported cases",style = style_text)
                        ],className = card_class )
                    ],width = 2,lg=2,className = card_style,style = {"margin-right":"10px"}),
                    
                    dbc.Col([
                        dbc.CardBody([
                            html.Label(f"{total_deaths:,}",className ="text-dark fs-3"),
                            html.P("Total reported deaths",style = style_text),
                       ],className = card_class)
                    ],width = 2,lg=2,className = card_style,style = {"margin-right":"10px"}),
                    
                    dbc.Col([
                        dbc.CardBody([
                            html.Label(f"{total_recoveries:,}",className = "text-success fs-3"),
                            html.P("Total recoveries",style = style_text),
                       ],className = card_class)
                    ],width = 2,lg=2,className = card_style,style = {"margin-right":"10px"}),
                    
                    dbc.Col([
                        dbc.CardBody([
                            html.Label(f"{total_tests:,}",className = "text-primary fs-3"),
                            html.P("Tests done",style = style_text),
                       ],className = card_class)
                    ],width = 2,lg=2,className = card_style),
                    
                    dbc.Col([
                        dbc.CardBody([
                            html.Strong(f"{overall_positivity}",className = "text-info fs-3"),html.Span(children="%",className = "text-info fs-4"), 
                            html.P("Overall Positivity",style = style_text),
                        ],className = card_class)
                    ],width = 2,lg=2,className = card_style,style = {"margin-left":"10px"})
                    
                ],justify="center",className = classname_col,align = "center"),
                
                dbc.Row([
                    dbc.Col([
                        html.P("Updates: Last 24hrs",className = "text-black fs-4 fw-normal ms-2"),
                        dbc.Card([
                            dbc.CardBody([
                                html.H6("Cases"),html.Hr(style = {"width":"50%"}),
                                html.Strong(new_cases_last_24hrs,className = "fs-5 fw-normal"),
                                html.Span(children = [arrow_type,cases_fold_value],className = fold_change_class,style = {"margin-left":"20px"}),                              
                            ]),
                        ],className = "border-0"),
                        html.Hr(),#html.Br(),
                        dbc.Card([
                            dbc.CardBody([
                                html.H6("Positivity"),html.Hr(style = {"width":"50%"}),
                                html.Strong(f"{posity_last_24}%",className = "fs-4 fw-normal"),
                                html.Span(children = [pos_arrow_type,pos_fold_value],
                                          className = pos_fold_change_class,style = {"margin-left":"20px"}),
                            ]),
                        ],className = "border-0"),
                        
                        html.Hr(),#,html.Br(),
                        dbc.Card([
                            dbc.CardBody([
                               html.H6("Fatalities"),html.Hr(style = {"width":"50%"}),
                               html.Strong(fatalities_last_24 ,className = "fs-4 fw-normal"),
                               html.Span(children = [fat_arrow_type, fat_fold_value],className = fat_fold_change_class,style = {"margin-left":"20px"})
                            ]),
                        ],className = "border-0"),
                        html.Hr(),#html.Br(),
                        dbc.Card([
                            dbc.CardBody([
                                html.H6("Recoveries"),html.Hr(style = {"width":"50%"}),
                                html.Strong(recoveries_last_24,className = "fs-4 fw-normal"),
                                html.Span(children = [rec_arrow_type, rec_fold_value],className = rec_fold_change_class,style = {"margin-left":"20px"})
                            ]),
                        ],className = "border-0"),
                        html.Hr(),#html.Br(),
                        
                        dbc.Card([
                            dbc.CardBody([
                                html.H6("Samples Tested"),html.Hr(style = {"width":"50%"}),
                                html.Strong(samplesize_last_24hrs,className = "fs-4 fw-normal"),
                            ]),
                        ],className = "border-0"),
                        
                    ],width=2,lg = 2,className = "bg-white"),
                    
                    dbc.Col([
                                               
                       html.P("Counties with reported cases in the last 24 hrs",className = col_title),
                       dcc.Graph(figure = fig_county,responsive = True, style = {"width":"30vw","height":"30vh"}),
                       html.Hr(className = hr_class,style = hr_style),
                               
                       html.P("Trends in Cases since beginnig of pandemic",className = col_title),
                       dcc.Graph(figure=cases_trend,responsive = True, style = {"width":"30vw","height":"30vh"}),
                      
                       html.Hr(className = hr_class,style = hr_style),
                       
                       html.P("Cases by Gender and age",className = col_title),
                       dcc.Graph(figure = age_gender_cases_plot,responsive = True, style = {"width":"30vw","height":"30vh"})
                       
                    ],width=4,lg=4,className = col_class,style = {"margin-left":"15px","margin-right":"0px"} ),
                    
                    dbc.Col([
                        html.P("Most affected counties",className = col_title),
                        dcc.Graph(figure = affected_counties, responsive = True, style = {"width":"30vw","height":"30vh"}),
                        html.Hr(className = hr_class,style = hr_style),
                    #    html.Div([
                    #             #dbc.Button("7-days",id = "7_days",outline=True,color="primary",size="sm",className = "me-1 fs-6"),
                    #             #dbc.Button("COVID-19 Positivity for last 30-days",id = "positivity_30_days",outline=True,color="primary",size="sm"),
                    #         ],className = "d-sm-flex justify-content-sm-center"),
                        html.P("Trends in fatalities since beginnig of pandemic",className = col_title),
                        dcc.Graph(figure = deaths_trends,responsive = True, style = {"width":"30vw","height":"30vh"}),
                        
                        html.Hr(className = hr_class,style = hr_style),
                        html.P("Fatalities by Gender and age",className = col_title),
                        dcc.Graph(figure= age_gender_death_plot, responsive = True, style = {"width":"30vw","height":"30vh"})
                    ],width = 4,lg=4,className = col_class,style = {"margin-left":"15px","margin-right":"0px"}),
                    
                ],className = classname_col,style = {"horizontal-align":"top"},justify = "center"),
         
    ])
])
