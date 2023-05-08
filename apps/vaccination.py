#layout for vaccination tab
from utils import *
#load_figure_template("pulse")
#laod data
def load_data():
    global vac_by_age, kenya_data,daily_updates_moh,kenya_county,total_doses_administered,total_vaccines_received,fully_vaccinated_adults \
            ,partially_vaccinated_adults,booster_doses,perc_vaccinated
            
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
    total_vaccines_received = daily_updates_moh["total_vaccines_received"].dropna().iat[-1]
    fully_vaccinated_adults= daily_updates_moh["fully_vaccinated_adult_population"].dropna().iat[-1]
    partially_vaccinated_adults= daily_updates_moh["partially_vaccinated_adult_population"].dropna().iat[-1]
    booster_doses = daily_updates_moh["Booster_doses"].dropna().iat[-1]
    perc_vaccinated = round(daily_updates_moh["proportion_of_fully_vaccinated_adult_population"].dropna().iat[-1],1)
    
    return vac_by_age,kenya_data,daily_updates_moh,kenya_county,total_doses_administered,total_vaccines_received,fully_vaccinated_adults \
            ,partially_vaccinated_adults,booster_doses,perc_vaccinated
    

#vaccination by age plot
def vaccination_fig():
    global vac_age_fig
    vac_age_fig = px.bar(vac_by_age, x = "Age_years", y = ["partially_vaccinated","administered_dose_2","administered_dose_1",], barmode="group")
    vac_age_fig.update_yaxes(title = "Frequency",title_font = {"size":tickfont}, tickfont = dict(size=tickfont),linewidth = 0.1, linecolor = "black")
    vac_age_fig.update_xaxes(title = "Age-group", showgrid=False,showline=True, linewidth = 0.1, linecolor = "black", 
                        tickfont = dict(size=tickfont),title_font = {"size":tickfont})
    vac_age_fig.update_layout(margin=margin,legend = dict(orientation = "v",title = None,xanchor = "right",  # yanchor  = "top",y=0.2,
                                            font = dict(size=10)))
    vac_age_fig["layout"]["xaxis"]["autorange"] = "reversed"
    return vac_age_fig

#-------------------------
def plot_figure(data):
    fig = go.Figure()
    fig.add_trace(go.Bar(x = data["Proportion_vaccinated"],
                            y = data.index, \
                            orientation = "h",
                            #marker = dict(color = pcolor_vaccination),
                            text = data["Proportion_vaccinated"], 
                            textposition = "outside"))
    fig.update_layout(bargap =0.008,autosize=False,margin = dict(l=2, r=20, t=5, b=5),paper_bgcolor = bg_color,plot_bgcolor=bg_color,)
    fig.update_traces(width=0.6)
    fig.update_yaxes(tickfont = dict(size=tickfont))
    fig.update_xaxes(range = [0,60],title = "Proportion Vaccinated", showgrid=True,showline=True, linewidth = 0.1, linecolor = "black", 
                     gridcolor = "gainsboro",tickfont = dict(size=tickfont),title_font = {"size":tickfont})
    return fig

#set layout
layout = html.Div([
        dbc.Row([
            dbc.Col([
                html.H5("Visualization of vaccination across the country",className = col_title, style ={"text-align":"start"}),
                html.Hr(),
            ], width = 11, lg=10),
            #html.H5("Countrywide Summary"),
        ],justify="center", className = "mb-2 ms-4 me-4 ps-4 pe-4 mt-5 pt-5"),
    
    
    html.Div(id = "vaccine-content"),
    interval
]),

@callback(Output("vaccine-content","children"),Input("interval-component", "n_intervals"),
)

def update_content(n_intervals):
    load_data(),
    vac_fig1 = plot_figure(kenya_data.head(n=24))
    vac_fig2 = plot_figure(kenya_data.tail(n=23))
    vac_age_fig = vaccination_fig()
    

    dev = html.Div([
                # dbc.Row([
                #         dbc.Col([
                #             html.H5("Visualization of vaccination across the country",className = col_title, style ={"text-align":"start"}),
                #             html.Hr(),
                #         ], width = 11, lg=10),
                #         #html.H5("Countrywide Summary"),
                # ],justify="center", className = "mb-2 ms-4 me-4 ps-4 pe-4 mt-5 pt-5"),

                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.Label(f"{int(total_vaccines_received):,}",style = {"color":marker_text},className ="fs-5"),
                                html.P("Received Doses",style = style_text)
                            ])
                        ], className='text-center border-0 rounded-0',style = {}),

                        dbc.Card([
                            dbc.CardBody([
                                html.Label(f"{int(fully_vaccinated_adults):,}",style = {"color":marker_text},className ="fs-5"),
                                html.P("Fully vaccinated",style = style_text)
                            ])
                        ], className='text-center border-0 rounded-0 mt-1',style = {}),

                        dbc.Card([
                            dbc.CardBody([
                               html.Label(f"{int(partially_vaccinated_adults):,}",style = {"color":marker_text},className ="fs-5"),
                                html.P("Partially vaccinated",style = style_text)
                            ])
                        ], className='text-center border-0 mt-1 rounded-0',style = {})
                    ],xs=5, md=2),
                    
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.Label(f"{int(total_doses_administered):,}",style = {"color":marker_text},className ="fs-5"),
                                html.P("Total Doses",style = style_text),
                            ]), 

                        ], className='border-0 text-center rounded-0',style = {}),

                        dbc.Card([
                           dbc.CardBody([
                               html.Label(f"{int(booster_doses):,}",style = {"color":marker_text},className ="fs-5"),
                               html.P("Booster doses",style = style_text),
                           ])
                        ], className='border-0 text-center rounded-0 mt-1',style = {}),

                        dbc.Card([
                           dbc.CardBody([
                               html.Label(f"{round(perc_vaccinated,1):,}%",style = {"color":marker_text},className ="fs-5"),
                               html.P("Fully vaccinated",style = style_text)
                           ])
                        ], className='text-center border-0 mt-1 rounded-0')    
                    ],xs=5, md=2),

                    dbc.Col([
                        dbc.Card([
                            html.P("Vaccination by Age and Dose",className = col_title),
                            dbc.CardBody([
                                dcc.Graph(figure = vac_age_fig,responsive = True, style = {"width":"25hw","height":"30vh"}),#"width":"25hw","height":"30vh"
                            ]),
                        ], className='border-0 rounded-0'),
                    ],xs=10,md=6, lg=5),

                ],justify="center"), #,align="center"

                dbc.Row([
                    dbc.Col([

                        dbc.Card([
                            html.P("Proportion of Vaccinated Persons at County Level",className = col_title),
                            dbc.Row([
                                dbc.Col(
                                    dbc.CardBody([
                                        dcc.Graph(figure = vac_fig2,responsive = True, style = {"width":"50hw","height":"60vh"})
                                    ],class_name = "border-end")
                                ,className = "col-md-6"),

                                dbc.Col(
                                    dbc.CardBody(
                                        dcc.Graph(figure = vac_fig1,responsive = True, style = {"width":"50hw","height":"60vh"})
                                    ),
                                className = "col-md-6")
                            ],justify="center")
                        ],className = "border-0 rounded-0")
                    ],xs=10,md=10, lg=9)
                ],justify="center", className='align-items-center mt-3 mb-3'),

                reference       

        ],className=classname_col),
    return dev




# def map_plot(value):
#     fig = px.choropleth(kenya_data,
#                         geojson=kenya_data.geometry,
#                         locations=kenya_data.index, #must be index column
#                         #hover_data = {"County":True},# "random":False},
#                         color_continuous_scale="brwnyl",#tempo",#Brownly
#                         color=kenya_data["Proportion_vaccinated"],
#                         range_color=(10,60))
#     fig.update_geos(fitbounds = "locations", visible=False,scope="africa")
#     fig.update_coloraxes(colorbar = dict(title = None,orientation = "h",len=0.3,nticks = 5,thickness = 8,ticks="outside", x = 0.3,y=0.1))
#     fig.update_layout(margin = dict(l=5, r=5, t=5, b=5),paper_bgcolor = bg_color,plot_bgcolor=bg_color,
#                       geo = dict(bgcolor = bg_color,projection_scale=6,))
    
#     return fig

# cases_fig = map_plot(2)
#fatality_fig = map_plot("Death_cases",0.5)


# dev2 = dbc.Row([
#                 dbc.Col([
#                     html.Br(),
#                     dbc.CardBody([
#                             html.Label(f"{int(fully_vaccinated_adults):,}",style = {"color":marker_text},className ="fs-5"),
#                             html.P("Fully vaccinated",style = style_text)
#                     ],class_name = card_class ),
                    
#                     html.Hr(),html.Br(),
#                     dbc.CardBody([
#                             html.Label(f"{int(partially_vaccinated_adults):,}",style = {"color":marker_text},className ="fs-5"),
#                             html.P("Partially vaccinated",style = style_text)
#                     ],className = card_class ),
                    
#                     html.Hr(),html.Br(),   
#                 ],xs=4, md=3,lg=2,className = col_class, style = {"height":"100%"}),
                
#                 dbc.Col([     
#                     html.Br(),     
#                     dbc.CardBody([
#                             html.Label(f"{int(booster_doses):,}",style = {"color":marker_text},className ="fs-5"),
#                             html.P("Booster doses",style = style_text)
#                     ],className = card_class ),
                    
#                     html.Hr(),html.Br(),
#                     dbc.CardBody([
#                             html.Label(f"{round(perc_vaccinated,1):,}%",style = {"color":marker_text},className ="fs-5"),
#                             html.P("Fully vaccinated",style = style_text)
#                     ],className = card_class ),
#                     html.Hr(),html.Br(),
#                 ],xs=4,md=3,lg=2,className =col_class,style = {"margin-left" : "0px","height":"100%"} ), #, 
                
#                 dbc.Col([
#                     dcc.Graph(figure = vac_age_fig,responsive = True, style = {"width":"50hw","height":"40vh"})
#                 ],xs=8,md=6,lg=5, className = col_class,style = {"margin-left" : "10px","height":"75%"}),
                
#             ],justify = "center", className = "bg-secondary bg-opacity-10 g-1 justify-content-center p-2 m-2", style = {"height":"100%"}),
            
# ]), #,style={"height":"100vh"}
            
            
            
            
            
# div = html.Div([ dbc.Row([
#                 dbc.Col([
#                         dbc.CardBody([
#                             html.Label(f"{int(total_doses_administered):,}",style = {"color":marker_text},className ="fs-4"),
#                             html.P("Administered Doses",style = style_text)
#                         ],className = card_class )
#                     ],width = 2,xs=5,md=3,lg=2,className = "card_style ms-5",style = {"margin-right":margin_size}),
                
#                 dbc.Col([
#                         dbc.CardBody([
#                             html.Label(f"{int(fully_vaccinated_adults):,}",style = {"color":marker_text},className ="fs-4"),
#                             html.P("Fully vaccinated adults",style = style_text)
#                         ],className = card_class )
#                     ],width = 2,xs=5,md=3,lg=2,className = "card_style",style = {"margin-right":margin_size}),
#                 dbc.Col([
#                         dbc.CardBody([
#                             html.Label(f"{int(partially_vaccinated_adults):,}",style = {"color":marker_text},className ="fs-4"),
#                             html.P("Partially vaccinated adults",style = style_text)
#                         ],className = card_class )
#                     ],width = 2,xs=5,md=3,lg=2,className = "card_style",style = {"margin-right":margin_size}),
#                 dbc.Col([
#                         dbc.CardBody([
#                             html.Label(f"{int(booster_doses):,}",style = {"color":marker_text},className ="fs-4"),
#                             html.P("Booster doses received",style = style_text)
#                         ],className = card_class )
#                     ],width = 2,xs=5,md=3,lg=2,className = "card_style",style = {"margin-right":margin_size}),
#                 dbc.Col([
#                         dbc.CardBody([
#                             html.Label(f"{round(perc_vaccinated,1):,}%",style = {"color":marker_text},className ="fs-4"),
#                             html.P("Fully vaccinated population",style = style_text)
#                         ],className = card_class )
#                     ],width = 2,xs=6,md=3,lg=2,className = "card_style me-5"),
                
#             ],className = hm.classname_col,justify = "center"),
#             dbc.Row([
#                 html.Div([
#                     dcc.Dropdown(
#                     id = "Filter_metrics",
#                     options = [
#                         {"label" :"Vaccination by County","value":"vaccination_county"},
#                         {"label":"Vaccination by Age","value":"vaccination_age"}
#                     ],
#                     value = "vaccination_county",
                
#                     ),
#                 ],style = {"width":"30%","font-size":12,"justify-flex":"flex-end"}),
#             ],justify="end",className = "me-3 pe-3"),
            
#             html.Div(id = "content_vacc"),
            
#             hm.reference
# ])
# vaccination_by_count = html.Div([
#         dbc.Row([
#                 dbc.Col([
#                     html.Br(),
#                     html.Label("Proportion of fully vaccinated Adults", className = "text-dark ms-5 fw-normal",style = {"font-size":"14"}),
                
#                     dcc.Graph(figure = vac_fig,responsive = True, style = {"width":"25hw","height":"120vh"})# {"width":"400px","height":"550px"})
                
#                 ],width=5,xs=8,md=4,className = col_class,style = {"margin-right":"7px"}),
                
#                 dbc.Col([
#                     html.Br(),
#                     html.Label("Layout map showing level of vaccination across the country",className = "text-dark ms-5 fw-normal",style = {"font-size":"14"}),
#                     dcc.Graph(figure = cases_fig,responsive = True, style =  {"width":"25hw","height":"120vh"})# {"width":"550px","height":"550px"})
#                 ],width=6,xs=8,md=4,className = col_class,style = {"margin-left":"10px"})
                
#             ],className = classname_col,justify = "center"),
#         ]),

# vaccination_by_age = html.Div([
    
#                 dbc.Row([
                    
#                     dbc.Col([
#                     dcc.Graph(figure = vac_age_fig,responsive = True, style = {"width":"50hw","height":"40vh"} )
#                     ],width=6,xs=10,md=8,lg=5,className = col_class),
#                     dbc.Col([],width=2)
#                 ],className = classname_col,justify = "center")
    
# ]),



# @app.callback(
#     Output("content_vacc", "children"),
#     Input("Filter_metrics","value")
# )

# def render_vaccination_data(value):
#     if value == "vaccination_county":
#         return vaccination_by_count
#     elif  value == "vaccination_age":
#          return vaccination_by_age
