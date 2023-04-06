#layout for counties tab
from utils import *
#load dataset
data = pd.read_csv(DATA_PATH.joinpath("cases_per_county.csv"))
county_daily_data = pd.read_csv(DATA_PATH.joinpath("county_daily_data.csv"),dtype='unicode', low_memory=False)
county_daily_data["date_of_lab_confirmation"] = pd.to_datetime(county_daily_data["date_of_lab_confirmation"])
county_daily_data["Date"] = county_daily_data["date_of_lab_confirmation"]#.dt.date
county_daily_data.set_index("Date", inplace = True)

layout = html.Div([
            dbc.Spinner([
                dbc.Row([
                    dbc.Col([
                        html.H5("Visualization of trends at County level", style ={"text-align":"start"}),
                        html.Hr(),
                    ], width = 11, xxl=10),
                ],justify="center", className = "mb-2 ms-4 me-4 ps-4 pe-4 mt-5 pt-5"),
               
                
                dbc.Row([
                    dbc.Row([
                        
                        dbc.Col([
                            html.P('Select county',className ="fs-6 text-primary mb-1 pb-1"),
                            dcc.Dropdown(
                                
                                id = "county_selected",
                                 options = [
                                     {"label" : name, "value" : name} for name in county_daily_data["county"].sort_values().unique()
                                 ],
                                 value = ["Nairobi","Mombasa"],
                                 multi=True,
                                 clearable=False,
                                 style = {"width":300},
                            ),
                        ],width=4,className="me-2 mb-2"),
                    ],justify="end"),
                    
                    dbc.Col([
                        html.Br(),
                        html.P("Summary of cases, deaths and proportion of infected within the selected county.", 
                                   className="fw-bold fs-6 mt-4 text-center"),
                        html.Div(id = "table"),
                        
                        html.Br(),html.Br(),html.Br(),
                        html.Hr(),
                        html.P("Cumulative cases at the selected county",className = col_title),
                        dcc.Graph(id = "cumulative_plot", figure = {},responsive=True,style={"height":"250px"}),
                        
                        
                    ],width=5,lg=5,className = col_class,style = {"height":"700px"}),
                    
                    dbc.Col([
                        html.Br(),
                        html.P("Trends in cases at the selected county (14-days average)",
                               className="fw-bold fs-6 mt-4 text-center"),
                        dcc.Graph(id = "trends_plot", figure = {}, responsive=True,style={"height":"250px"}),
                        html.Hr(),
                        
                        html.Br(),
                        html.P("Trends in deaths at the selected county",className = col_title),
                        dcc.Graph(id = "death_plot", figure = {},responsive=True,style={"height":"250px"})
                        
                        
                    ],width=5,lg=5,className = col_class,style={"margin-left":"15px", "height":"700px"})
                    
                ],justify = "center",className = classname_col),
            
            hm.reference,
            ],type="border",color="info")
])

                
#function for 7-day moving average
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
   
@app.callback( [Output("trends_plot", "figure"),
                Output("cumulative_plot", "figure"),
                Output("death_plot","figure"),
                #Output("cases_value","children"),
                #Output("death_value","children"),
                #Output("prevalence","children"),
                Output("table","children")],
                [Input("county_selected", "value"),
                #Input("my-date-picker" , "start_date"),Input("my-date-picker" , "end_date"
                ])

def update_graph_card(county):
    if len(county) == 0:
        return dash.no_update
    else:
        data_county = county_daily_data[county_daily_data["county"].isin(county)]
        death_data = data_county[data_county["outcome"] == "Dead"] 
        #data_filter = data_filter.sort_index().loc[start_date : end_date]
        data_filter= data_county[["county","lab_results", "date_of_lab_confirmation"]].groupby(["county","date_of_lab_confirmation"]).count().reset_index()
        
        fig2 = px.line(data_filter, x="date_of_lab_confirmation" , y = data_filter["lab_results"].cumsum() , color = "county")
        fig2.update_yaxes(title =None, showline=True, linewidth = 0.1, linecolor = "gray")
        fig2.update_xaxes(title = None,linecolor = "gray", showline=True,showgrid=False)
        fig2.update_layout(hovermode="x unified",uniformtext_minsize = 3, bargap =0.05,margin =margin,
                           legend = dict(orientation = "h"))#,yanchor = "top",y = 1,xanchor = "right",x = 1)) 

        data_average = seven_day_average(data_filter, "lab_results")
        fig = px.line(data_average, x="date_of_lab_confirmation" , y = "moving_average" , color = "county")
        fig.update_yaxes(title = "14 day average", showline=True, linewidth = 0.1, linecolor = "black")
        fig.update_xaxes(title = None, showline=True,showgrid=False,linecolor = "black",)
        fig.update_layout(hovermode="x unified",uniformtext_minsize = 3, bargap =0.05,margin =margin,
                          legend = dict(orientation = "h"))#,yanchor = "bottom"))#,y = 0,xanchor = "right",x = 1)) 
        
        #death plot
        death_data = death_data.groupby(["county","date_of_lab_confirmation"])[["date_of_lab_confirmation"]].count().rename(columns = {"date_of_lab_confirmation":"Freq"}).reset_index()
        death_data = seven_day_average(death_data,"Freq")
        fig_death = px.line(death_data, x = "date_of_lab_confirmation", y = "moving_average",color = "county")
        fig_death.update_yaxes(title = "14 day average", showline=True, linewidth = 0.1, linecolor = "black")
        fig_death.update_xaxes(title = None, showline=True,showgrid=False,linecolor = "black",)
        fig_death.update_layout(hovermode="x unified",uniformtext_minsize = 3, bargap =0.05,margin =margin,
                          legend = dict(orientation = "h"))
        
        
        data_county = data[data["County"].isin(county)]
        data_county["Proportion_affected"] = round(data_county["cases"]/data_county["Population"]*100,2)
        data_county.drop(["Unnamed: 0","Population","Discharged"],axis=1,inplace = True)
        data_county.rename(columns={"cases":"Cases","Death_cases":"Deaths",
                                    "Proportion_affected":"Affected(%)","Proportion_vaccinated":"Vaccinated(%)" },
                           inplace=True)
        
        data_table = data_county.to_dict('rows')
        columns =  [{"name": i, "id": i,} for i in (data_county[["County","Cases","Deaths","Affected(%)","Vaccinated(%)"]])] #data_county.columns
        table = dt.DataTable(data_table, columns = columns, page_size=5,#fixed_rows={'headers': True},
                             style_table={'height': '150px', 'overflowY': 'hidden','textOverflow': 'ellipsis'},
                             style_cell = {'font_family': 'helvetica','font_size': '14px','text_align': 'center'},
                            style_data = {'lineHeight': '10px','whiteSpace': 'normal','height': 'auto',
                                          'color': 'black','backgroundColor': 'white'},
                            style_as_list_view=True, #removes the grids
                            style_cell_conditional=[{
                                'if': {'column_id': 'Affected(%)'},'width': '20%',
                                "if": {"column_id": "County"}, "textAlign": "left"}],
                            style_data_conditional = [{
                                'if': {'row_index': 'odd'},'backgroundColor': 'rgb(220, 220, 220)',
                                
                                
                                }],
                            style_header = {'backgroundColor': 'rgb(210, 210, 210)', 'color': 'black','fontWeight': 'bold'}
                            
                )
       
        return fig,fig2,fig_death,table

#