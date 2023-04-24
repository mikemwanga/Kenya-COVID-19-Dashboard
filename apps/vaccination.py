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
vac_by_age = pd.read_table(DATA_PATH.joinpath("vaccination_by_age.txt"))


total_doses_administered = daily_updates_moh["total_doses_administered"].dropna().iat[-1]
fully_vaccinated_adults= daily_updates_moh["fully_vaccinated_adult_population"].dropna().iat[-1]
partially_vaccinated_adults= daily_updates_moh["partially_vaccinated_adult_population"].dropna().iat[-1]
booster_doses = daily_updates_moh["Booster_doses"].dropna().iat[-1]
perc_vaccinated = round(daily_updates_moh["proportion_of_fully_vaccinated_adult_population"].dropna().iat[-1],1)

margin = dict(l=20, r=20, t=20, b=20)
margin_size = "1px"
marker_text = "#67001f"


#vaccination by age plot
vac_age_fig = px.bar(vac_by_age, x = "Age_years", y = ["partially_vaccinated","administered_dose_2","administered_dose_1",], barmode="group")


vac_age_fig.update_yaxes(title = "Frequency", tickfont = dict(size=tickfont),linewidth = 0.1, linecolor = "black")
vac_age_fig.update_xaxes(title = None, showgrid=False,showline=True, linewidth = 0.1, linecolor = "black", 
                     tickfont = dict(size=tickfont))
#vac_age_fig.update_traces(width=0.3)
vac_age_fig.update_layout(margin=margin,legend = dict(orientation = "h",title = None, yanchor  = "top", xanchor = "left",y=1.2,
                                        font = dict(size=10)))

vac_age_fig["layout"]["xaxis"]["autorange"] = "reversed"


#-------------------------
vac_fig = go.Figure()
vac_fig.add_trace(go.Bar(x = kenya_data["Proportion_vaccinated"],
                        y = kenya_data.index, \
                        orientation = "h",
                        marker = dict(color = pcolor_vaccination),
                        text = kenya_data["Proportion_vaccinated"], 
                        textposition = "outside"))
vac_fig.update_layout(bargap =0.008,autosize=False,margin = dict(l=2, r=20, t=5, b=5),
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
    fig.update_layout(margin = dict(l=5, r=5, t=5, b=5),paper_bgcolor = bg_color,plot_bgcolor=bg_color,
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
                            html.Label(f"{int(total_doses_administered):,}",style = {"color":marker_text},className ="fs-4"),
                            html.P("Administered Doses",style = style_text)
                        ],className = card_class )
                    ],width = 2,xs=5,md=3,lg=2,className = "card_style ms-5",style = {"margin-right":margin_size}),
                
                dbc.Col([
                        dbc.CardBody([
                            html.Label(f"{int(fully_vaccinated_adults):,}",style = {"color":marker_text},className ="fs-4"),
                            html.P("Fully vaccinated adults",style = style_text)
                        ],className = card_class )
                    ],width = 2,xs=5,md=3,lg=2,className = "card_style",style = {"margin-right":margin_size}),
                dbc.Col([
                        dbc.CardBody([
                            html.Label(f"{int(partially_vaccinated_adults):,}",style = {"color":marker_text},className ="fs-4"),
                            html.P("Partially vaccinated adults",style = style_text)
                        ],className = card_class )
                    ],width = 2,xs=5,md=3,lg=2,className = "card_style",style = {"margin-right":margin_size}),
                dbc.Col([
                        dbc.CardBody([
                            html.Label(f"{int(booster_doses):,}",style = {"color":marker_text},className ="fs-4"),
                            html.P("Booster doses received",style = style_text)
                        ],className = card_class )
                    ],width = 2,xs=5,md=3,lg=2,className = "card_style",style = {"margin-right":margin_size}),
                dbc.Col([
                        dbc.CardBody([
                            html.Label(f"{round(perc_vaccinated,1):,}%",style = {"color":marker_text},className ="fs-4"),
                            html.P("Fully vaccinated population",style = style_text)
                        ],className = card_class )
                    ],width = 2,xs=6,md=3,lg=2,className = "card_style me-5"),
                
            ],className = hm.classname_col,justify = "center"),
            dbc.Row([
                html.Div([
                    dcc.Dropdown(
                    id = "Filter_metrics",
                    options = [
                        {"label" :"Vaccination by County","value":"vaccination_county"},
                        {"label":"Vaccination by Age","value":"vaccination_age"}
                    ],
                    value = "vaccination_county",
                
                    ),
                ],style = {"width":"30%","font-size":12,"justify-flex":"flex-end"}),
            ],justify="end",className = "me-3 pe-3"),
            
            html.Div(id = "content_vacc"),
            
            hm.reference
])
vaccination_by_count = html.Div([
        dbc.Row([
                dbc.Col([
                    #html.Br(),
                    html.Label("Proportion of fully vaccinated Adults", className = "text-dark ms-5 fw-normal",style = {"font-size":"14"}),
                
                    dcc.Graph(figure = vac_fig,responsive = True, style = {"width":"25hw","height":"120vh"})# {"width":"400px","height":"550px"})
                
                ],width=5,xs=8,md=4,className = col_class,style = {"margin-right":"7px"}),
                
                dbc.Col([
                    html.Br(),
                    html.Label("Layout map showing level of vaccination across the country",className = "text-dark ms-5 fw-normal",style = {"font-size":"14"}),
                    dcc.Graph(figure = cases_fig,responsive = True, style =  {"width":"25hw","height":"120vh"})# {"width":"550px","height":"550px"})
                ],width=6,xs=8,md=4,className = col_class,style = {"margin-left":"10px"})
                
            ],className = classname_col,justify = "center"),
        ]),

vaccination_by_age = html.Div([
    
                dbc.Row([
                    
                    dbc.Col([
                    dcc.Graph(figure = vac_age_fig,responsive = True, style = {"width":"50hw","height":"40vh"} )
                    ],width=6,xs=10,md=8,lg=5,className = col_class),
                    dbc.Col([],width=2)
                ],className = classname_col,justify = "center")
    
]),



@app.callback(
    Output("content_vacc", "children"),
    Input("Filter_metrics","value")
)

def render_vaccination_data(value):
    if value == "vaccination_county":
        return vaccination_by_count
    elif  value == "vaccination_age":
         return vaccination_by_age
