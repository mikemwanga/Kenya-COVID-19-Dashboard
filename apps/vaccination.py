#layout for vaccination tab
from utils import *
#load_figure_template("pulse")
#laod data
def load_data():
    global vac_by_age, kenya_data,daily_updates_moh,kenya_county,total_doses_administered,total_vaccines_received,fully_vaccinated_adults \
            ,partially_vaccinated_adults,booster_doses,perc_vaccinated
            
    daily_updates_moh =  pd.read_excel(DATA_PATH.joinpath("daily_updates_metadata.xlsx"))
    metadata = pd.read_table(DATA_PATH.joinpath("county_metadata.tsv"))
    #kenya_county = gpd.read_file(DATA_PATH.joinpath("kenyan-counties/County.shp"))
    #kenya_county.loc[(kenya_county["COUNTY"] == "Keiyo-Marakwet"),"COUNTY"] = "Elgeyo Marakwet"
    #kenya_county.loc[(kenya_county["COUNTY"] == "Tharaka"),"COUNTY"] = "Tharaka Nithi"
    #kenya_data = pd.merge(kenya_county, metadata,left_on="COUNTY",right_on = "County",how="inner" ).drop(columns = ["COUNTY"])
    kenya_data = metadata.copy()
    kenya_data.sort_values("Proportion_vaccinated", ascending=True,inplace=True)
    kenya_data =  kenya_data.set_index("County")
    vac_by_age = pd.read_table(DATA_PATH.joinpath("vaccination_by_age.txt"))
    total_doses_administered = daily_updates_moh["total_doses_administered"].dropna().iat[-1]
    total_vaccines_received = daily_updates_moh["total_vaccines_received"].dropna().iat[-1]
    fully_vaccinated_adults= daily_updates_moh["fully_vaccinated_adult_population"].dropna().iat[-1]
    partially_vaccinated_adults= daily_updates_moh["partially_vaccinated_adult_population"].dropna().iat[-1]
    booster_doses = daily_updates_moh["Booster_doses"].dropna().iat[-1]
    perc_vaccinated = round(daily_updates_moh["proportion_of_fully_vaccinated_adult_population"].dropna().iat[-1],1)
    
    return vac_by_age,kenya_data,daily_updates_moh,total_doses_administered,total_vaccines_received,fully_vaccinated_adults \
            ,partially_vaccinated_adults,booster_doses,perc_vaccinated #kenya_county
    

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
            ], width = 11, lg=8),
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
                    ],xs=5, md=3,lg=2,xxl=2,className=""),
                    
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
                          
                    ],xs=5, md=3,lg=2,xxl=2,className=""),

                    dbc.Col([
                        dbc.Card([
                            html.P("Vaccination by Age and Dose",className = col_title),
                            dbc.CardBody([
                                dcc.Graph(figure = vac_age_fig,responsive = True, style = {"width":"25hw","height":"30vh"}),#"width":"25hw","height":"30vh"
                            ]),
                        ], className='border-0 rounded-0'),
                    ],xs=10,md=6,lg=5,xxl=6),

                ],justify="center"), #,align="center"

                dbc.Row([
                    
                    dbc.Col([

                        dbc.Card([
                            html.P("PROPORTION OF VACCINATED PERSONS AT COUNTY LEVEL",className = col_title),
                            dbc.Row([
                                dbc.Col([
                                    dbc.CardBody([
                                        dcc.Graph(figure = vac_fig2,responsive = True, style = {"width":"50hw","height":"60vh"})
                                    ],class_name = "border-end")
                                ],xs=10,md=6,className = ""),

                                dbc.Col([
                                    dbc.CardBody(
                                        dcc.Graph(figure = vac_fig1,responsive = True, style = {"width":"50hw","height":"60vh"})
                                    ),
                                ],xs=10,md=6,) #col-md-6
                            ],justify="center"),
                            #set the model
                            dbc.Row([
                                dbc.Col([
                                html.Div([
                                    dmc.Button("more info",id="vacc_button",variant="outline",color = "gray",
                                               leftIcon=DashIconify(icon="bi:info-square-fill")),
                                    dbc.Modal([
                                        dbc.ModalBody(vaccination_content),
                                        dbc.ModalFooter(
                                            dbc.Button( "Close", id="close", className="ms-auto", n_clicks=0)
                                        )
                                    ],id="vacc_modal",size="xs",is_open=False,scrollable=True,centered = True)
                                ])
                            ],width=2,className = "me-1")
                                
                        ],justify="end",className = "mb-3"),
                            
                        ],className = "border-0 rounded-0"),
                    ],xs=10,md=11,lg=9,xxl=10)
                    
                ],justify="center", className='align-items-center mt-3 mb-3'),
                
                reference       

        ],className=classname_col),
    return dev

@app.callback(
    Output("vacc_modal", "is_open"),
    [Input("vacc_button", "n_clicks"),
    Input("close", "n_clicks")],
    [State("vacc_modal", "is_open")]
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open