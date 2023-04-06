from utils import *
from apps import variant_trends as vt

daily_updates_moh =  pd.read_excel(hm.DATA_PATH.joinpath("daily_updates_metadata.xlsx"))
total_vaccines = daily_updates_moh["total_vaccines_received"].dropna().iat[-1]
fully_vaccinated_adults= daily_updates_moh["fully_vaccinated_adult_population"].dropna().iat[-1]
partially_vaccinated_adults= daily_updates_moh["partially_vaccinated_adult_population"].dropna().iat[-1]
booster_doses = daily_updates_moh["Booster_doses"].dropna().iat[-1]
perc_vaccinated = round(daily_updates_moh["proportion_of_fully_vaccinated_adult_population"].dropna().iat[-1],1)
total_doses_administered = daily_updates_moh["total_doses_administered"].dropna().iat[-1]

values = [["Total Vaccines received",total_vaccines],
          ["Total doses administered",total_doses_administered],
          ["Fully vaccinated adults",fully_vaccinated_adults],
          ["Partially vaccinated adults",partially_vaccinated_adults],
          ["Total booster doses",booster_doses],
          ["Percentage vaccinated",perc_vaccinated]]

vaccination_data = pd.DataFrame(values,columns=["Vaccine","Doses Administered"])
vaccination_data["Doses Administered"] = vaccination_data["Doses Administered"].astype(int)

vaccination_data_dict = vaccination_data.to_dict('rows')
columns =  [{"name": i, "id": i,} for i in (vaccination_data.columns)]

vaccine_table = dt.DataTable(vaccination_data_dict, columns=columns)



variant_data = pd.read_table(hm.DATA_PATH.joinpath("variant_month_data.txt"))
#average_df_clean = pd.read_csv(hm.DATA_PATH.joinpath("average_weekly_submission_to_gsaid.csv"), parse_dates = ["date_sampled"])
variants_kenya = pd.read_table(hm.DATA_PATH.joinpath("variant_data_kenya.tsv"))
variants_kenya["Month"] = pd.to_datetime(variants_kenya["Month"], format = "%Y-%m-%d")

fig_var = px.bar(variants_kenya, x = "Month", y = "percentage", color="variant",range_x=["2020-01-01","2023-01-12"],
                 color_discrete_sequence = ["#1b9e77","#d95f02","#7570b3","#e7298a","#8111A5","#e6ab02","#a6761d"])
#fig_var.update_traces(textfont_size=10,textposition="outside", text = variant_values["Frequency"])
fig_var.update_xaxes(nticks = 10,linecolor = "black",ticks="outside",tickfont = dict(size=10),title = None)
fig_var.update_yaxes(linecolor = "black",ticks="outside",tickfont = dict(size=12),title ="Proportion", title_font = {"size":12})
fig_var.update_layout(legend=dict(itemsizing="constant",title = None,orientation = "h", font=dict(size=10)),plot_bgcolor = "white",
                      margin = hm.margin,paper_bgcolor = "white")


text = "Trying to download things"

content = html.Div([
    dbc.Row([
        
        dbc.Col([
            html.H3("Kenya COVID-19 Report", className = "text-center fw-bold text-decoration-underline"),#{hm.update_date}
            html.H5("1. Summary",className = "fw-bold"),
            html.P([f"COVID-19 was first reported in Kenya on March 13, 2020. As of {hm.total_cases:,}  infections and {hm.total_deaths:,} \
                have been reported. The overall positivity stands at {hm.overall_positivity}%. {hm.total_recoveries:,} have so far recovered.\
                Nairobi is the highest hit county with 41.3%, Kiambu 6.2% Mombasa 5.3% Nakuru 5.2% and Uasin Gishu 3.2% of all total reported cases \
                across the country.\
                "],
                className = "fs-6 mt-2"),
            
            dbc.Row([
                dbc.Col([
                    #html.P("Table 1", className = "fst-italic fs-6 fw-bold mb-0"),
                    dbc.CardBody([
                        html.Label(f"{hm.total_cases:,}",className ="text-danger fs-3"),
                        html.P("Total confirmed cases"),#,style = style_text),
                        html.Hr(),
                        html.Label(f"{hm.total_deaths:,}",className ="text-dark fs-3"),
                        html.P("Total confirmed deaths"),
                        html.Hr(),
                                       
                    ])
                ],width=3),
                dbc.Col([
                    #html.P(className = "fst-italic fs-6 fw-bold mb-0"),
                    dbc.CardBody([
                        html.Label(f"{hm.total_recoveries:,}",className = "text-success fs-3"),
                        html.P("Total recoveries"),
                        html.Hr(),
                        html.Label(f"{hm.overall_positivity}",className = "text-info fs-3"),
                        html.P("Overall Positivity"), 
                        html.Hr(),
                    ])    
                ],width=3),
                dbc.Col([
                    html.P("Figure 1", className = "fst-italic fs-6 fw-bold mb-0"),
                    dcc.Graph(figure = hm.affected_counties, responsive = True, style = {"width":"32vw","height":"35vh"}),
                ],width=5)
                
            ],justify = "evenly"),
            html.Hr(),
            html.H5("2. Epidemiology",className = "fw-bold"),
            html.H6("2.1 Temporal trends in cases and deaths",className = "fw-bold ms-6"),
            
            dbc.Row([
                dbc.Col([
                    html.P("Figure 2: Cases Trends", className = "fst-italic fs-6 fw-normal mb-0"),
                    dcc.Graph(figure=hm.cases_trend,responsive = True, style = {"width":"35vw","height":"25vh"}),
                    
                    html.P("Figure 3: Deaths Trends", className = "fst-italic fs-6 fw-normal mb-0"),
                    dcc.Graph(figure = hm.deaths_trends,responsive = True, style = {"width":"35vw","height":"25vh"}),
                ],width=7),
                dbc.Col([
                    html.P("Figure 2 on the left shows temporal trends of COVID-19 confirmed cases in Kenya. As of October 2022, Kenya\
                        had experienced atleast 6 waves of COVID-19. Figure 3 shows temporal trends in fatalaties from COVID-19 disease.", 
                    className = "fs-6 mt-5 pt-5")
                ],width=5)
             
            ],justify="evenly"),
            
            html.Br(),
            html.H6("2.2 Distribution of cases and deaths by age and sex",className = "fw-bold"),
            html.P(f"A total of {hm.total_male_cases:,} ({round(hm.perc_male_cases*100,1)}%) of the cumulative cases are male, while\
            {hm.total_female_cases:,} ({round(hm.perc_female_cases*100,1)}%) are female. Most of the cases for both male and females have \
            been observed within age gropus of 25-30, 32-35 and 36-40. Figure 4 shows distribution of the cases based on sex and gender.",
               className = "fs-6 mt-1 ms-1"),
            html.P(f"A total of {hm.total_male_death:,} ({round(hm.perc_male_deaths*100,1)}%) of the reported deaths are male, while\
            {hm.total_female_death:,} ({round(hm.perc_female_deaths*100,1)}%) are female. Most of the fatalities for both male and females have \
            been observed in the older age groups of above 40 years old. Figure 5 shows distribution of the deaths based on sex and gender.",
               className = "fs-6 mt-1 ms-1"),
            
            dbc.Row([
                dbc.Col([
                    html.P("Figure 4: Cases", className = "fst-italic fs-6 fw-normal mb-0"),
                    dcc.Graph(figure = hm.age_gender_cases_plot,responsive = True, style = {"width":"30vw","height":"30vh"})

                ], width=5),
                dbc.Col([
                    html.P("Figure 5: Deaths", className = "fst-italic fs-6 fw-normal mb-0"),
                    dcc.Graph(figure= hm.age_gender_death_plot, responsive = True, style = {"width":"30vw","height":"30vh"})
                ],width=5)
            ],justify = "evenly"),
            html.Hr(),
            
            
            html.H5("3. Vaccination",className = "fw-bold"),
            dbc.Row([
                dbc.Col([
                    html.P(f"Vaccination in Kenya was launched on March 5,2021. As of December 2021,a total of{fully_vaccinated_adults:,} adults have been full\
                    vaccinated, while {partially_vaccinated_adults:,} adults have been partially vaccinated. {booster_doses:,} individuals \
                        have received booster doses. Only {perc_vaccinated}% of adult Kenyans have been fully vaccinated."),
                ],width=5,xl=4),
                dbc.Col([
                    vaccine_table
                ],width=6,xl=5)
            ],justify = "evenly"),
            html.Hr(),
            
            
            html.H5("4. SARS-CoV-2 Variant trends",className = "fw-bold"),
            dbc.Row([
                dbc.Col([
                    html.P("Figure 5 shows temporal distribution of SARS-CoV-2 variants detected in Kenya from whole genome sequence data. As of January 2023 \
                    Omicron is the dominant circulating variant in Kenya. Omicron variant replaced the Delta variant which was in circulation up until \
                    end of 2021. Non-VOC/VOI was the dominant variant in the beginning of the pandemic which was replaced by co-circulation of Alpha and \
                    Beta variants from December 2020 to July 2021.",
                    className = "fs-6 mt-1 pt-1"),
                    
                    html.P("Figure 5: SARS-CoV-2 variants", className = "fst-italic fs-6 fw-normal mb-1"),
                    dcc.Graph(figure = vt.fig_var,responsive = True,style = {"height":"50vh", "width":"100vh"})
                ],width={"size":12,"offset":1}, xl=8),
                
            ])
            
        
        ],width=8,lg=9),
    
    
    ],justify = "center",className = "pt-5 mt-5")
])


layout = html.Div([
    content,
])



@app.callback(
    Output("download-text","data"),
    Input("btn-download","n_clicks"),
    prevent_initial_call=True
)

def download(n_clicks):
    return dict(content = text, filename = "summary.txt")