import dash
from dash import dcc, html,dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.graph_objects import Layout
from dash.exceptions import PreventUpdate
import pathlib
from datetime import datetime as datetime
from app import app
import warnings
warnings.filterwarnings('ignore')
import geopandas as gpd

load_figure_template("flatly")


# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], # LUX, FLATLY LUMEN SPACELAB YETI
#                 suppress_callback_exceptions=True,
#                 meta_tags=[{"name":"viewport","content":"width=device-width,initial-scale=1.0"}])

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
tickfont = 10
titlefont = 12

#load dataset
# Reading the data
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data/").resolve()
kenya_county = gpd.read_file(DATA_PATH.joinpath("kenyan-counties/County.shp"))
data = pd.read_csv(DATA_PATH.joinpath("cases_per_county.csv"))
lati_lot = pd.read_csv(DATA_PATH.joinpath("kenya_data_latitude_longitude.csv"))

county_daily_data = pd.read_csv(DATA_PATH.joinpath("county_daily_data.csv"),dtype='unicode', low_memory=False)
county_daily_data["date_of_lab_confirmation"] = pd.to_datetime(county_daily_data["date_of_lab_confirmation"])
county_daily_data["Date"] = county_daily_data["date_of_lab_confirmation"]#.dt.date
county_daily_data.set_index("Date", inplace = True)

classname_col = "bg-secondary bg-opacity-10 p-2 m-2"
class_style = "shadow-sm bg-light border rounded g-1"
col_style  = {"margin-left":"15px","margin-right":"0px"}
card_style = "bg-light border rounded-3 shadow"
style_text ={"font-size":14,"text-align":"centre"}
card_class = "text-center mt-3"
col_title = "text-center text-black fw-bolder"
hr_style = {"height":"5vh", "align":"center"}
hr_class = "bg-secondary bg-opacity-10 justify-content-center"
col_class = "bg-white align-self-center"

kenya_county.loc[(kenya_county["COUNTY"] == "Keiyo-Marakwet"),"COUNTY"] = "Elgeyo Marakwet"
kenya_county.loc[(kenya_county["COUNTY"] == "Tharaka"),"COUNTY"] = "Tharaka Nithi"
kenya_data = pd.merge(kenya_county, data,left_on="COUNTY",right_on = "County",how="inner" )
kenya_data = pd.merge(kenya_data, lati_lot, on ="County")
kenya_data["random"] = [0.7] * len(kenya_data)
kenya_data =  kenya_data.set_index("County")


layout = html.Div([
            dbc.Spinner([
                dbc.Row([
                    dbc.Col([
                        html.H5("Visualization of trends at County level", style ={"text-align":"start"}),
                        html.Hr(),
                    ], width = 11, xxl=10),
                ],justify="center", className = "mb-2 ms-4 me-4 ps-4 pe-4 mt-5 pt-5"),
               
                
                dbc.Row([
                    dbc.Row([
                        dbc.Col([
                            html.P('Select county',className ="fs-6 text-primary mb-1 pb-1"),
                            dcc.Dropdown(
                                
                                id = "county_selected",
                                 options = [
                                     {"label" : name, "value" : name} for name in county_daily_data["county"].sort_values().unique()
                                 ],
                                 value = "Nairobi",
                                 multi=False,
                                 clearable=False,
                                 style = {"width":150},
                            ),
                        ],width=2,className="me-2 mb-2")
                    ],justify="end"),
                    
                    dbc.Col([
                        html.Br(),
                        html.P("Trends in cases at the selected county (14-days average)",className = col_title),
                        dcc.Graph(id = "trends_plot", figure = {}, responsive=True,style={"height":"250px"}),
                        html.Hr(),
                        
                        html.Br(),
                        html.P("Cumulative cases at the selected county",className = col_title),
                        dcc.Graph(id = "cumulative_plot", figure = {},responsive=True,style={"height":"250px"}),
                        html.Hr(),
                        
                        html.Br(),
                        html.P("Trends in deaths at the selected county",className = col_title),
                        dcc.Graph(id = "death_plot", figure = {},responsive=True,style={"height":"250px"})
                    ],width=5,lg=5,className = col_class,style = {"height":"1100px"}),
                    
                    dbc.Col([
                        
                        dbc.Row([
                            
                            html.P("Summary of cases, deaths and proportion of infected within the selected county.", 
                                   className="fw-bold fs-6 mt-4 text-center"),
                            dbc.Col([dbc.CardBody([
                                html.H4(id="cases_value",className ="text-danger fs-3"),
                                html.P("Total cases",style = style_text)
                                ],className = card_class ),
                            ]),
                            dbc.Col([
                                dbc.CardBody([
                                html.H4(id="death_value",className ="text-black fs-3"),
                                html.P("Total deaths",style = style_text)
                                ],className = card_class ),
                            ]),
                            dbc.Col([
                                dbc.CardBody([
                                html.H4(id="prevalence",className ="text-info fs-3"),
                                html.P("Proportion infected",style = style_text)
                                ],className = card_class ),
                            ]),
                        
                        ]),
                        html.Hr(),
                        
                        html.Div([
                            dbc.Button("Cases",id="cases_button",n_clicks=0,size="sm",color = "primary",outline=True,style = {"font-size":10}),
                            dbc.Button("Deaths",id="deaths_button",n_clicks=0,size="sm",color = "primary",outline=True,className="me-2",style = {"font-size":10}),
                        ],className = "d-grid gap-1 d-md-flex justify-content-sm-end"),
                        html.Div(id = "map-content", children = []),
                        
                    ],width=5,lg=5,className = col_class,style={"margin-left":"7px", "height":"1100px"})
                    
                ],justify = "center",className = classname_col),
        
            ])
])

def map_plot(observation,value):
    fig = px.choropleth(kenya_data, geojson=kenya_data.geometry, locations=kenya_data.index,hover_data = {observation:True, "random":False},
                        color_continuous_scale="cividis",color="random", range_color=(0.4,1),width=700,height=650)
    fig.update_geos(fitbounds = "locations", visible=False,scope="africa")
    fig2 = go.Figure(go.Scattergeo(
            lat = kenya_data.latitude, lon = kenya_data.longitude,text = kenya_data.index,textposition="middle center",
            marker = dict(size=kenya_data[observation]*value,sizemode="area",color = kenya_data.random,line_color="#f0f0f0",line_width=1)
            ))
    fig.add_trace(fig2.data[0])
    fig.update_layout(#paper_bgcolor = pcolor,plot_bgcolor=pcolor,bgcolor = pcolor
                    geo = dict(projection_scale=6,center = dict(lat = 0.25,lon=38.09),landcolor ='rgb(217, 217, 217)'),
                    coloraxis_showscale=False, height = 600,width=800,margin = margin)
    return fig
cases_fig = map_plot("cases",0.02)
fatality_fig = map_plot("Death_cases",0.5)

@app.callback(Output("map-content","children"),
              [Input("cases_button", "n_clicks"),
                Input("deaths_button","n_clicks")])

def render_map_content(click1,click2):
        size = {"width":"37vw","height":"70vh"}
        cases = html.Div([
                    html.P("County distribution of COVID-19 cases",className="fs-6 text-center fw-bold"),
                    dcc.Graph(figure = cases_fig,responsive=True, style = size ),
                    ])
        deaths = html.Div([
                    html.P("County distribution of COVID-19 fatalities",className="fs-6 text-center fw-bold"),
                    dcc.Graph(figure = fatality_fig,responsive=True,style = size)
                    ]),
        
        ctx = dash.callback_context #used to determine which button is triggered
        
        button_id = ctx.triggered[0]['prop_id'].split('.')[0] #grab id of button triggered
        if button_id == "cases_button":
            return cases
        elif button_id == "deaths_button":
             return deaths
        else:
             return cases
                
#function for 7-day moving average
def seven_day_average(data,column):
    window_size = 14
    moving_average = []
    data_col = data[column]
    for i in range(len(data)):
        if i + window_size < len(data_col):
            moving_average.append(round(np.mean(data_col[i:i+window_size]),1))
        else:
            moving_average.append(np.mean(data_col[i:len(data_col)])) 
    data["moving_average"] = moving_average
    return data
   
@app.callback( [Output("trends_plot", "figure"),
                Output("cumulative_plot", "figure"),
                Output("death_plot","figure"),
                Output("cases_value","children"),
                Output("death_value","children"),
                Output("prevalence","children")],
                [Input("county_selected", "value"),
                #Input("my-date-picker" , "start_date"),Input("my-date-picker" , "end_date"
                ])

def update_graph_card(county):
    if len(county) == 0:
        return dash.no_update
    else:
        data_filter = county_daily_data[county_daily_data["county"] == county]
        death_data = data_filter[data_filter["outcome"] == "Dead"] 
        #data_filter = data_filter.sort_index().loc[start_date : end_date]
        data_filter= data_filter[["county","lab_results", "date_of_lab_confirmation"]].groupby(["county","date_of_lab_confirmation"]).count().reset_index()
        
        fig2 = px.line(data_filter, x="date_of_lab_confirmation" , y = data_filter["lab_results"].cumsum() , color = "county")
        fig2.update_yaxes(title =None, showline=True, linewidth = 0.1, linecolor = "gray")
        fig2.update_xaxes(title = None,linecolor = "gray", showline=True,showgrid=False)
        fig2.update_layout(hovermode="x unified",uniformtext_minsize = 3, bargap =0.05,margin=margin,
                           legend = dict(orientation = "h"))#,yanchor = "top",y = 1,xanchor = "right",x = 1)) 

        data_average = seven_day_average(data_filter, "lab_results")
        fig = px.line(data_average, x="date_of_lab_confirmation" , y = "moving_average" , color = "county")
        fig.update_yaxes(title = None, showline=True, linewidth = 0.1, linecolor = "black")
        fig.update_xaxes(title = None, showline=True,showgrid=False,linecolor = "black",)
        fig.update_layout(hovermode="x unified",uniformtext_minsize = 3, bargap =0.05,margin=margin,
                          legend = dict(orientation = "h"))#,yanchor = "bottom"))#,y = 0,xanchor = "right",x = 1)) 
        
        #death plot
        death_data = death_data.groupby(["date_of_lab_confirmation"])[["date_of_lab_confirmation"]].count().rename(columns = {"date_of_lab_confirmation":"Freq"}).reset_index()
        death_data = seven_day_average(death_data,"Freq")
        fig_death = px.line(death_data, x = "date_of_lab_confirmation", y = "moving_average")
        fig_death.update_yaxes(title = None, showline=True, linewidth = 0.1, linecolor = "black")
        fig_death.update_xaxes(title = None, showline=True,showgrid=False,linecolor = "black",)
        fig_death.update_layout(hovermode="x unified",uniformtext_minsize = 3, bargap =0.05,margin=margin,
                          legend = dict(orientation = "h"))
        
        cases_value = data[data["County"]== county]["cases"]
        death_value = data[data["County"]== county]["Death_cases"]
        prevalence = round(cases_value/data[data["County"] == county]["Population"]*100,1)
       
        return fig,fig2,fig_death,cases_value,death_value, prevalence #fig, fig2,

#