from utils import *

def load_home_data():
    #global daily_updates_moh,county_daily_updates,daily_cases,age_gender_data,data #
    #RECOMMENDED TO AVOID USING GLOBAL FUCNTION AS IT MAKES CODE HARD TO UNDERSTAND. INSTEAD UTILIZE RETURN IN FUNCTIONS
    daily_updates_moh =  pd.read_excel(DATA_PATH.joinpath("daily_updates_metadata.xlsx"))
    daily_updates_moh.set_index("Date", inplace=True)
    county_daily_updates = pd.read_excel(DATA_PATH.joinpath("county_daily_updates.xlsx"), 
                                         parse_dates=["Date"], index_col='Date')
    daily_cases = pd.read_csv(DATA_PATH.joinpath("covid_daily_data.csv"))
    daily_cases["Date"] = pd.to_datetime(daily_cases["Date"],format = "%d/%m/%Y")
    # print(daily_cases.tail())
    age_gender_data = pd.read_table(DATA_PATH.joinpath("age_gender_data.txt"),sep = "\t")
    data = pd.read_csv(DATA_PATH.joinpath("cases_per_county.csv"))
    data["percentage_cases"] = round(data["cases"]/data["cases"].sum() * 100,2)
    return daily_updates_moh,county_daily_updates,daily_cases,age_gender_data,data

def daily_plots(df,observation1,observation2):#, observation2
    fig = go.Figure()
    fig.add_trace(go.Scatter( x = df["Date"],mode='none', y = df[observation1],fill='tonext',hovertext=df['Reported_Cases']))
    fig.add_trace(go.Scatter(x = df["Date"], y = df[observation2]))
    fig.update_layout(showlegend=False,margin = margin)
    fig.update_xaxes(showgrid=False,showline=True,nticks=10,ticks='outside',linecolor = axis_color,tickfont = dict(size=tickfont))
    fig.update_yaxes(tickfont = dict(size=tickfont),nticks=15,title = "7-day Average", title_font = {"size":titlefont})
    return fig

  #age gender plots
def age_gender_plots2(data):
            #plot for cases based on gender and age
            age_gender_cases_plot = go.Figure()
            
            age_gender_cases_plot.add_trace(go.Bar(y = data["age_groups"], x = data["Female_cases"]*-1, orientation="h",name = "Female",
                                    text = data["Female_cases"],hoverinfo = "text", textfont = dict(size=1,color ="#2C3E50")))#,marker=dict(color="#2C3E50"))), #marker=dict(color='#18BC9C')
            
            age_gender_cases_plot.add_trace(go.Bar(y = data["age_groups"], x = data["Male_cases"], orientation="h",name = "Male",
                                    hoverinfo = "x")),
                                
            age_gender_cases_plot.update_layout(barmode = "relative",bargap = 0.0,bargroupgap=0,
                        xaxis =  dict(tickvals = [-50000,-40000,-30000,-20000,-10000,0,10000,20000,30000,40000,50000],
                                        ticktext = ["50k","40k","30k","20k","10k","0","10k","20k","30k","40k","50k"]),
                        margin=margin,
                        legend = dict(orientation = "h",title=None,font = dict(size=9)))
            
            age_gender_cases_plot.update_yaxes(tickfont = dict(size=tickfont),title = "Age group",title_font = {"size":titlefont})
            age_gender_cases_plot.update_xaxes(linecolor = axis_color,ticks='outside',tickfont = dict(size=tickfont),title = None,title_font = {"size":titlefont} )
            age_gender_cases_plot.update_traces(width=0.6)
            
            #--------------------------------------------------------------------------------------------------------------------
            #plot for deaths based on gender and age
            age_gender_death_plot = go.Figure()
            age_gender_death_plot.add_trace(go.Bar(y = data["age_groups"], x = data["Female_deaths"]*-1, orientation="h",name = "Female",
                                        text = data["Female_deaths"],hoverinfo = "text", textfont = dict(color ="#2C3E50",size=1)))
            age_gender_death_plot.add_trace(go.Bar(y = data["age_groups"], x = data["Male_deaths"], orientation="h",name = "Male",
                                        hoverinfo = "x" ))
            age_gender_death_plot.update_layout(barmode = "relative",bargroupgap=0,bargap = 0,
                        xaxis =  dict(tickvals = [-800,-600,-400,-200,-100,0,100,200,400,600,800],
                                        ticktext = ["800","600","400","200","100","0","100","200","400","600","800"]),#bargap = 0.0
                        margin=margin,
                        legend = dict(orientation = "h",font = dict(size=9)))
            age_gender_death_plot.update_yaxes(tickfont = dict(size=tickfont),title = "Age group",title_font = {"size":titlefont})
            age_gender_death_plot.update_xaxes(linecolor = axis_color,ticks='outside',tickfont = dict(size=tickfont),title = None,title_font = {"size":titlefont})
            age_gender_death_plot.update_traces(width=0.6)
            
            total_female_cases = data["Female_cases"].sum()
            total_male_cases = data["Male_cases"].sum()
            perc_female_cases = total_female_cases/(total_female_cases + total_male_cases)
            perc_male_cases = total_male_cases/(total_female_cases + total_male_cases)
            
            total_female_death = data["Female_deaths"].sum()
            total_male_death = data["Male_deaths"].sum()
            perc_female_deaths = total_female_death/(total_female_death+total_male_death )
            perc_male_deaths = total_male_death/(total_female_death+total_male_death )
            
            return age_gender_cases_plot,age_gender_death_plot
            
            #return age_gender_cases_plot,age_gender_death_plot,total_female_cases, total_male_cases, perc_female_cases,perc_male_cases,total_female_death,total_male_death,perc_female_deaths,perc_male_deaths
           
layout = html.Div([
        html.Div(id = "home-content"),
        interval
]),

@app.callback(
    Output("home-content","children"),
    Input("interval-component", "n_intervals")
)

def update_home_content(n_intervals):
    daily_updates_moh,county_daily_updates,daily_cases,age_gender_data,data = load_home_data()
    test_date = "2023-06-14"
    daily_updates_moh = daily_updates_moh[pd.notnull(daily_updates_moh.index)]
    test_dates = datetime.strptime(test_date,"%Y-%m-%d").strftime("%B %d, %Y")
    #print(daily_updates_moh.index[-1])
    update_date = datetime.strftime(daily_updates_moh.index[-1],"%B, %d %Y")
    # update_date = datetime.strftime("2024-03-14","%B, %d %Y")

    total_cases = daily_updates_moh["total_confirmed_cases"].dropna().iat[-1]
    total_tests =  daily_updates_moh["cumulative_tests"].dropna().iat[-1]
    total_deaths = daily_updates_moh["cumulative_fatalities"].dropna().iat[-1]
    total_recoveries = daily_updates_moh["total_recoveries"].dropna().iat[-1]
    overall_positivity = round(total_cases/total_tests*100,1)
    test_data = daily_updates_moh.loc[daily_updates_moh.index == "2023-01-26"]
    new_cases_last_24hrs = test_data["new_cases_last_24_hrs"].iat[0]
    samplesize_last_24hrs = int(test_data["sample_size_last_24_hrs"].iat[0])
    posity_last_24 = round((new_cases_last_24hrs/samplesize_last_24hrs)*100,1)
    fatalities_last_24 = test_data["recorded_deaths_last_24_hrs"].iat[-1]
    recoveries_last_24 = daily_updates_moh["recoveries_last_24_hrs"].dropna().iat[-1]
    
    ###
    cases_trend = daily_plots(daily_cases,"moving_average_cases","moving_average_cases") #"Reported_Cases",plot of daily reported infections
    deaths_trends = daily_plots(daily_cases,"moving_average_deaths","moving_average_deaths") #,"moving_average_deaths"
    
    #county plot for daily updates
    filtered_data = county_daily_updates.iloc[[-1]].fillna(0)
    filtered_data =  filtered_data.astype(int)
    filtered_data = filtered_data.loc[:,(filtered_data != 0).any(axis=0)].T
    filtered_data = filtered_data.rename(columns = {filtered_data.columns[0]:"Cases"})
    filtered_data.sort_values("Cases", ascending=True, inplace=True)
    max_value = max(filtered_data["Cases"]) #initiate maximum value to set the range of values
    fig_county = px.bar(filtered_data, x = "Cases", text_auto=True,range_x =[0,max_value+3])#, color_discrete_sequence=[markercolor])
    fig_county.update_traces(textposition = "outside", textfont_size=10,cliponaxis=True, width=0.6)
    fig_county.update_layout(margin = margin,font_size=10,uniformtext_minsize = 3, yaxis_title = None)
    fig_county.update_xaxes(title = "Reported cases",linecolor = "black",tickfont = dict(size=10),title_font = {"size":10})
    fig_county.update_yaxes(tickfont = dict(size=10),title_font = {"size":10})
    
    #most affected counties plot
    affected_counties = px.bar(data.sort_values("cases",ascending=False).head(n=8),
                            x = "percentage_cases",y="County",text_auto=True,orientation = "h") #range_x=[0,45]
    affected_counties.update_yaxes(title = None,tickfont = dict(size=tickfont), autorange = "reversed")
    affected_counties.update_xaxes(nticks=8,title = "Prevalence (%)",linecolor = "black",tickfont = dict(size=tickfont),
                                title_font = {"size":10})
    affected_counties.update_traces(textposition = "outside",textfont_size=10,width=0.6)
    affected_counties.update_layout(margin=margin)
    
    
    age_gender_cases_plot,age_gender_death_plot = age_gender_plots2(age_gender_data)
    
    homelayout = html.Div([
        dbc.Row([
            dbc.Col([
                html.P(f"""Data as of: {update_date}""", className = "text-end text-primary", style = {"font-size":12}), #{update_date}
                html.P("This dashboard allows a visualization of COVID-19 disease trends in cases, fatalities, vaccination and variant diversity. \
                This platform intergrates data from Ministry of Health of Republic of Kenya, GISAID and other SARS-CoV-2 associated studies.",
                className = "fs-6",style ={"text-align":"start"}),
                html.Hr(),
            ],xs=10,lg=10,xxl=10),
        ],justify="center", className = "mb-1 ms-3 me-3 ps-3 pe-3 mt-5 pt-5"),
        
        dbc.Row([
            dbc.Row([
                dbc.Col([
                    html.P([html.Label("CASE UPDATES",className = col_title,style = style_title)]),
                ],width=11,className='ms-3')
            ],justify='center'),
            
            dbc.Col([
                dbc.CardBody([
                    html.Label(f"{int(total_cases):,}",className ="text-danger fs-4"),
                    html.P("Total reported cases",style = style_text)
                ],className = card_class )
            ],xs=5,md=3,lg=2,xxl=2,className = "card_style",style = {"margin-right":"5px"}),
            
            dbc.Col([
                dbc.CardBody([
                    html.Label(f"{int(total_deaths):,}",className ="text-dark fs-4"),
                    html.P("Total reported deaths",style = style_text),
                ],className = card_class)
            ],xs=5,md=3,lg=2,xxl=2,className = "card_style",style = {"margin-right":"5px"}),
            
            dbc.Col([
                dbc.CardBody([
                    html.Label(f"{int(total_recoveries):,}",className = "text-success fs-4"),
                    html.P("Reported recoveries",style = style_text),
                ],className = card_class)
            ],xs=5,md=3,lg=2,xxl=2,className = "card_style",style = {"margin-right":"5px"}),
            
            dbc.Col([
                dbc.CardBody([
                    html.Label(f"{int(total_tests):,}",className = "text-primary fs-4"),
                    html.P("Tests done",style = style_text),
                ],className = card_class)
            ],xs=5,md=3,lg=2,xxl=2,className = "card_style"),
            
            dbc.Col([
                dbc.CardBody([
                    html.Strong(f"{overall_positivity}",className = "text-info fs-3"),html.Span(children="%",className = "text-info fs-4"), 
                    html.P("Overall Positivity",style = style_text),
                ],className = card_class)
            ],xs=5,md=3,lg=2,xxl=2,className = "card_style",style = {"margin-left":"10px"})
            
        ],justify="center",align = "center", className = "bg-secondary bg-opacity-10 g-1 justify-content-center"),
        
   

        dbc.Row([
            dbc.Col([
                dbc.Card([  
                    html.P([html.Label("TESTING UPDATES",className = col_title,style = style_title),
                            html.Br(),html.A(f" On {test_dates}",style={"font-size":12})]),
                    html.Hr(className =hr_class,style=hr_style),
                            html.H6("Cases",className=col1_class),
                            html.Hr(className = col1_class,style = {"width":"50%"}),
                            html.Strong(new_cases_last_24hrs,className = val_class),
                            #html.Span(children = [arrow_type,cases_fold_value],className = fold_change_class,
                    #                style = {"margin-left":"20px"}),
                    html.Hr(className =hr_class,style=hr_style),
                            html.H6("Positivity",className=col1_class),
                            html.Hr(className=col1_class,style = {"width":"50%"}),
                            html.Strong(f"{posity_last_24}%",className = val_class), 
                    html.Hr(className =hr_class,style=hr_style),
                        html.H6("Fatalities",className = col1_class),
                        html.Hr(className=col1_class,style = {"width":"50%"}),
                        html.Strong(fatalities_last_24 ,className = val_class),
                        #html.Span(children = [fat_arrow_type, fat_fold_value],className = fat_fold_change_class,
                        #           style = {"margin-left":"20px"}),
                    html.Hr(className =hr_class,style=hr_style),
                            html.H6("Recoveries",className = col1_class),
                            html.Hr(className = col1_class,style = {"width":"50%"}),
                            html.Strong(recoveries_last_24,className = val_class),
                            #html.Span(children = [rec_arrow_type, rec_fold_value],className = rec_fold_change_class,
                            #       style = {"margin-left":"20px"}),
                    html.Hr(className =hr_class,style=hr_style),
                            html.H6("Samples Tested",className = col1_class),
                            html.Hr(className = col1_class,style = {"width":"50%"}),
                            html.Strong(samplesize_last_24hrs,className = val_class),
                    html.Hr(),
                ],body=True,className='h-100 border-0')
            ],xs=10,md=1,lg=2,xxl=2,className = 'mt-1'),
            
            dbc.Col([
                dbc.Card([
                    html.P("TRENDS IN CASES",className = col_title,style = style_title),
                    dcc.Graph(figure=cases_trend,responsive = True, style = {"width":"30hw","height":"25vh"},   config= plotly_display),
                ],className='border-0'),
                space,
                dbc.Card([
                    html.P("TRENDS IN FATALITIES",className = col_title,style = style_title),
                    dcc.Graph(figure = deaths_trends,responsive = True, style = {"width":"30hw","height":"25vh"},config= plotly_display),
                ],className='border-0 mt-1'),

                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([  
                            html.P("COUNTIES WITH RECENT UPDATES",className = col_title,style = style_title),
                            dcc.Graph(figure = fig_county,responsive = True, style = {"height":"25vh"},config= plotly_display),
                            ])
                        ],className='border-0 mt-1'),

                        dbc.Card([
                        html.P("CASES BY AGE AND GENDER",className = col_title,style = style_title),
                        dcc.Graph(figure = age_gender_cases_plot,responsive = True,style = {"height":"30vh"},config= plotly_display),
                        ],className='border-0 mt-1'),   
                    ]),
                    dbc.Col([
                        dbc.Card([
                        html.P("MOST AFFECTED COUNTIES",className = col_title,style = style_title),
                        dcc.Graph(figure = affected_counties, responsive = True, style = {"height":"25vh"},config= plotly_display),
                        ],body=True,className='border-0 mt-1'),

                        dbc.Card([
                        #html.Hr(className = hr_class, style = hr_style),
                        html.P("FATALITIES BY AGE AND GENDER",className = col_title,style = style_title),
                        dcc.Graph(figure= age_gender_death_plot, responsive = True, style = {"height":"30vh"},config= plotly_display),
                        ],className='border-0 mt-1'),
                    ]),
                      

                ],justify='center',className= midrow_classname)


            ],md=7,className='mt-3') #className = col_class,,style={"height":1200}
            
        ],justify = "center"),
            
            # dbc.Col([
                                    
            #     html.P("COUNTIES WITH RECENT UPDATES",className = col_title,style = style_title),
            #     dcc.Graph(figure = fig_county,responsive = True, style = {"width":"30hw","height":"25vh"},config= plotly_display),
            #     html.Hr(className = hr_class, style = hr_style),
                        
            #     html.P("TRENDS IN CASES",className = col_title,style = style_title),
            #     dcc.Graph(figure=cases_trend,responsive = True, style = {"width":"30hw","height":"25vh"},config= plotly_display),
                
            #     html.Hr(className = hr_class, style = hr_style),
            #     html.P("CASES BY AGE AND GENDER",className = col_title,style = style_title),
            #     dcc.Graph(figure = age_gender_cases_plot,responsive = True,style = {"width":"25hw","height":"30vh"},config= plotly_display),
                        
            # ],xs=10,md=5,lg=4,xxl=4,className = col_class,style = {"margin-left":"15px","margin-right":"0px","height":900} ),
            
            # dbc.Col([
            #     html.P("MOST AFFECTED COUNTIES",className = col_title,style = style_title),
            #     dcc.Graph(figure = affected_counties, responsive = True, style = {"width":"32hw","height":"25vh"},config= plotly_display),
            #     html.Hr(className = hr_class, style = hr_style),
            #     html.P("TRENDS IN FATALITIES",className = col_title,style = style_title),
            #     dcc.Graph(figure = deaths_trends,responsive = True, style = {"width":"30hw","height":"25vh"},config= plotly_display),
                
            #     html.Hr(className = hr_class, style = hr_style),
            #     html.P("FATALITIES BY AGE AND GENDER",className = col_title,style = style_title),
            #     dcc.Graph(figure= age_gender_death_plot, responsive = True, style = {"width":"25hw","height":"30vh"},config= plotly_display),#
            # ],xs=10,md=5,lg=4,xxl=4,className = col_class,style = {"margin-left":"15px","margin-right":"0px","height":900}),
                        
                        
        
        
        reference
        
    ])
    
    return homelayout