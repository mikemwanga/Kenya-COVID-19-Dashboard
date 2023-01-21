import dash
from dash import dcc, html,dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.graph_objects import Layout
import warnings
import pathlib
import geopandas as gpd
load_figure_template("sandstone")
warnings.filterwarnings('ignore')
from app import app
PATH = pathlib.Path(__file__).parent


# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], # LUX, FLATLY LUMEN SPACELAB YETI
#                 suppress_callback_exceptions=True,
#                 meta_tags=[{"name":"viewport","content":"width=device-width,initial-scale=1.0"}])

#laod data
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data/").resolve()
daily_updates_moh =  pd.read_excel(DATA_PATH.joinpath("daily_updates_metadata.xlsx"))

metadata = pd.read_table(DATA_PATH.joinpath("county_metadata.tsv"))
kenya_county = gpd.read_file(DATA_PATH.joinpath("kenyan-counties/County.shp"))
kenya_county.loc[(kenya_county["COUNTY"] == "Keiyo-Marakwet"),"COUNTY"] = "Elgeyo Marakwet"
kenya_county.loc[(kenya_county["COUNTY"] == "Tharaka"),"COUNTY"] = "Tharaka Nithi"
kenya_data = pd.merge(kenya_county, metadata,left_on="COUNTY",right_on = "County",how="inner" ).drop(columns = ["COUNTY"])
kenya_data.sort_values("Proportion_vaccinated", ascending=True,inplace=True)
kenya_data =  kenya_data.set_index("County")


total_vaccines = daily_updates_moh["total_vaccines_received"].iat[-1]
fully_vaccinated_adults= daily_updates_moh["fully_vaccinated_adult_population"].iat[-1]
partially_vaccinated_adults= daily_updates_moh["partially_vaccinated_adult_population"].iat[-1]
booster_doses = daily_updates_moh["Booster_doses"].iat[-1]
perc_vaccinated = round(daily_updates_moh["proportion_of_fully_vaccinated_adult_population"].iat[-1],1)


card_style = "bg-light border rounded-3 shadow"
classname_col = "bg-light bg-opacity-0 g-1 p-2 m-2"
margin = dict(l=20, r=20, t=20, b=20)
pcolor = "#999999"
bg_color = "rgba(0,0,0,0)"
style_text ={"font-size":14,"text-align":"center"}
card_class = "text-center"
markercolor = "#8B0000"

vac_fig = go.Figure()
vac_fig.add_trace(go.Bar(x = kenya_data["Proportion_vaccinated"],
                        y = kenya_data.index, \
                        orientation = "h",
                        marker = dict(color = pcolor),
                        text = kenya_data["Proportion_vaccinated"], 
                        textposition = "outside"))
vac_fig.update_layout(uniformtext_minsize = 3, bargap =0.01,font_size=10,autosize=False,margin = margin,
                      paper_bgcolor = bg_color,plot_bgcolor=bg_color,)
vac_fig.update_traces( width=0.8)
vac_fig.update_xaxes(title = None, showgrid=True,showline=True, linewidth = 0.1, linecolor = "black", 
                     gridcolor = "gainsboro")


def map_plot(value):
    fig = px.choropleth(kenya_data,
                        geojson=kenya_data.geometry,
                        locations=kenya_data.index, #must be index column
                        #hover_data = {"County":True},# "random":False},
                        color_continuous_scale="brwnyl",#tempo",#Brownly
                        color=kenya_data["Proportion_vaccinated"],
                        range_color=(10,60))
    fig.update_geos(fitbounds = "locations", visible=False,scope="africa")
    fig.update_coloraxes(colorbar = dict(title = None,orientation = "h",len=0.3,nticks = 5,thickness = 8,ticks="outside", x = 0.3,y=0.1))
    fig.update_layout(margin = margin,paper_bgcolor = bg_color,plot_bgcolor=bg_color,
                      geo = dict(bgcolor = bg_color,projection_scale=6,))
    
    return fig

cases_fig = map_plot(2)
#fatality_fig = map_plot("Death_cases",0.5)



layout = html.Div([
    dbc.Row([
                    dbc.Col([
                        html.H5("Visualization of vaccination across the country", style ={"text-align":"start"}),
                        html.Hr(),
                    ], width = 11, xxl=10),
                    
                    
                    #html.H5("Countrywide Summary"),
                ],justify="center", className = "mb-2 ms-4 me-4 ps-4 pe-4 mt-5 pt-5"),
            dbc.Row([
                dbc.Col([
                        dbc.CardBody([
                            html.Label(f"{total_vaccines:,}",style = {"color":markercolor},className ="fs-4"),
                            html.P("Vaccines received",style = style_text)
                        ],className = card_class )
                    ],width = 2,lg=2,className = card_style,style = {"margin-right":"10px"}),
                
                dbc.Col([
                        dbc.CardBody([
                            html.Label(f"{fully_vaccinated_adults:,}",style = {"color":markercolor},className ="fs-4"),
                            html.P("Fully vaccinated adults",style = style_text)
                        ],className = card_class )
                    ],width = 2,lg=2,className = card_style,style = {"margin-right":"10px"}),
                dbc.Col([
                        dbc.CardBody([
                            html.Label(f"{partially_vaccinated_adults:,}",style = {"color":markercolor},className ="fs-4"),
                            html.P("Partially vaccinated adults",style = style_text)
                        ],className = card_class )
                    ],width = 2,lg=2,className = card_style,style = {"margin-right":"10px"}),
                dbc.Col([
                        dbc.CardBody([
                            html.Label(f"{booster_doses:,}",style = {"color":markercolor},className ="fs-4"),
                            html.P("Booster doses received",style = style_text)
                        ],className = card_class )
                    ],width = 2,lg=2,className = card_style,style = {"margin-right":"10px"}),
                dbc.Col([
                        dbc.CardBody([
                            html.Label(f"{round(perc_vaccinated,1):,}%",style = {"color":markercolor},className ="fs-4"),
                            html.P("Fully vaccinated vaccinated",style = style_text)
                        ],className = card_class )
                    ],width = 2,lg=2,className = card_style,style = {"margin-right":"0px"}),
                
            ],className = classname_col,justify = "center"),
            dbc.Row([
                dbc.Col([
                    html.Label("Proportion of fully vaccinated persons by county", className = "text-dark ms-5 fs-6 fw-bold"),
                        dcc.Graph(figure = vac_fig,responsive = True, style = {"width":"500px","height":"600px"})
                ],width = 4,lg=5,className = card_style,style = {"margin-right":"10px"}),
                
                dbc.Col([
                    html.Label("Layout map showing level of vaccination across the country",className = "text-dark ms-5 fs-6 fw-bold"),
                    dcc.Graph(figure = cases_fig,responsive = True, style = {"width":"650px","height":"700px"})
                    
                ],width = 6,lg=6,className = card_style,style = {"margin-left":"10px"})
            ],className = classname_col,justify = "center"),
            
            dbc.Row([
                #metadata.head()
            ])
])
