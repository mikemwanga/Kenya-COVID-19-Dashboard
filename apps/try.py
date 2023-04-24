import dash
from dash import html,dcc, no_update
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import os
from utils import *
from datetime import timedelta

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])


def load_data():
    #Load datasets
    daily_updates_moh =  pd.read_excel("../data/daily_updates_metadata.xlsx")
    county_daily_updates = pd.read_excel("../data/county_daily_updates.xlsx", parse_dates=["Date"], index_col='Date')
    data = pd.read_csv("../data/cases_per_county.csv")
    data["percentage_cases"] = round(data["cases"]/data["cases"].sum() * 100,2)
    county_prevalence = pd.read_csv("../data/cases_per_county.csv")
    daily_cases = pd.read_csv("../data/covid_daily_data.csv")
    daily_cases["Date"] = pd.to_datetime(daily_cases["Date"],format = "%d/%m/%Y")
    age_gender_data = pd.read_table("../data/age_gender_data.txt",sep = "\t")
    
    return daily_updates_moh, county_daily_updates, data, county_prevalence,daily_cases,age_gender_data


app.layout = html.Div([
            
    html.Div(id = "home-content"),
    
    dcc.Interval(
            id='interval',
            interval= 43200 * 1000, # in milliseconds update every 24 hrs
            n_intervals=0,
                ),
])

@app.callback(
        Output("home-content","children"),
        Input("interval", "n_intervals")
)

def update_content(n):
    
    daily_updates_moh, county_daily_updates, data, county_prevalence,daily_cases,age_gender_data = load_data()
    
    #processing the datasets
    daily_updates_moh.set_index("Date", inplace=True)
    new_cases_last_24hrs = daily_updates_moh["new_cases_last_24_hrs"].dropna().iat[-1]
    previous_case = daily_updates_moh["new_cases_last_24_hrs"].dropna().iat[-2]
    case_fold_change = (new_cases_last_24hrs/previous_case) - 1

    total_cases_last_7  = daily_updates_moh["new_cases_last_24_hrs"].dropna().iloc[-7:].sum()

    samplesize_last_24hrs = daily_updates_moh["sample_size_last_24_hrs"].dropna().iat[-1]
    samplesize_previous = daily_updates_moh["sample_size_last_24_hrs"].dropna().iat[-2]

    total_samples_last_7 = daily_updates_moh["sample_size_last_24_hrs"].iloc[-7:].sum()
    posity_last_24 = round((new_cases_last_24hrs/samplesize_last_24hrs)*100,1)
    previous_positivity = round((previous_case/samplesize_previous)*100,1)

    posity_last_7 = round((total_cases_last_7/total_samples_last_7)* 100,1)

    fatalities_last_24 = daily_updates_moh["recorded_deaths_last_24_hrs"].iat[-1]
    fatalities_last_7 = daily_updates_moh["recorded_deaths_last_24_hrs"].iloc[-7:].sum()
    fatalities_previous = daily_updates_moh["recorded_deaths_last_24_hrs"].iat[-2]


    recoveries_last_24 = daily_updates_moh["recoveries_last_24_hrs"].dropna().iat[-1]
    recoveries_previous = daily_updates_moh["recoveries_last_24_hrs"].dropna().iat[-2]

    recoveries_last_7 = daily_updates_moh["recoveries_last_24_hrs"].dropna().iloc[-7:].sum()

    total_cases = daily_updates_moh["total_confirmed_cases"].dropna().iat[-1]
    total_tests =  daily_updates_moh["cumulative_tests"].dropna().iat[-1]
    total_deaths = daily_updates_moh["cumulative_fatalities"].dropna().iat[-1]
    total_recoveries = daily_updates_moh["total_recoveries"].dropna().iat[-1]
    proportion_fully_vaccntd_adults = daily_updates_moh["proportion_of_fully_vaccinated_adult_population"].dropna().iat[-1]

    overall_positivity = round(total_cases/total_tests*100,1)
    #update_date = datetime.date.today().strftime("%B %d, %Y")
    update_date = daily_updates_moh.index[-1].strftime("%B %d, %Y")

    ##Plots
    last_7 = daily_updates_moh[["new_cases_last_24_hrs","positivity_rate_last_24_hrs"]].iloc[-7:].reset_index()
    fig_7days = px.line(last_7,x = "Date",y ="new_cases_last_24_hrs", hover_data={"Date":"|%B %d"})
    fig_7days.update_layout(width=450,height=350, hovermode = "x unified",plot_bgcolor = pcolor,paper_bgcolor = pcolor)
    fig_7days.update_yaxes(title = "cases",linecolor = "black")
    fig_7days.update_xaxes(linecolor = "black",ticks="outside",nticks = 7)
    fig_7days.update_traces(line_color = markercolor)

    fig_7_positivity = px.line(last_7,x = "Date",y ="positivity_rate_last_24_hrs", hover_data={"Date":"|%B %d"})
    fig_7_positivity.update_layout(width=450,height=350, hovermode = "x unified",plot_bgcolor = pcolor,paper_bgcolor = pcolor)
    fig_7_positivity.update_yaxes(title = "Positivity(%)",linecolor = "black")
    fig_7_positivity.update_xaxes(linecolor = "black",ticks="outside",nticks = 7)
    fig_7_positivity.update_traces(line_color = markercolor)

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


    county_daily_updates.fillna(0, inplace = True)
    county_total_cases =  pd.DataFrame(county_daily_updates.sum(axis=0).reset_index()).rename(columns = {"index":"county",0:"Freq"})
    county_plot = px.bar(county_total_cases.sort_values("Freq", ascending=True).tail(n=8), y = "county", 
                         x = "Freq",#orientation = "h",
                         color_discrete_sequence=[markercolor], text_auto=True,)

    county_plot.update_traces(textposition = "outside", textfont_size=7,cliponaxis=True,width=0.6)
    county_plot.update_layout(plot_bgcolor = pcolor_home,paper_bgcolor = pcolor_home,xaxis_title = None,
                              margin = margin)
    county_plot.update_yaxes(title = None, linecolor = "black",title_font = {"size":titlefont},
                             tickfont = dict(size=tickfont))
    county_plot.update_xaxes(linecolor = "black",tickfont = dict(size=tickfont),title = "Frequency",
                             title_font = {"size":tickfont})


    #trends in kenya plot cases
    def daily_plots(observation1, observation2):
            fig = go.Figure()
            fig.add_trace(go.Scatter( x = daily_cases["Date"],mode='none', y = daily_cases[observation1]))
            fig.add_trace(go.Scatter(x = daily_cases["Date"], y = daily_cases[observation2]))
            fig.update_layout(hovermode="x unified",showlegend=False,margin = margin)
            fig.update_xaxes(showgrid=False,showline=True,linecolor = axis_color,tickfont = dict(size=tickfont))
            fig.update_yaxes(tickfont = dict(size=tickfont),nticks=10,title = "7-day Average", title_font = {"size":titlefont})
            return fig

    cases_trend = daily_plots("Reported_Cases","moving_average_cases") #plot of daily reported infections
    deaths_trends = daily_plots("death_cases","moving_average_deaths")

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
        age_gender_cases_plot.update_xaxes(tickfont = dict(size=tickfont),title = None,title_font = {"size":titlefont} )
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
        age_gender_death_plot.update_xaxes(tickfont = dict(size=tickfont),title = None,title_font = {"size":titlefont})
        age_gender_death_plot.update_traces(width=0.6)

        total_female_cases = data["Female_cases"].sum()
        total_male_cases = data["Male_cases"].sum()
        perc_female_cases = total_female_cases/(total_female_cases + total_male_cases)
        perc_male_cases = total_male_cases/(total_female_cases + total_male_cases)

        total_female_death = data["Female_deaths"].sum()
        total_male_death = data["Male_deaths"].sum()
        perc_female_deaths = total_female_death/(total_female_death+total_male_death )
        perc_male_deaths = total_male_death/(total_female_death+total_male_death )

        return age_gender_cases_plot,age_gender_death_plot,total_female_cases, total_male_cases, perc_female_cases,\
            perc_male_cases,total_female_death,total_male_death,perc_female_deaths,perc_male_deaths

    age_gender_cases_plot,age_gender_death_plot,total_female_cases, total_male_cases, perc_female_cases,perc_male_cases,total_female_death,\
        total_male_death,perc_female_deaths,perc_male_deaths  = age_gender_plots2(age_gender_data)
    
    #function to caculate fold change
    class fold_change:
        def __init__(self):
            #classname components
            self.up_fold = "fs-6 text-danger bg-danger bg-opacity-10"
            self.down_fold = "fs-6 text-success bg-success bg-opacity-10"
            self.no_change_fold = "fs-6 text-dark bg-dark bg-opacity-10"
            #arrow to be returned
            self.up_arrow = DashIconify(icon="material-symbols:arrow-circle-up-rounded",width=20,color="red",height=25)#
            self.down_arrow = DashIconify(icon="material-symbols:arrow-circle-down-rounded",width=25,color="green",height=25)

            self.no_change = DashIconify(id="no_change",icon="ic:baseline-indeterminate-check-box",width=25,color="black",height=25)

            self.rec_up_arrow = DashIconify(icon="material-symbols:arrow-circle-up-rounded",width=25,color="green",height=25)#
            self.rec_down_arrow = DashIconify(icon="material-symbols:arrow-circle-down-rounded",width=25,color="red",height=25)#


        def case_fold_change(self):
            case_fold_value = round((new_cases_last_24hrs/previous_case)-1,1)
            if case_fold_value > 0:
                return case_fold_value,self.up_arrow,self.up_fold
            elif case_fold_value == 0:
                return case_fold_value,self.no_change,self.no_change_fold
            else:
                return case_fold_value,self.down_arrow, self.down_fold

        def pos_change(self):
            pos_change = round((posity_last_24/previous_positivity)-1,1)
            if pos_change >0:
                return pos_change,self.up_arrow,self.up_fold
            elif pos_change == 0:
                return pos_change,self.no_change,self.no_change_fold
            else:
                return pos_change,self.down_arrow, self.down_fold
        def recoveries_change(self):
            rec_change = round((recoveries_last_24/recoveries_previous)-1,1)
            if rec_change >0:
                return rec_change,self.rec_up_arrow,self.down_fold
            elif rec_change == 0:
                return rec_change,self.no_change,self.no_change_fold
            else:
                return rec_change,self.rec_down_arrow, self.up_fold

        def fatality_change(self):
            fat_change = round((fatalities_last_24/fatalities_previous)-1,1)
            if fat_change > 0:
                return fat_change,self.up_arrow,self.up_fold
            elif fat_change == 0:
                return fat_change,self.no_change,self.no_change_fold
            else:
                return fat_change,self.down_arrow,self.down_fold

    cases_fold_value,arrow_type,fold_change_class = fold_change().case_fold_change()
    pos_fold_value,pos_arrow_type,pos_fold_change_class =fold_change().pos_change()
    rec_fold_value,rec_arrow_type,rec_fold_change_class = fold_change().recoveries_change()
    fat_fold_value,fat_arrow_type,fat_fold_change_class  =fold_change().fatality_change()
    
    dev = html.Div([
    		dbc.Row([
                    dbc.Col([
                        html.P(f"{update_date}", className = "text-end text-primary", style = {"font-size":12}), #{update_date}
                        html.P("This dashboard allows a visualization of COVID-19 disease trends in cases, fatalities, vaccination and variant diversity. \
                        This platform intergrates data from Ministry of Health of Republic of Kenya, GISAID and other SARS-CoV-2 associated studies.",
                        className = "fs-6",style ={"text-align":"start"}),
                        html.Hr(),
                    ], width = 11, lg=10),
                ],justify="center", className = "mb-2 ms-3 me-3 ps-3 pe-3 mt-5 pt-5"),
      
      
            dbc.Row([
                    dbc.Col([
                        dbc.CardBody([
                            html.Label(f"{int(total_cases):,}",className ="text-danger fs-3"),
                            html.P("Total reported cases",style = style_text)
                        ],className = card_class )
                    ],xs=5,md=3,lg=2,className = "card_style",style = {"margin-right":"10px"}),
                    
                    dbc.Col([
                        dbc.CardBody([
                            html.Label(f"{int(total_deaths):,}",className ="text-dark fs-3"),
                            html.P("Total reported deaths",style = style_text),
                       ],className = card_class)
                    ],xs=5,md=3,lg=2,className = "card_style",style = {"margin-right":"10px"}),
                    
                    dbc.Col([
                        dbc.CardBody([
                            html.Label(f"{int(total_recoveries):,}",className = "text-success fs-3"),
                            html.P("Total recoveries",style = style_text),
                       ],className = card_class)
                    ],xs=5,md=3,lg=2,className = "card_style",style = {"margin-right":"10px"}),
                    
                    dbc.Col([
                        dbc.CardBody([
                            html.Label(f"{int(total_tests):,}",className = "text-primary fs-3"),
                            html.P("Tests done",style = style_text),
                       ],className = card_class)
                    ],xs=5,md=3,lg=2,className = "card_style"),
                    
                    dbc.Col([
                        dbc.CardBody([
                            html.Strong(f"{overall_positivity}",className = "text-info fs-3"),html.Span(children="%",className = "text-info fs-4"), 
                            html.P("Overall Positivity",style = style_text),
                        ],className = card_class)
                    ],xs=5,md=3,lg=2,className = "card_style",style = {"margin-left":"10px"})
                    
                ],justify="center",className = classname_col,align = "center"),

                dbc.Row([
                    dbc.Col([
                        html.P(f"Updates: Last 24hrs of: {update_date}",className = "text-black fs-6 fw-bold ms-1"),
                        html.Hr(className =hr_class,style=hr_style),
                                html.H6("Cases",className=col1_class),
                                html.Hr(className = col1_class,style = {"width":"50%"}),
                                html.Strong(new_cases_last_24hrs,className = val_class),
                                html.Span(children = [arrow_type,cases_fold_value],className = fold_change_class,
                                          style = {"margin-left":"20px"}),
                        html.Hr(className =hr_class,style=hr_style),
                                html.H6("Positivity",className=col1_class),
                                html.Hr(className=col1_class,style = {"width":"50%"}),
                                html.Strong(f"{posity_last_24}%",className = val_class),
                                html.Span(children = [pos_arrow_type,pos_fold_value],
                                          className = pos_fold_change_class,style = {"margin-left":"20px"}),
                        html.Hr(className =hr_class,style=hr_style),
                               html.H6("Fatalities",className = col1_class),
                               html.Hr(className=col1_class,style = {"width":"50%"}),
                               html.Strong(fatalities_last_24 ,className = val_class),
                               html.Span(children = [fat_arrow_type, fat_fold_value],className = fat_fold_change_class,
                                         style = {"margin-left":"20px"}),
                        html.Hr(className =hr_class,style=hr_style),
                                html.H6("Recoveries",className = col1_class),
                                html.Hr(className = col1_class,style = {"width":"50%"}),
                                html.Strong(recoveries_last_24,className = val_class),
                                html.Span(children = [rec_arrow_type, rec_fold_value],className = rec_fold_change_class,
                                          style = {"margin-left":"20px"}),
                        html.Hr(className =hr_class,style=hr_style),
                                html.H6("Samples Tested",className = col1_class),
                                html.Hr(className = col1_class,style = {"width":"50%"}),
                                html.Strong(samplesize_last_24hrs,className = val_class),
                        html.Hr()
                        
                    ],xs=10,md=1,lg=2,className = col_class,style = {"height":"1000px"}),
                    
                    dbc.Col([
                                               
                       html.P("Counties with recently reported cases",className = col_title),
                       dcc.Graph(figure = fig_county,responsive = True, style = {"width":"30hw","height":"25vh"}),
                       html.Hr(className = hr_class, style = hr_style),
                               
                       html.P("Trends in Cases since beginning of pandemic",className = col_title),
                       dcc.Graph(figure=cases_trend,responsive = True, style = {"width":"30hw","height":"25vh"}),
                      
                       html.Hr(className = hr_class, style = hr_style),
                       html.P("Cases by Gender and age",className = col_title),
                       dcc.Graph(figure = age_gender_cases_plot,responsive = True,style = {"width":"25hw","height":"30vh"})#,style = {"width":"30hw","height":"35vh"})
                       
                    ],xs=10,md=4,lg=4,className = col_class,style = {"margin-left":"15px","margin-right":"0px","height":"1000px"} ),
                    
                    dbc.Col([
                        html.P("Most affected counties",className = col_title),
                        dcc.Graph(figure = affected_counties, responsive = True, style = {"width":"32hw","height":"25vh"}),
                        html.Hr(className = hr_class, style = hr_style),
                        html.P("Trends in fatalities since beginning of pandemic",className = col_title),
                        dcc.Graph(figure = deaths_trends,responsive = True, style = {"width":"30hw","height":"25vh"}),
                        
                        html.Hr(className = hr_class, style = hr_style),
                        html.P("Fatalities by Gender and age",className = col_title),
                        dcc.Graph(figure= age_gender_death_plot, responsive = True, style = {"width":"25hw","height":"30vh"}),# style = {"width":"30vw","height":"30vh"})
                    ],xs=10,md=4,lg=4,className = col_class,style = {"margin-left":"15px","margin-right":"0px","height":"1000px"}),
                    
                ],className = classname_col,style = {},justify = "center"),
      
        ]   )
    
    return dev
    
    
    
if __name__ == '__main__':
     app.run_server(debug=True)