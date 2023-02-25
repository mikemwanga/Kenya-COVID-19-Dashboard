#layout for vaccination tab
from utils import *
#laod data
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

margin = dict(l=20, r=20, t=20, b=20)
margin_size = "1px"

vac_fig = go.Figure()
vac_fig.add_trace(go.Bar(x = kenya_data["Proportion_vaccinated"],
                        y = kenya_data.index, \
                        orientation = "h",
                        marker = dict(color = pcolor_vaccination),
                        text = kenya_data["Proportion_vaccinated"], 
                        textposition = "outside"))
vac_fig.update_layout(bargap =0.008,autosize=False,margin = margin,
                      paper_bgcolor = bg_color,plot_bgcolor=bg_color,)
vac_fig.update_traces(width=0.6)
vac_fig.update_yaxes(tickfont = dict(size=tickfont))
vac_fig.update_xaxes(title = None, showgrid=True,showline=True, linewidth = 0.1, linecolor = "black", 
                     gridcolor = "gainsboro",tickfont = dict(size=tickfont))


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
                    ],width = 2,lg=2,className = "card_style ms-5",style = {"margin-right":margin_size}),
                
                dbc.Col([
                        dbc.CardBody([
                            html.Label(f"{fully_vaccinated_adults:,}",style = {"color":markercolor},className ="fs-4"),
                            html.P("Fully vaccinated adults",style = style_text)
                        ],className = card_class )
                    ],width = 2,lg=2,className = "card_style",style = {"margin-right":margin_size}),
                dbc.Col([
                        dbc.CardBody([
                            html.Label(f"{partially_vaccinated_adults:,}",style = {"color":markercolor},className ="fs-4"),
                            html.P("Partially vaccinated adults",style = style_text)
                        ],className = card_class )
                    ],width = 2,lg=2,className = "card_style",style = {"margin-right":margin_size}),
                dbc.Col([
                        dbc.CardBody([
                            html.Label(f"{booster_doses:,}",style = {"color":markercolor},className ="fs-4"),
                            html.P("Booster doses received",style = style_text)
                        ],className = card_class )
                    ],width = 2,lg=2,className = "card_style",style = {"margin-right":margin_size}),
                dbc.Col([
                        dbc.CardBody([
                            html.Label(f"{round(perc_vaccinated,1):,}%",style = {"color":markercolor},className ="fs-4"),
                            html.P("Fully vaccinated population",style = style_text)
                        ],className = card_class )
                    ],width = 2,lg=2,className = "card_style me-5"),
                
            ],className = hm.classname_col,justify = "center"),
            dbc.Row([
                dbc.Col([
                    html.Br(),
                    html.Label("Proportion of fully vaccinated persons by county", className = "text-dark ms-5 fs-6 fw-bold"),
                        dcc.Graph(figure = vac_fig,responsive = True, style = {"width":"450px","height":"700px"})
                ],width = 5,lg=4,className = col_class,style = {"margin-right":"10px"}),
                
                dbc.Col([
                    html.Br(),
                    html.Label("Layout map showing level of vaccination across the country",className = "text-dark ms-5 fs-6 fw-bold"),
                    dcc.Graph(figure = cases_fig,responsive = True, style = {"width":"650px","height":"700px"})
                    
                ],width = 6,lg=5,className = col_class,style = {"margin-left":"10px"})
            ],className = classname_col,justify = "center"),
            
            hm.reference
])
