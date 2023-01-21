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

classname_col = "bg-secondary bg-opacity-10 g-1 p-2 m-2"
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
                    
                    
                    #html.H5("Countrywide Summary"),
                ],justify="center", className = "mb-2 ms-4 me-4 ps-4 pe-4 mt-5 pt-5"),
                dbc.Row([
                    # dbc.Col([
                    #     dbc.CardBody([
                    #         html.H6("Filter by county"),
                    #         dcc.Dropdown(
                    #             id = "county_chosen" , 
                    #             options = [{"label" : name, "value" : name} for name in county_daily_data["county"].sort_values().unique()],
                    #             placeholder = "Select County",
                    #             value = "Nairobi"),#,  multi = False, style = {"color":"#000000"}),
                    #         html.Div(id = "selected_county"),
                    #     ])
                    # ],width=4),
                    dbc.Col([
                        dbc.CardBody([
                            #html.H6("Filter by period"), 
                            # dcc.DatePickerRange(
                            #     id = "my-date-picker",
                            #     calendar_orientation = "horizontal", day_size=30,# placeholder = "Return",with_portal = False,
                            #     first_day_of_week = 0,with_portal=False,start_date_placeholder_text="1/3/2020",end_date_placeholder_text = ("4/2/2022"), #(0 = sunday)
                            #     reopen_calendar_on_clear = False,is_RTL = False, clearable = True, number_of_months_shown = 2,
                            #     min_date_allowed = datetime(2020, 3, 1),max_date_allowed  = datetime(2022, 11, 30),initial_visible_month = datetime(2021,2,1),
                            #     start_date = datetime(2020, 3, 1),end_date = datetime(2022, 11, 30),minimum_nights = 2,persistence = True,
                            #     persisted_props = ["start_date"],persistence_type = "session",updatemode = "singledate", show_outside_days = True,                        
                            # )
                        ])
                    ],width = 4)
                ],className = classname_col,justify = "center"),
                dbc.Row([
                    dbc.Col([
                        dbc.CardBody([
                            html.Label("Filter by county",className = "text-primary fs-6"),
                            dcc.Dropdown(
                                id = "county_chosen" , maxHeight=100,
                                options = [{"label" : name, "value" : name} for name in county_daily_data["county"].sort_values().unique()
                                           ],style = {"color":"blue"},
                                
                                placeholder = "Select County",
                                value = "Nairobi"),#,  multi = False, style = {"color":"#000000"}),
                            #html.Br(),
                            html.Label("Filter by date",className = "text-primary fs-6"),
                            dcc.DatePickerRange(
                                id = "my-date-picker",
                                calendar_orientation = "horizontal", day_size=30,# placeholder = "Return",with_portal = False,
                                first_day_of_week = 0,with_portal=False,start_date_placeholder_text="1/3/2020",end_date_placeholder_text = ("4/2/2022"), #(0 = sunday)
                                reopen_calendar_on_clear = False,is_RTL = False, clearable = True, number_of_months_shown = 2,
                                min_date_allowed = datetime(2020, 3, 1),max_date_allowed  = datetime(2022, 11, 30),initial_visible_month = datetime(2021,2,1),
                                start_date = datetime(2020, 3, 1),end_date = datetime(2022, 11, 30),minimum_nights = 2,persistence = True,
                                persisted_props = ["start_date"],persistence_type = "session",updatemode = "singledate", show_outside_days = True,                        
                            )
                        ]),#className = card_class)
                    ],width=3,className = "bg-white border-0",style = {"margin-right":"20px"}),
                    
                    
                    dbc.Col([
                        dbc.CardBody([
                            html.H3(id = "cases_value",className = "text-danger" ),
                            html.P("total COVID-19 cases in the selected county",style = style_text),
                            
                        ],className = card_class)
                    ],width = 2,xxl=2,className = card_style,style = {"margin-right":"20px"}),
                    
                    dbc.Col([
                        dbc.CardBody([
                            html.H3(id = "death_value",className = "text-black"),
                            html.P("total fatalities from COVID-19 in the selected county",style = style_text)
                        ],className = card_class)
                    ],width = 2,xxl=2,className = card_style,style = {"margin-right":"20px"}),
                    dbc.Col([
                        dbc.CardBody([
                            html.Strong(id = "prevalence",className = "text-info fs-3"),html.Span(children="%",className = "text-info fw-bold fs-4"),
                            html.P("Positivity in the selected county",style = style_text)
                        ],className = card_class)
                    ],width = 2,xxl=2,className = card_style),
                    
                    
                    
                ],className = classname_col,justify = "center"),
                      
                dbc.Row([
                    
                    dbc.Col([
                        html.H6("Trends in cases for the selected county",className = col_title),
                        dcc.Graph(id = "line_chart1",figure = {},responsive = True, style = {"width":"38vw","height":"30vh"}),
                        html.Hr(className = hr_class,style = hr_style),
                        
                        
                        html.H6("Cumulative cases in the seleced county",className = col_title),
                        dcc.Graph(id = "line_chart2",figure = {},responsive = True, style = {"width":"38vw","height":"30vh"}),
                      
                  ],width=5,className =  col_class,style = {"margin-right":"10px","display":"inline-block"}),
                    dbc.Col([
                        dcc.RadioItems(
                        id = "map-buttons",
                        options = ["Cases","Fatalities"],value = "Cases",
                        inputStyle = {"margin-right":"2px","margin-left":"20px"}
                        ),
                        html.Div(id = "map-content", children = []),
                    ],width = 5,className = col_class,style = {"margin-left":"10px"})
                  
                ],className = classname_col,justify = "center")
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

@app.callback(Output("map-content","children"),[Input("map-buttons", "value")])
def render_map_content(value):
        if value == "Cases":
                return [dbc.Spinner(
                        dcc.Graph(figure = cases_fig, responsive=True,style = {"width":"40vw","height":"70vh"}))]
        if value == "Fatalities":
                return [dbc.Spinner(
                        dcc.Graph(figure = fatality_fig, responsive = True,style = {"width":"40vw","height":"60vh"} ))
                ]
                

#function for 7-day moving average
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
   
@app.callback( [Output("line_chart1", "figure"),
                Output("line_chart2", "figure"),
                Output("cases_value","children"),
                Output("death_value","children"),
                Output("prevalence","children")],
                [Input("county_chosen", "value"),
                Input("my-date-picker" , "start_date"),
                Input("my-date-picker" , "end_date")])


def update_graph_card(county, start_date, end_date):
    if len(county) == 0:
        return dash.no_update
    else:
        data_filter = county_daily_data[county_daily_data["county"] == county]
        data_filter = data_filter.sort_index().loc[start_date : end_date]
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
        
        cases_value = data[data["County"]== county]["cases"]
        death_value = data[data["County"]== county]["Death_cases"]
        prevalence = round(cases_value/data[data["County"] == county]["Population"]*100,1)
       
        return fig, fig2,cases_value,death_value, prevalence

#