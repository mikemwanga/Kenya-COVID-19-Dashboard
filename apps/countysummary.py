from utils import *
from apps import counties as ct

cases_per_county = pd.read_csv(DATA_PATH.joinpath("cases_per_county.csv"))

county_daily_data = ct.county_daily_data.copy()
county_daily_data["date_of_lab_confirmation"] = pd.to_datetime(county_daily_data["date_of_lab_confirmation"])
county_daily_data["Date"] = ct.county_daily_data["date_of_lab_confirmation"]#.dt.date
county_daily_data.set_index("Date", inplace = True)

county_age_gender_cases = pd.read_table(DATA_PATH.joinpath("county_age_gender_cases.txt"),sep="\t")
county_age_gender_deaths = pd.read_table(DATA_PATH.joinpath("county_age_gender_death.txt"),sep="\t")

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



layout = html.Div([
    
    dbc.Row([
        dbc.Col([
            html.H6("COVID-19 County Summary", className = "text-center fw-normal text-decoration-underline")
        ],width=6),
        dbc.Col([
            html.Div([
                html.Label("Select County",className="text-primary mb-0 pb-0",style = {"font-size":12}),

                dcc.Dropdown(
                    options = county_daily_data["county"].sort_values().unique(),
                    value = "Nairobi",
                    id = "selected_county"
                )
            ],style = {"width":"60%","font-size":12,"justify-flex":"flex-end"}),
        ],width=4)
    ],justify="end",className = "me-3 pe-3 mt-5 pt-4"),
    
    dbc.Row([
        dbc.Col([
            html.H5(id = "title", className = "text-center fw-bold text-decoration-underline"),

            
            dbc.Row([
                dbc.Col([
                    dbc.CardBody([
                        html.Label(id = "total_cases",className ="text-center text-danger fs-3"),
                        html.P("Total reported cases",style = style_text),
                    ],className = card_class)
                ],width=3),
                dbc.Col([
                    dbc.CardBody([
                        html.Label(id = f"total_deaths",className ="text-dark fs-3"),
                        html.P("Total reported fatalities",style = style_text),
                    ],className = card_class)
                ],width=3),
                dbc.Col([
                    dbc.CardBody([
                        html.Label(id = "affected",className ="text-info fs-3"),
                        html.P("Proportion affected",style = style_text),
                    ],className = card_class)
                ],width=3)
            ],justify="center"),
            
            dbc.Row([
               dbc.Col([
                   dcc.Graph("trends_plot_county",responsive = True, style = {"width":"30vw","height":"25vh"}),
               ],width=5),
               
               dbc.Col([
                   dcc.Graph("death_plot_county",responsive = True, style = {"width":"30vw","height":"25vh"}),
               ],width=5)
            ],justify="center"),
            
            dbc.Row([
               dbc.Col([
                   dcc.Graph("cases_age_gender",responsive = True, style = {"width":"30vw","height":"30vh"}),
               ],width=5),
               
               dbc.Col([
                   dcc.Graph("deaths_age_gender",responsive = True, style = {"width":"30vw","height":"30vh"}),
               ],width=5)
            ],justify="center"),
            
        ],width=12, lg=10),
        
    ],justify="center")
    
])
@app.callback(
        [   
            Output("title", "children"),
            Output("total_cases","children"),
            Output("total_deaths","children"),
            Output("affected","children"),
            Output("trends_plot_county", "figure"),
            Output("death_plot_county","figure"),
            Output("cases_age_gender","figure"),
            Output("deaths_age_gender","figure")
        ],
            Input("selected_county", "value")
)

def render_callback(county):
    if len(county) == 0:
        return dash.no_update
    else:
        title_county = f"COVID-19 {county} County Summary Report"
        data_county = county_daily_data[county_daily_data["county"].isin([county])]
        death_data = data_county[data_county["outcome"] == "Dead"] 
        data_filter= data_county[["county","lab_results", "date_of_lab_confirmation"]].\
            groupby(["county","date_of_lab_confirmation"]).count().reset_index()

        data_average = seven_day_average(data_filter, "lab_results")
        fig = px.line(data_average, x="date_of_lab_confirmation" , y = "moving_average" , color = "county")
        fig.update_yaxes(title = None, tickfont = tickfont_dict,showline=True, linewidth = 0.1, linecolor = "black")
        fig.update_xaxes(title = None,tickfont = tickfont_dict, showline=True,showgrid=False,linecolor = "black",)
        fig.update_layout(showlegend = False,hovermode="x unified",uniformtext_minsize = 3, bargap =0.05,margin =margin,)
                          #legend = dict(orientation = "h"))#,yanchor = "bottom"))#,y = 0,xanchor = "right",x = 1)) 
        
        #death plot
        death_data = death_data.groupby(["county","date_of_lab_confirmation"])[["date_of_lab_confirmation"]].count().rename(columns = {"date_of_lab_confirmation":"Freq"}).reset_index()
        death_data = seven_day_average(death_data,"Freq")
        fig_death = px.line(death_data, x = "date_of_lab_confirmation", y = "moving_average",color = "county")
        fig_death.update_yaxes(title = None,tickfont = tickfont_dict,showline=True, linewidth = 0.1, linecolor = "black")
        fig_death.update_xaxes(title = None,tickfont = tickfont_dict, showline=True,showgrid=False,linecolor = "black",)
        fig_death.update_layout(hovermode="x unified",uniformtext_minsize = 3, bargap =0.05,margin =margin,
                                showlegend = False)
                          #legend = dict(orientation = "h"))

        cases_gender = county_age_gender_cases[county_age_gender_cases["county"].isin([county])]
        deaths_gender = county_age_gender_deaths[county_age_gender_deaths["county"].isin([county])]
        
        fig_cases_gender = px.bar(cases_gender, x = "age_groups", y = "Frequency", color="sex",barmode="group")
        fig_cases_gender.update_yaxes(title = None,tickfont =tickfont_dict,showline=True, linewidth = 0.1, 
                                      linecolor = "black")
        fig_cases_gender.update_xaxes(title = None,tickfont =tickfont_dict,showline=True, linewidth = 0.1, 
                                      linecolor = "black")
        fig_cases_gender.update_layout(margin =margin,legend = dict(orientation="h",title=None,yanchor  = "top",
                                                    itemwidth=30,
                                        xanchor = "left",y=1.2,font = dict(size=9)))
        
        
        fig_deaths_gender = px.bar(deaths_gender, x = "age_groups", y = "Frequency", color="sex",barmode="group")
        fig_deaths_gender.update_xaxes(title = None,tickfont =tickfont_dict,showline=True, linewidth = 0.1, 
                                      linecolor = "black"),
        fig_deaths_gender.update_yaxes(title = None,tickfont =tickfont_dict,showline=True, linewidth = 0.1, 
                                      linecolor = "black")
        fig_deaths_gender.update_layout(margin =margin,
                                        legend = dict(orientation="h",title=None,yanchor  = "top",tracegroupgap = 5, 
                                                     xanchor = "left",y=1.2,font = dict(size=9)))
        
        cases = cases_per_county[cases_per_county["County"].isin([county])]["cases"].iat[-1]
        deaths = cases_per_county[cases_per_county["County"].isin([county])]["Death_cases"].iat[-1]
        affected = round(cases/cases_per_county[cases_per_county["County"].isin([county])]["Population"].iat[-1]*100,1)
        cases = f"{cases:,}"
        deaths = f"{deaths:,}"
        affected = f"{affected}%"
        
        
        return title_county,cases,deaths,affected,fig,fig_death,fig_cases_gender,fig_deaths_gender