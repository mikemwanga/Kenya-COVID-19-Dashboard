import dash
from dash import dcc, html,dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.graph_objects import Layout
import pathlib
import datetime as datetime
from app import app
import warnings
warnings.filterwarnings('ignore')
import geopandas as gpd

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
color_patterns = ["#FF5733","#8E44AD","#2236A0","#252525","#1B6311"]

#Load datasets
daily_updates_moh =  pd.read_excel(DATA_PATH.joinpath("daily_updates_metadata.xlsx"))
county_daily_updates = pd.read_excel("../COVID-19-Dashboard2/data/county_daily_updates.xlsx", parse_dates=["Date"], index_col='Date')
kenya_county = gpd.read_file(DATA_PATH.joinpath("kenyan-counties/County.shp"))
data = pd.read_csv(DATA_PATH.joinpath("cases_per_county.csv"))
lati_lot = pd.read_csv(DATA_PATH.joinpath("kenya_data_latitude_longitude.csv"))

#vaccinated proportion-----------------------------------------------------------------------------------------------------------------------------------------
county_vaccination = pd.read_csv(DATA_PATH.joinpath("county_vaccination.csv"))
vaccination_updates = pd.read_csv(DATA_PATH.joinpath("vaccination_metadata_october.csv"), index_col="Group")
county_prevalence = pd.read_csv(DATA_PATH.joinpath("cases_per_county.csv"))
lati_lot = pd.read_csv(DATA_PATH.joinpath("kenya_data_latitude_longitude.csv"))

#processing the datasets
daily_updates_moh.set_index("Date", inplace=True)
new_cases_last_24hrs = daily_updates_moh["new_cases_last_24_hrs"].iat[-1]
total_cases_last_7  = daily_updates_moh["new_cases_last_24_hrs"].iloc[-7:].sum()

samplesize_last_24hrs = daily_updates_moh["sample_size_last_24_hrs"].iat[-1]
total_samples_last_7 = daily_updates_moh["sample_size_last_24_hrs"].iloc[-7:].sum()
posity_last_24 = round((new_cases_last_24hrs/samplesize_last_24hrs)*100,1)
posity_last_7 = round((total_cases_last_7/total_samples_last_7)* 100,1)

fatalities_last_24 = daily_updates_moh["recorded_deaths_last_24_hrs"].iat[-1]
fatalities_last_7 = daily_updates_moh["recorded_deaths_last_24_hrs"].iloc[-7:].sum()

recoveries_last_24 = daily_updates_moh["recoveries_last_24_hrs"].iat[-1]
recoveries_last_7 = daily_updates_moh["recoveries_last_24_hrs"].iloc[-7:].sum()

total_cases = daily_updates_moh["total_confirmed_cases"].iat[-1]
total_tests =  daily_updates_moh["cumulative_tests"].iat[-1]
total_deaths = daily_updates_moh["cumulative_fatalities"].iat[-1]
total_recoveries = daily_updates_moh["total_recoveries"].iat[-1]
proportion_fully_vaccntd_adults = daily_updates_moh["proportion_of_fully_vaccinated_adult_population"].iat[-1]

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


overall_positivity = round(total_cases/total_tests*100,1)

global_percent = round(total_cases/630550058*100,2)

update_date = datetime.date.today().strftime("%B %d, %Y")

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

fig_county = px.bar(filtered_data, x = "Cases", text_auto=True, color_discrete_sequence=[markercolor])
fig_county.update_traces(textposition = "outside", textfont_size=10,cliponaxis=True, width=0.6)
fig_county.update_layout(font_size=10,uniformtext_minsize = 3, yaxis_title = None,
                         plot_bgcolor = pcolor_home,margin = margin, paper_bgcolor = pcolor_home)
fig_county.update_xaxes(title = "Frequency",linecolor = "black",tickfont = dict(size=10),title_font = {"size":10})
fig_county.update_yaxes(linecolor = "black",tickfont = dict(size=10),title_font = {"size":10})

county_daily_updates.fillna(0, inplace = True)
county_total_cases =  pd.DataFrame(county_daily_updates.sum(axis=0).reset_index()).rename(columns = {"index":"county",0:"Freq"})
county_plot = px.bar(county_total_cases.sort_values("Freq", ascending=True).tail(n=8), y = "county", x = "Freq",#orientation = "h",
                     color_discrete_sequence=[markercolor], text_auto=True,)

county_plot.update_traces(textposition = "outside", textfont_size=7,cliponaxis=True,width=0.6)
county_plot.update_layout(plot_bgcolor = pcolor_home,paper_bgcolor = pcolor_home,xaxis_title = None,margin = margin)
county_plot.update_yaxes(title = None, linecolor = "black",title_font = {"size":10},tickfont = dict(size=10))
county_plot.update_xaxes(linecolor = "black",tickfont = dict(size=8),title = "Frequency",title_font = {"size":10})

style_label={"font-size":35, "text-align":"center"}
style_text ={"font-size":14,"text-align":"start"}
classname_shadow = "shadow border rounded-2 align-center"
#Layout of home page
layout = html.Div([
                
                dbc.Row([
                    dbc.Col([
                        html.P(f"""Last updated: {update_date}""", className = "text-md-end text-primary"),
                        html.H6("This dashboard allows a visualization of COVID-19 disease trends in cases, fatalities, vaccination and variant diversity. \
                        This platform intergrates data from Ministry of Health of Republic of Kenya, GISAID and other SARS-CoV-2 associated studies.",
                        style ={"font-size":16,"text-align":"start"}),
                    ], width = 11, xxl=10),
                    
                    html.Hr(),
                    html.H5("Countrywide Summary"),
                ],justify="center", className = "mb-2 ms-4 me-4 ps-4 pe-4 mt-5 pt-5"),
                dbc.Row([
                    
                   dbc.Col([
                       dbc.CardBody([
                            html.Label(f"{total_cases:,}", style = style_label, className = "text-danger"),
                            html.P("Total reported cases",style = style_text,className = "text-danger"),
                       ],className= "ms-4",style = {"display":"inline-block"})
                   ],width = 2, xxl=3) ,
                   
                   dbc.Col([
                       dbc.CardBody([
                            html.Label(f"{total_deaths:,}",style = style_label),
                            html.P("Total reported deaths",style = style_text),
                       ])
                   ],width=2,xxl=3) ,
                   dbc.Col([
                       dbc.CardBody([
                            html.Label(f"{total_recoveries:,}",style = style_label,className = "text-success"),
                            html.P("Total recoveries",style = style_text,className = "text-success"),
                       ])
                   ],width=2,xxl=3),
                   dbc.Col([
                       dbc.CardBody([
                            html.Label(f"{total_tests:,}",style = style_label,className = "text-primary"),
                            html.P("Tests done",style = style_text,className = "text-primary"),
                       ])
                   ],width=2,xxl=3),
        
                ], justify = "center", className = "g-1 ms-5"),
                
                dbc.Row([
                    html.Br(),
                    html.H6("Reported trends in the last 24 hours and 7 days", className = "fw-bold text-dark ms-4 ps-4"),
                	dbc.Col([
                        dbc.CardBody([
                            html.H5("Cases"),html.Hr(style = {"width":"50%"}),
                            html.A("Last 24hrs"),html.H4(new_cases_last_24hrs),
                            html.A("Last 7 days"),html.H4(total_cases_last_7),
                        ],style = cardbody_style_home, className = classname_shadow),
                                                
                	],width=2,xxl=2, style={"height": "100%"}),
                 
                    dbc.Col([
                    	dbc.CardBody([
                            html.H5("Samples Tested"),html.Hr(style = {"width":"50%"}),
                            html.A("Last 24hrs"),html.H4(samplesize_last_24hrs),
                            html.A("Last 7 days"),html.H4(total_samples_last_7),
                        ],style = cardbody_style_home,className = classname_shadow),
                    ],width=2,xxl=2, style={"height": "100%"}),
                    
                    dbc.Col([
                        dbc.CardBody([
                            html.H5("Positivity"),html.Hr(style = {"width":"50%"}),
                            html.A("Last 24hrs"),html.H4(f"{posity_last_24}%"),
                            html.A("Last 7 days"),html.H4(f"{posity_last_7}%"),
                            #html.A("Overall positivity"),html.H4(f"{overall_positivity}%")
                        ],style = cardbody_style_home,className = classname_shadow),
                        
                    ],width=2,xxl=2, style={"height": "100%"}),
                    
                    dbc.Col([
                        dbc.CardBody([
                            html.H5("Reported Deaths"),html.Hr(style = {"width":"50%"}),
                            html.A("Last 24hrs"),html.H4(fatalities_last_24 ),
                            html.A("Last 7 days"),html.H4(fatalities_last_7),
                            #html.A("Total"),html.H4(f"{total_deaths:,}")
                            ],style = cardbody_style_home,className = classname_shadow),
                    ],width=2,xxl=2, style={"height": "100%"}),
                    
                    dbc.Col([
                        dbc.CardBody([
                            html.H5("Recoveries"),html.Hr(style = {"width":"50%"}),
                            html.A("Last 24hrs"),html.H4(recoveries_last_24),
                            html.A("Last 7 days"),html.H4(recoveries_last_7),
                            #html.A("Total"),html.H4(f"{total_recoveries:,}")
                            ],style = cardbody_style_home,className = classname_shadow),
                    ],width=2,xxl=2, style={"height": "100%"}),
                ], justify="evenly",className = "m-3 p3"),#, style={"height": "100vh"},className = "m-2"),
                
                
                dbc.Row([
                    html.Hr(className = "m-3"),
                    dcc.RadioItems(
                        id = "cases_plots",
                        options = [
                            {"label":"Select to view trends for last 7 days", "value":"7-days"},
                            {"label":"Select to view trends for last 30 days", "value":"30-days"}],
                        value = "7-days",
                        labelStyle = {"display":"block"},
                        inputStyle = {"margin-right":"10px","margin-left":"10px","margin-top":"5px"},
                        style = {"display":"flex","align-items":"center", "justify-content":"start", 
                                 "color":"black","font-size":14}
                    ),
                    dbc.Col([
                        html.H6("COVID-19 Cases",className = "text-sm-center mt-4"),
                        html.Div(dcc.Graph("cases_7_days",responsive = True, style = {"width":"350px","height":"250px"}))
                    ],width=3,xxl=3), #style = cardbody_style,className = "border-end"
                    
                    dbc.Col([
                        html.H6("COVID-19 Positivity",className = "text-center mt-4"),
                        html.Div(dcc.Graph("positivity_7_days",responsive = True, style = {"width":"350px","height":"250px"}))
                    ],width=3,xxl=3),
                    
                    dbc.Col([
                        html.H6("COVID-19 Fatalities",className = "text-center mt-4"),
                        html.Div(dcc.Graph("fatalities_7_days",responsive = True, style = {"width":"350px","height":"250px"}))
                    ],width=3,xxl=3)
                    
                ], justify = "around", className = "ms-2 me-2"),
                
                dbc.Row([
                    html.Hr(className = "m-3"),
                    dbc.Col([
                        html.P("Counties with reported cases in last 24-hours"),
                        dcc.Graph(figure = fig_county, responsive = True, style = {"width":"450px","height":"300px"})
                    ],width=5,xxl = 5,style = cardbody_style_home, className = classname_shadow),#style = cardbody_style_home
                    
                    dbc.Col([
                        html.P("Most affected counties in last 30-days"),
                        dcc.Graph(figure = county_plot, responsive = True, style = {"width":"550px","height":"300px"}),
                        html.Br(),
                    ],width=6,xxl=6,style = cardbody_style_home,className = classname_shadow),#style = cardbody_style_home
                    
                    
                ], justify = "evenly", className = "ms-2 me-2"),
                
    
                html.Br(),html.Hr(),
                dbc.Row([
                    
                    dbc.Col([
                        dbc.Spinner(
                            dbc.CardBody([
                                dcc.RadioItems(
                                    id = "map-buttons",
                                    options = ["Cases","Fatalities"],value = "Cases",
                                    inputStyle = {"margin-right":"2px","margin-left":"20px"}
                                ),
                                html.Div(id = "map-content", children = []),
                            ],style = cardbody_style),
                        )
                    ], width = 7),
                    
                    dbc.Col([
                        dbc.CardBody([
                            html.P("Five most affected counties",className = "fw-bold"),
                            dash_table.DataTable(                                                               
                                columns = [{"name":i,"id":i} for i in county_prevalence[["County","cases"]].head(n=5).columns],
                                data = county_prevalence[["County","cases"]].head(n=5).to_dict("records"),
                                style_cell={'textAlign': 'left','backgroundColor': "#D7DBDD"},
                                style_header={'backgroundColor': "#D7DBDD",'fontWeight': 'bold'},
                                style_data =  {"color":"#980043"}
                            ),
                            html.Br(),
                            html.P("Five least affected counties",className = "fw-bold"),
                            dash_table.DataTable(                                                       
                                columns = [{"name":i,"id":i} for i in county_prevalence[["County","cases"]].tail(n=5).columns],
                                data = county_prevalence[["County","cases"]].tail(n=5).to_dict("records"),
                                style_cell={'textAlign': 'left','backgroundColor': "#D7DBDD"},
                                style_header={'backgroundColor': "#D7DBDD",'fontWeight': 'bold'},
                                style_data =  {"color":"#980043"}
                            )
                        ],style = cardbody_style),
                        
                    ],width=5),#,style={"height": "20vh"}),
                
                ],className = "m-2"),
                
                
                dbc.Row([
                    dbc.Col([
                        dbc.CardBody([
                                html.P("Developed and Maintained by KEMRI-Wellcome Trust Research Program in collaboration with Centre for Viral Research, KEMRI and Ministry of Health"),
                                html.P("Source: Ministry of Health of the Republic of Kenya")
                                ], style = cardbody_style_home, className = "mt-3"),
                    ]),
                   
                ], justify = "around"),
])#ß, style = {"width":"1090px"})

                
kenya_county.loc[(kenya_county["COUNTY"] == "Keiyo-Marakwet"),"COUNTY"] = "Elgeyo Marakwet"
kenya_county.loc[(kenya_county["COUNTY"] == "Tharaka"),"COUNTY"] = "Tharaka Nithi"
kenya_data = pd.merge(kenya_county, data,left_on="COUNTY",right_on = "County",how="inner" )
kenya_data = pd.merge(kenya_data, lati_lot, on ="County")
kenya_data["random"] = [0.7] * len(kenya_data)
kenya_data =  kenya_data.set_index("County")

def map_plot(observation,value):
    fig = px.choropleth(kenya_data, geojson=kenya_data.geometry, locations=kenya_data.index,hover_data = {observation:True, "random":False},
                        color_continuous_scale="cividis",color="random", range_color=(0.4,1),width=700,height=650)
    fig.update_geos(fitbounds = "locations", visible=False,scope="africa")
    fig2 = go.Figure(go.Scattergeo(
            lat = kenya_data.latitude, lon = kenya_data.longitude,text = kenya_data.index,textposition="middle center",
            marker = dict(size=kenya_data[observation]*value,sizemode="area",color = kenya_data.random,line_color="#f0f0f0",line_width=1)
            ))
    fig.add_trace(fig2.data[0])
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},paper_bgcolor = pcolor,plot_bgcolor=pcolor,
                    geo = dict(bgcolor = pcolor,projection_scale=6,center = dict(lat = 0.25,lon=38.09),landcolor ='rgb(217, 217, 217)'),
                    coloraxis_showscale=False, height = 600,width=800)
    return fig
cases_fig = map_plot("cases",0.02)
fatality_fig = map_plot("Death_cases",0.5)

@app.callback(Output("map-content","children"),[Input("map-buttons", "value")])
def render_map_content(value):
        if value == "Cases":
                return [dbc.Spinner(
                        dcc.Graph(figure = cases_fig, responsive=True))]
        if value == "Fatalities":
                return [dbc.Spinner(
                        dcc.Graph(figure = fatality_fig, responsive = True ))
                ]
#cases plots
class cases_plots:
    def __init__(self, days):
        self.last_7 = daily_updates_moh[["new_cases_last_24_hrs","positivity_rate_last_24_hrs", 
                                         "recorded_deaths_last_24_hrs"]].iloc[-days:].reset_index()
        self.filtered_data = filtered_data.sort_values("Cases", ascending=True, inplace=True)
        
    def cases_last_7_days(self):
        fig_7days = px.line(self.last_7,x = "Date",y ="new_cases_last_24_hrs", hover_data={"Date":"|%B %d"})
        fig_7days.update_layout(margin=margin, hovermode = "x unified", plot_bgcolor=pcolor_white,
                                modebar = dict(bgcolor=plot_color))
        fig_7days.update_yaxes(title = None,linecolor = "black",title_font = {"size":10},tickfont = dict(size=8))
        fig_7days.update_xaxes(title=None,linecolor = "black",ticks="outside",title_font = {"size":10},
                               tickfont = dict(size=8))
        fig_7days.update_traces(line_color = markercolor)
        return fig_7days
    
    def positivity_last_7_days(self):
        fig_7_positivity = px.line(self.last_7,x = "Date",y ="positivity_rate_last_24_hrs", hover_data={"Date":"|%B %d"})
        fig_7_positivity.update_layout(margin=margin, hovermode = "x unified",plot_bgcolor=pcolor_white,
                                       modebar = dict(bgcolor=plot_color))
        fig_7_positivity.update_yaxes(title = None,linecolor = "black",tickfont = dict(size=8),
                                      title_font = {"size":10})
        fig_7_positivity.update_xaxes(title=None,linecolor = "black",ticks="outside",tickfont = dict(size=8),title_font = {"size":10})
        fig_7_positivity.update_traces(line_color = markercolor)
        return fig_7_positivity
    
    def fatality_7_days(self):
        fig_7_fatality = px.line(self.last_7,x = "Date",y ="recorded_deaths_last_24_hrs", hover_data={"Date":"|%B %d"}, range_y = [-1,10])
        fig_7_fatality.update_layout(margin=margin, hovermode = "x unified",plot_bgcolor=pcolor_white)
        fig_7_fatality.update_yaxes(title = None,linecolor = "black",tickfont = dict(size=8),title_font = {"size":10})
        fig_7_fatality.update_xaxes(title=None,linecolor = "black",tickfont = dict(size=8),title_font = {"size":10})
        fig_7_fatality.update_traces(line_color = markercolor)
        return fig_7_fatality
        
    def county_plot(self):
        fig_county = px.bar(self.filtered_data, x = "Cases", text_auto=True, color_discrete_sequence=[markercolor])
        fig_county.update_traces(textposition = "outside", textfont_size=10,cliponaxis=True, width=0.6)
        fig_county.update_layout(margin=margin,font_size=10,uniformtext_minsize = 3, yaxis_title = None,
                                 plot_bgcolor = pcolor_white)
        fig_county.update_xaxes(title = "Number of cases",linecolor = "black")
        return fig_county
        


@app.callback(
    [Output("cases_7_days","figure"),
     Output("positivity_7_days","figure")
     ,Output("fatalities_7_days","figure")],
    [Input("cases_plots","value")]
)

def render_cases_plots(value):
    if value == "7-days":
        n = 7
        fig_cases = cases_plots(n).cases_last_7_days()
        fig_pos = cases_plots(n).positivity_last_7_days()
        fig_deaths = cases_plots(n).fatality_7_days()
        return fig_cases, fig_pos, fig_deaths
    
    elif value == "30-days":
        n = 30
        fig_cases = cases_plots(n).cases_last_7_days()
        fig_pos = cases_plots(n).positivity_last_7_days()
        fig_deaths = cases_plots(n).fatality_7_days()
        
        return fig_cases, fig_pos, fig_deaths
        