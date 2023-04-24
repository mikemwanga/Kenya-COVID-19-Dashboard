from utils import *
from plotly.subplots import make_subplots
from apps import home as hm

sero_data = pd.read_excel(DATA_PATH.joinpath("KWTRP_serosurveillance_data_Dashboard_09Sep2022.xlsx"))
daily_cases = pd.read_csv(DATA_PATH.joinpath("covid_daily_data.csv"))
daily_cases["Date"] = pd.to_datetime(daily_cases["Date"],format = "%d/%m/%Y")


legend = dict(orientation = "h",title=None,yanchor  = "top", xanchor = "left",y=1.2,
                                                    font = dict(size=9))
class sero_prevalence:
        def __init__(self):
                sero_data["Period"] = sero_data[["Month(s)", "Year"]].astype(str).agg(" ".join, axis=1)
                data = sero_data[["Population","Region", "start","finish", "Anti-spike_perc"]]
                self.data_period = data.groupby(["start","finish","Population",])["Anti-spike_perc"].mean()
                self.data_period = self.data_period.to_frame().reset_index()
                self.data_period["start"] = pd.to_datetime(self.data_period["start"])
                self.data_period["finish"] = pd.to_datetime(self.data_period["finish"])

        def seroplot(self):
                fig = make_subplots(specs = [[{"secondary_y":True}]], shared_xaxes=True)
                line_fig = px.timeline(self.data_period, x_start="start", x_end = "finish", y = "Anti-spike_perc", color = "Population", 
                                        hover_name="Population", range_y = [0,1], hover_data={"Population":False, "Anti-spike_perc":":0%"}, 
                                        color_discrete_sequence= color_patterns )
                line_fig.update_traces(width=0.02, type = "bar", textposition = "outside")
                cum_fig = px.line(daily_cases, x = "Date",  y = "Cum_Cases", color_discrete_sequence=[markercolor]) 
                cum_fig.update_traces(yaxis="y2")
                fig.add_traces(cum_fig.data + line_fig.data)
                fig.update_yaxes(title_font = {"size":titlefont},title_text = "Cumulative Cases",ticks="outside", 
                                 secondary_y = True, tickfont = tickfont_dict,
                                 linecolor = "black")
                fig.update_yaxes(title_font = {"size":titlefont},title_text = "Average % Anti IgG seroprevalence",
                                 linecolor = "black",ticks="outside",col=1,nticks=20,
                                 secondary_y = False,range = [0,1],tickfont =tickfont_dict )#,gridcolor = gridcolor
                fig.update_xaxes(title_font = {"size":titlefont},tickfont = tickfont_dict,dtick="M1",tickformat="%b\n%Y",
                                 linecolor = "black",ticks="outside",nticks=5)#tickformat="%b\n%Y"
                fig.update_layout(margin=margin,
                                  legend = dict(orientation = "h",yanchor  = "bottom", xanchor = "left",y=-0.25))#y=1.02,x=0.01,xanchor="left"))
                #fig.update_layout(legend = dict(yanchor  = "top",y=1,x=0.01,xanchor="left"),legend_orientation ="h",margin = margin) #plot_bgcolor = pcolor,paper_bgcolor = pcolor,
                
                return fig

        def population_plot(self, population):
                self.population = population
                fig = make_subplots(specs = [[{"secondary_y":True}]], shared_xaxes=True)
                pop_data = self.data_period[self.data_period["Population"] == population]
                line_fig = px.timeline(pop_data, x_start="start", x_end = "finish", y = "Anti-spike_perc", color = "Population", 
                    hover_name="Population", range_y = [0,1], hover_data={"Population":False, "Anti-spike_perc":":0%"}, 
                    color_discrete_sequence= color_patterns)
                line_fig.update_traces(width=0.02, type = "bar", textposition = "outside")
                cum_fig = px.line(daily_cases, x = "Date",  y = "Cum_Cases",color_discrete_sequence=[markercolor])# color_discrete_sequence=['black',"red"]) 
                cum_fig.update_traces(yaxis="y2")
                fig.add_traces(cum_fig.data + line_fig.data)
                fig.update_yaxes(title_font = {"size":titlefont},tickfont = tickfont_dict,title_text = "cumulative cases", 
                                 linecolor = "black", secondary_y = True, range = [0,400000],nticks=10)
                fig.update_yaxes(title_font = {"size":titlefont},tickfont = tickfont_dict,title_text = "seroprevalence",
                                 linecolor = "black",ticks="outside",col=1,
                                 nticks=10,secondary_y = False,range = [0,1]) #,gridcolor = gridcolor
                fig.update_xaxes(tickfont = tickfont_dict,dtick="M1",tickformat="%b\n%Y",linecolor = "black",ticks="outside")#,nticks = 20)
                fig.update_layout(margin = margin,showlegend=False)#legend_orientation ="h")
                return fig
sero_class = sero_prevalence()           
subfig = sero_class.seroplot()


layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.H5("Visualization of Seroprevalence across the country", style ={"text-align":"start"}),
        ], width = 6, lg=7),
        dbc.Col([
            html.Div([
                html.P("Select Population",className="text-primary mb-0 pb-0", style= {"font-size":14}),
                dcc.Dropdown(
                    id = "population",
                    options = ["Overall","Blood Donors","Health Workers","HDSS Residents"],#"ANC Attendees"],
                    value = "Overall", 
                )
            ],style={"width":"100%","font-size":14})
        ],width=4, lg=3,className = "me-5 pe-5"),
        html.Hr(),
    ],justify="center",className ="mt-5 pt-5 ms-5 me-5"),# className = "mb-2 ms-4 me-1 ps-4 pe-1 mt-5 pt-5"),
    #returning content here
    html.Div(id = "content"),
    hm.reference
],className =  "bg-light bg-opacity-20"),

class hdss_residents_strat:
        """
        Returns population-based plots relative to Age of the studied group, gender (Male/Female) and regions.

        """
        def __init__(self):
                
                self.data = sero_data[sero_data["Population"] == "HDSS residents"]
                
                self.hdss_region =  self.data.loc[(self.data["Age in years"] == "16 - 65") & (self.data["Sex"] == "All")]

        def age_plot(self):
                age_data = self.data[self.data["Age in years"].isin(["<16","16 - 24","25 - 34", "35 - 44","45 - 54","55 - 64","≥65"])]
                age_fig = px.timeline(age_data, x_start="start", x_end = "finish", y = "Anti-spike_perc", color = "Age in years", 
                                        color_discrete_sequence= color_patterns,hover_name="Age in years", range_y = [0,.6], 
                                        hover_data={"Anti-spike_perc":":0%"})
                age_fig.update_layout(title = None,margin=margin,
                                      legend = legend)
                age_fig.update_xaxes(title_font = {"size":titlefont},tickfont = tickfont_dict, dtick="M1",tickformat="%b\n%Y",
                                     linecolor = "black",ticks="outside")
                age_fig.update_yaxes(title_font = {"size":titlefont},tickfont = tickfont_dict,gridcolor = gridcolor,
                                     title_text = "seroprevalence",linecolor = "black",ticks="outside")
                return age_fig
        def gender_plot(self):
                gender_data = self.data[self.data["Sex"].isin(["Female","Male"])]
                gender_fig = px.timeline(gender_data, x_start="start", x_end = "finish", y = "Anti-spike_perc", color = "Sex", 
                                        hover_name="Sex", range_y = [0,.6], hover_data={"Anti-spike_perc":":0%"})
                gender_fig.update_layout(title = None,margin=margin,legend=legend)
                gender_fig.update_xaxes(title_font = {"size":titlefont},tickfont = tickfont_dict,dtick="M1",tickformat="%b\n%Y",
                                        linecolor = "black",ticks="outside")
                gender_fig.update_yaxes(title_font = {"size":titlefont},tickfont = tickfont_dict,gridcolor = gridcolor,
                                        title_text = "seroprevalence",linecolor = "black",ticks="outside")
                return gender_fig
        
        def region_plot(self):
                #region_data = self.data.loc[(self.data["Age in years"] == "16 - 65")] # & (self.data["Sex"]=="All")
                region_fig = px.timeline(self.hdss_region, x_start="start", x_end = "finish", y = "Anti-spike_perc", color = "Region", 
                                        hover_name="Region",range_y = [0,.9],  hover_data={"Anti-spike_perc":":0%"}) #range_y = [0,0.3],
                region_fig.update_layout(title = None,margin=margin,legend=legend)
                region_fig.update_traces(width = 0.003)
                region_fig.update_xaxes(title_font = {"size":titlefont},tickfont = tickfont_dict,dtick="M1",tickformat="%b\n%Y",
                                        linecolor = "black",ticks="outside")
                region_fig.update_yaxes(title_font = {"size":titlefont},tickfont = tickfont_dict,gridcolor = gridcolor,
                                        title_text = "seroprevalence",linecolor = "black",ticks="outside")
                return region_fig


class blood_donor_strat:
        """
        Returns population-based plots relative to Age of the studied group, gender (Male/Female) and regions.

        """
        def __init__(self):
                
                self.data = sero_data[sero_data["Population"] == "Blood donors"]

        def age_plot(self):
                age_data = self.data[self.data["Age in years"].isin(["15 - 24","25 - 34", "35 - 44","45 - 54","55 - 64"])]
                age_fig = px.timeline(age_data, x_start="start", x_end = "finish", y = "Anti-spike_perc", color = "Age in years", 
                                        color_discrete_sequence= color_patterns,hover_name="Age in years", range_y = [0,.6], 
                                        hover_data={"Anti-spike_perc":":0%"})
                age_fig.update_layout(title = None,margin=margin,
                                      legend = legend)
                age_fig.update_xaxes(title_font = {"size":titlefont},tickfont = tickfont_dict, dtick="M1",tickformat="%b\n%Y",
                                     linecolor = "black",ticks="outside")
                age_fig.update_yaxes(title_font = {"size":titlefont},tickfont = tickfont_dict,gridcolor = gridcolor,
                                     title_text = "seroprevalence",linecolor = "black",ticks="outside")
                return age_fig
        
        def gender_plot(self):
                gender_data = self.data[self.data["Sex"].isin(["Female","Male"])]
                gender_fig = px.timeline(gender_data, x_start="start", x_end = "finish", y = "Anti-spike_perc", color = "Sex", 
                                        hover_name="Sex", range_y = [0,.6], hover_data={"Anti-spike_perc":":0%"})
                gender_fig.update_layout(title = None,margin=margin,legend=legend)
                gender_fig.update_xaxes(title_font = {"size":titlefont},tickfont = tickfont_dict,dtick="M1",tickformat="%b\n%Y",
                                        linecolor = "black",ticks="outside")
                gender_fig.update_yaxes(title_font = {"size":titlefont},tickfont = tickfont_dict,gridcolor = gridcolor,
                                        title_text = "seroprevalence",linecolor = "black",ticks="outside")
                return gender_fig
        def region_plot(self):
                region_data = self.data.loc[(self.data["Age in years"] == "15 - 64") & (self.data["Sex"]=="All")]
                region_fig = px.timeline(region_data, x_start="start", x_end = "finish", y = "Anti-spike_perc", color = "Region", 
                                        hover_name="Region", range_y = [0,0.3], hover_data={"Anti-spike_perc":":0%"})
                region_fig.update_layout(title = None,margin=margin,legend=legend)
                region_fig.update_traces(width = 0.003)
                region_fig.update_xaxes(title_font = {"size":titlefont},tickfont = tickfont_dict,dtick="M1",tickformat="%b\n%Y",
                                        linecolor = "black",ticks="outside")
                region_fig.update_yaxes(title_font = {"size":titlefont},tickfont = tickfont_dict,gridcolor = gridcolor,
                                        title_text = "seroprevalence",linecolor = "black",ticks="outside")
                return region_fig

class health_workers_strat:
    """
    Returns population-based plots relative to Age of the health workers group, gender (Male/Female) and regions.
    """
    def __init__(self):
        health_workers = sero_data[sero_data["Population"] == "Health workers"]
        self.health_workers_age = health_workers[health_workers["Age in years"].isin(["18 - 30","31 - 40", "41 - 50","51 - 60"])]
        self.health_workers_gender = health_workers[health_workers["Sex"].isin(["Male","Female"])]
        self.health_workers_region =  health_workers.loc[(health_workers["Sex"] == "All") & (health_workers["Age in years"] == "≥18") ]
    
    def age_plot(self):
        fig=px.timeline(self.health_workers_age, x_start="start", x_end = "finish", y = "Anti-spike_perc", color = "Age in years", 
                                                hover_name="Age in years",range_x = ["2020-06-01", "2021-07-01"], 
                                                range_y = [0,.3], hover_data={"Anti-spike_perc":":0%"})
        fig.update_traces(width=0.01)
        fig.update_layout(title = None,margin=margin, legend = legend)
        fig.update_xaxes(title_font = {"size":titlefont},tickfont = tickfont_dict,dtick="M1",tickformat="%b\n%Y",linecolor = "black",ticks="outside")
        fig.update_yaxes(title_font = {"size":titlefont},tickfont = tickfont_dict,gridcolor = gridcolor,title_text = "seroprevalence",linecolor = "black",ticks="outside")
        return fig

    def gender_plot(self):
        fig=px.timeline(self.health_workers_gender, x_start="start", x_end = "finish", y = "Anti-spike_perc", color = "Sex", 
                                                hover_name="Sex",range_x = ["2020-06-01", "2021-07-01"], 
                                                range_y = [0,.3], hover_data={"Anti-spike_perc":":0%"})
        fig.update_traces(width=0.01)
        fig.update_layout(title = None,margin=margin,legend = legend)
        fig.update_xaxes(title_font = {"size":titlefont},tickfont = tickfont_dict,dtick="M1",tickformat="%b\n%Y",linecolor = "black",ticks="outside")
        fig.update_yaxes(title_font = {"size":titlefont},gridcolor = gridcolor,tickfont = tickfont_dict,title_text = "seroprevalence",linecolor = "black",ticks="outside")
        return fig

    def region_plot(self):
        fig=px.timeline(self.health_workers_region, x_start="start", x_end = "finish", y = "Anti-spike_perc", color = "Region", 
                                                hover_name="Region",range_x = ["2020-06-01", "2021-02-01"], 
                                                range_y = [0,.6], hover_data={"Anti-spike_perc":":0%"})
        fig.update_traces(width=0.01)
        fig.update_layout(title = None,margin=margin,legend=legend)
        fig.update_xaxes(title_font = {"size":titlefont},tickfont = tickfont_dict,dtick="M1",tickformat="%b\n%Y",linecolor = "black",ticks="outside")
        fig.update_yaxes(title_font = {"size":titlefont},gridcolor = gridcolor,title_text = "seroprevalence",linecolor = "black",ticks="outside")

        return fig


overall_image = html.Div([
    dbc.Row([
        #dbc.Col([],width=2),
        dbc.Col([
            dcc.Graph(figure = subfig,responsive = True,className = "ms-3",style = {"width":"800px","height":"400px"})
            
        ],width = 8, lg = 7, style = {"margin-right":"30px"}),
        #dbc.Col([],width=2),
    ],justify = "center")
])

blood_donors_plot = html.Div([
            dbc.Row([
                
                dbc.Col([
                    html.Br(),
                    html.P("Overall Seroprevalence",className = col_title),
                    dcc.Graph(figure = sero_class.population_plot("Blood donors"),responsive = True, style ={"height":"40vh"}),
                    html.Hr(),
                    html.P("Seroprevalence by gender",className = col_title),
                    dcc.Graph(figure = blood_donor_strat().gender_plot(),responsive = True, style={"height":"40vh"})
                
                ],xs=8,md=5,xl=4,className = col_class,style = {"margin-right":"10px"}),
            
                dbc.Col([
                    html.Br(),
                    html.P("Seroprevalence by age",className = col_title),
                    dcc.Graph(figure = blood_donor_strat().age_plot(),responsive = True, style={"height":"40vh"}),
                    html.Hr(),
                    html.P("Seroprevalence in by region",className = col_title),
                    dcc.Graph(figure = blood_donor_strat().region_plot(),responsive = True, style={"height":"40vh"})
                ],xs=8,md=5,xl=4,className = col_class)
                
            ],justify = "center",className = classname_col)
        ])

health_care_workers = html.Div([
            dbc.Row([
                
                dbc.Col([
                    html.Br(),
                    html.P("Overall Seroprevalence",className = col_title),
                    dcc.Graph(figure = sero_class.population_plot("Health workers"),responsive = True, style ={"height":"40vh"}),
                    html.Hr(),
                    html.P("Seroprevalence by gender",className = col_title),
                    dcc.Graph(figure = health_workers_strat().gender_plot(),responsive = True, style={"height":"40vh"})
                
                ],xs=8,md=5,xl=4,className = col_class,style = {"margin-right":"10px"}),
            
                dbc.Col([
                    html.Br(),
                    html.P("Seroprevalence by age",className = col_title),
                    dcc.Graph(figure = health_workers_strat().age_plot(),responsive = True, style={"height":"40vh"}),
                    html.Hr(),
                    html.P("Seroprevalence in by region",className = col_title),
                    dcc.Graph(figure = health_workers_strat().region_plot(),responsive = True, style={"height":"40vh"})
                ],xs=8,md=5,xl=4,className = col_class)
                
            ],justify = "center",className = classname_col)
        ]),


hdss_residents = html.Div([
        dbc.Row([
            
            dbc.Col([
                    html.Br(),
                    html.P("Overall Seroprevalence",className = col_title),
                    dcc.Graph(figure = sero_class.population_plot("HDSS residents"),responsive = True, style ={"height":"40vh"}),
                    html.Hr(),
                    html.P("Seroprevalence by gender",className = col_title),
                    dcc.Graph(figure = hdss_residents_strat().gender_plot(),responsive = True, style={"height":"40vh"})
                
                ],xs=8,md=5,xl=4,className = col_class,style = {"margin-right":"10px"}),
            
            dbc.Col([
                html.Br(),
                    html.P("Seroprevalence by age",className = col_title),
                    dcc.Graph(figure = hdss_residents_strat().age_plot(),responsive = True, style={"height":"40vh"}),
                    html.Hr(),
                    html.P("Seroprevalence in by region",className = col_title),
                    dcc.Graph(figure = hdss_residents_strat().region_plot(),responsive = True, style={"height":"40vh"})
                    
            ],xs=8,md=5,xl=4,className = col_class)        
        ],justify = "center",className = classname_col)
])

@app.callback(
    Output("content", "children"), 
    Input("population","value")
)

def render_content(value):
    if value == "Overall":
        return overall_image
    elif value == "Blood Donors":
        return blood_donors_plot
    elif value == "Health Workers":
        return health_care_workers
    elif value == "HDSS Residents":
        return hdss_residents
    else:
        return overall_image