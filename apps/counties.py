#layout for counties tab
from utils import *
#load dataset
# Reading the data
#kenya_county = gpd.read_file(DATA_PATH.joinpath("kenyan-counties/County.shp"))
data = pd.read_csv(DATA_PATH.joinpath("cases_per_county.csv"))
lati_lot = pd.read_csv(DATA_PATH.joinpath("kenya_data_latitude_longitude.csv"))
county_daily_data = pd.read_csv(DATA_PATH.joinpath("county_daily_data.csv"),dtype='unicode', low_memory=False)
county_daily_data["date_of_lab_confirmation"] = pd.to_datetime(county_daily_data["date_of_lab_confirmation"])
county_daily_data["Date"] = county_daily_data["date_of_lab_confirmation"]#.dt.date
county_daily_data.set_index("Date", inplace = True)

layout = html.Div([
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
                        # dbc.Row([
                            
                        #     html.P("Summary of cases, deaths and proportion of infected within the selected county.", 
                        #            className="fw-bold fs-6 mt-4 text-center"),
                        #     dbc.Col([dbc.CardBody([
                        #         html.H4(id="cases_value",className ="text-danger fs-3"),
                        #         html.P("Total cases",style = style_text)
                        #         ],className = card_class ),
                        #     ]),
                        #     dbc.Col([
                        #         dbc.CardBody([
                        #         html.H4(id="death_value",className ="text-black fs-3"),
                        #         html.P("Total deaths",style = style_text)
                        #         ],className = card_class ),
                        #     ]),
                        #     dbc.Col([
                        #         dbc.CardBody([
                        #         html.H4(id="prevalence",className ="text-info fs-3"),
                        #         html.P("Proportion infected",style = style_text)
                        #         ],className = card_class ),
                        #     ]),
                        
                        # ]),
                        #html.Hr(),
                        
                       # html.Div([
                            #dbc.Button("Cases",id="cases_button",n_clicks=0,size="sm",color = "primary",outline=True,style = {"font-size":10}),
                            #dbc.Button("Deaths",id="deaths_button",n_clicks=0,size="sm",color = "primary",outline=True,className="me-2",style = {"font-size":10}),
                        #],className = "d-grid gap-1 d-md-flex justify-content-sm-end"),
                        #html.Div(id = "map-content", children = []),
                        
                    ],width=5,lg=5,className = col_class,style={"margin-left":"15px", "height":"700px"})
                    
                ],justify = "center",className = hm.classname_col),
            
            hm.reference
])

# def map_plot(observation,value):
#     fig = px.choropleth(kenya_data, geojson=kenya_data.geometry, locations=kenya_data.index,hover_data = {observation:True, "random":False},
#                         color_continuous_scale="cividis",color="random", range_color=(0.4,1),width=700,height=650)
#     fig.update_geos(fitbounds = "locations", visible=False,scope="africa")
#     fig2 = go.Figure(go.Scattergeo(
#             lat = kenya_data.latitude, lon = kenya_data.longitude,text = kenya_data.index,textposition="middle center",
#             marker = dict(size=kenya_data[observation]*value,sizemode="area",color = kenya_data.random,line_color="#f0f0f0",line_width=1)
#             ))
#     fig.add_trace(fig2.data[0])
#     fig.update_layout(#paper_bgcolor = pcolor,plot_bgcolor=pcolor,bgcolor = pcolor
#                     geo = dict(projection_scale=6,center = dict(lat = 0.25,lon=38.09),landcolor ='rgb(217, 217, 217)'),
#                     coloraxis_showscale=False, height = 600,width=800,margin = margin)
#     return fig
# cases_fig = map_plot("cases",0.02)
# fatality_fig = map_plot("Death_cases",0.5)

# @app.callback(Output("map-content","children"),
#               [Input("cases_button", "n_clicks"),
#                 Input("deaths_button","n_clicks")])

# def render_map_content(click1,click2):
#         size = {"width":"37vw","height":"70vh"}
#         cases = html.Div([
#                     html.P("County distribution of COVID-19 cases",className="fs-6 text-center fw-bold"),
#                     dcc.Graph(figure = cases_fig,responsive=True, style = size ),
#                     ])
#         deaths = html.Div([
#                     html.P("County distribution of COVID-19 fatalities",className="fs-6 text-center fw-bold"),
#                     dcc.Graph(figure = fatality_fig,responsive=True,style = size)
#                     ]),
        
#         ctx = dash.callback_context #used to determine which button is triggered
        
#         button_id = ctx.triggered[0]['prop_id'].split('.')[0] #grab id of button triggered
#         if button_id == "cases_button":
#             return cases
#         elif button_id == "deaths_button":
#              return deaths
#         else:
#              return cases
                
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
        
        #cases_value = data[data["County"].isin(county)]["cases"]
        #death_value = data[data["County"]== county]["Death_cases"]
        #prevalence = round(cases_value/data[data["County"] == county]["Population"]*100,1)
        # data_table = data_county.to_dict('rows')
        # columns =  [{"name": i, "id": i,} for i in (data_county.columns)]
        # table = dt.DataTable(data_table, columns = columns)
        
        data_county = data[data["County"].isin(county)]
        data_county["Proportion_affected"] = round(data_county["cases"]/data_county["Population"]*100,2)
        data_county.drop(["Unnamed: 0","Population","Discharged"],axis=1,inplace = True)
        data_county.rename(columns={"cases":"Cases","Death_cases":"Deaths",
                                    "Proportion_affected":"Affected(%)"},
                           inplace=True)
        data_table = data_county.to_dict('rows')
        columns =  [{"name": i, "id": i,} for i in (data_county.columns)]
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
       
        return fig,fig2,fig_death,table#cases_value,death_value, prevalence,#table #fig, fig2,

#