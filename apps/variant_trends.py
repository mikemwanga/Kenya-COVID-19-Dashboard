import dash
from utils import *

# Reading the data

variant_data = pd.read_table(DATA_PATH.joinpath("variant_month_data.txt"))
variants_kenya = pd.read_table(DATA_PATH.joinpath("variant_data_kenya.tsv"))
variants_kenya["Month"] = pd.to_datetime(variants_kenya["Month"], format = "%Y-%m-%d")
kenya_data = pd.read_table(DATA_PATH.joinpath("kenya.metadata_0111_120122.tsv"))
variants_data = pd.read_table(DATA_PATH.joinpath("kenya_lineages_until020523.tsv"))
variant_map = pd.read_table(DATA_PATH.joinpath("map_lineages.tsv"))

class Variants:
        def __init__(self, percentage):
             self.percentage = percentage
        def variants_prevalence(self):
             fig= px.bar(variant_data, x = "months_period", y = self.percentage, color="variant_type",hover_data={"percentage":":.1%"}, 
                color_discrete_sequence = ["#AC3B3B","#377eb8","#4daf4a","#984ea3","#ff7f00","#E1B113","#6666FF"])
             fig.update_layout(paper_bgcolor = pcolor,plot_bgcolor = pcolor)
             fig.update_xaxes(title = "Time")
             fig.update_yaxes(title = "Proportion")
             return fig

plots = Variants("percentage")
variant_plot = plots.variants_prevalence()

#variants plot
#variant plot

legend = dict(orientation = "h",title=None,yanchor  = "bottom", xanchor = "left",y=-0.4,
                                                    font = dict(size=8))

fig_var = px.bar(variants_kenya, x = "Month", y = "percentage", color="variant",range_x=["2020-01-01","2023-05-01"],
                 color_discrete_sequence = ["#1b9e77","#d95f02","#7570b3","#e7298a","#8111A5","#e6ab02","#a6761d"])
#fig_var.update_traces(textfont_size=10,textposition="outside", text = variant_values["Frequency"])
fig_var.update_xaxes(nticks = 10,linecolor = "black",ticks="outside",tickfont = dict(size=10),title = None)
fig_var.update_yaxes(linecolor = "black",ticks="outside",tickfont = dict(size=12),title ="Proportion", title_font = {"size":12})
fig_var.update_layout(legend=legend,margin = margin,)


kenya_data = kenya_data[["date","pangolin_lineage"]].groupby(["date","pangolin_lineage"])[["pangolin_lineage"]].count().\
    rename(columns = {"pangolin_lineage":"Frequency"}).reset_index()
kenya_data = kenya_data[kenya_data["pangolin_lineage"] != "Unassigned"]
kenya_data["date"] = pd.to_datetime(kenya_data["date"],format = "%Y-%m-%d")
kenya_data["pangolin_lineage"].unique()
fig_kenya = px.scatter(kenya_data, x = "date",y = "pangolin_lineage",size= "Frequency", color = "pangolin_lineage")
fig_kenya.update_xaxes(title = None, linecolor = "black",tickfont = dict(size=8), title_font = dict(size=10),\
                    gridcolor = gridcolor, gridwidth = 0.2, nticks = 8)
fig_kenya.update_yaxes(title = None, linecolor = "black",tickfont = dict(size=8),gridcolor = gridcolor, gridwidth = 0.5)
fig_kenya.update_layout(margin=margin, showlegend = False)

#---------------------------------------------------------------------
#plots for observed lineages
#process data
lineages = variants_data[["date","pangolin_lineage"]].set_index("date")#.head()
lineages.index = pd.to_datetime(lineages.index, format='%d/%m/%Y')
recent_lineages = lineages[lineages.index >= "2023-01-01"].reset_index()
lineage_map = dict(zip(variant_map.lineage, variant_map.lineage_group))
recent_lineages["lineage_group"] = recent_lineages["pangolin_lineage"].map(lineage_map)
recent_lineages = recent_lineages[recent_lineages["lineage_group"] != "Unassigned"] #drop columns with unassigned annotations
recent_lineages = recent_lineages.groupby(["date","lineage_group"])[["lineage_group"]].count().rename(columns = {"lineage_group":"Frequency"}).reset_index()

#do the plot
sars_lineages = px.scatter(recent_lineages, x = "date",y = "lineage_group",size= "Frequency", color = "lineage_group",\
                    range_x=["2023-01-01","2023-05-01"])
sars_lineages.update_layout(margin=margin, showlegend = False)
sars_lineages.update_xaxes(title = None,linecolor = "black",tickfont = dict(size=10), nticks=6)
sars_lineages.update_yaxes(title = None, linecolor = "black",tickfont = dict(size=10),gridcolor = gridcolor)


layout = html.Div([
        dbc.Row([
                dbc.Col([
                    html.H5("SARS-CoV-2 Variant Epidemiology ",className = col_title, style ={"text-align":"start"}),
                    html.Hr(),
                ], width = 11, lg=10),
            ],justify="center", className = "mb-2 ms-4 me-4 ps-4 pe-4 mt-5 pt-5"),
            
        html.Div(id = "variant-content"),
        interval,
        
        reference
])

@app.callback(
    Output("variant-content","children"), Input("interval-component", "n_intervals")
)

def update_content(n_intervals):
    
    dev = html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Label("Temporal prevalence of SARS-COV-2 variants in Kenya", 
                            style = {"text-align":"start","font-size":14},className = "fw-bold text-dark ms-4"),

                        dcc.Graph(figure = fig_var,responsive = True,style = {"width":"50hw","height":"40vh"}),
                    ])
                ], className = "border-0 text-center rounded-0")
            ],xs = 10,md=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Label("SARS-COV-2 lineages between January to April 2023", 
                            style = {"text-align":"start","font-size":14},className = "fw-bold text-dark ms-4"),
                        html.Br(),html.Br(),
                        dcc.Graph(figure = sars_lineages,responsive = True,style = {"width":"40hw","height":"30vh"}),
                    ]),
                ],className = "h-100 border-0 text-center rounded-0")
                
            ],xs=10, md=4),
        ],justify = "center",className = classname_col),
        
        dbc.Row([
            dbc.Col([
                html.Label("SARS-CoV-2 Lineages Growth Rate Estimation", 
                style = {"text-align":"center","font-size":14},className = "fw-bold text-dark"),
                html.Label(["This section shows Bayesian estimate of growth rate for selected SARS-CoV-2 lineages recently observed in Kenya and globally. Data \
                    used are frequency of grouped lineages that are categorized based on region of isolation"], 
                style = {"text-align":"start","font-size":14},className = "fw-normal text-dark"),
            ],xs = 10,md=10),
            
            dbc.Row([
                html.Div([
                    html.Label("Select analyzed lineage-groups", style = {"font-size":12},className = "text-primary mb-0 pb-0"),
                    dcc.Dropdown(
                        id = "lineage_warning",
                        options = [
                            {"label":"BA.1-like/BN-like/BA.2-like", "value":"BA.1_BN_BA.2"},
                            {"label":"BA.4-like/BA.5-like/BF-like","value":"BA.4_BA.5_BF"},
                            {"label":"BQ.1-like/XBB-like/AY-like","value":"BQ.1_XBB_AY"},
                            {"label":"B.1-like/CH.1-like","value":"B.1_CH.1"},
                        ],
                        value = "BQ.1_XBB_AY",
                    )       
                ],style={"width":"20%","font-size":12,"margin-right":"55px", "margin-bottom":"5px"})
            ],justify="end"),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        
                        dbc.Row([
                            dbc.Col([
                                dbc.CardBody([                                  
                                    
                                    html.P("Flag per Country/Region",className = col_title),
                                    html.Br(),
                                    html.Div(id = "range_lineage")
                                ])

                            ], xs=10,md=6, style={}),
                            dbc.Col([
                                dbc.CardBody([                                    
                                    html.P("Flag per Variant",className = col_title),
                                    html.Br(),
                                    html.Div(id = "summary_lineage")
                                ])

                            ], xs=10,md=4)
                        ])
                    ],className = "border-0 rounded-0")
                ],xs=11, md=11)
           
            ],justify = "center"),
            
        ],justify = "center",className = classname_col)
        
    ]),           

    return dev
    
@app.callback(
        [Output("range_lineage", "children"),
        Output("summary_lineage","children")],
        Input("lineage_warning","value")
)
def load_images(value):
    if value in ["BQ.1_XBB_AY","BA.4_BA.5_BF","BA.1_BN_BA.2","B.1_CH.1"]:
        return [
            html.Img(src = dash.get_asset_url("../assets/plots/" + value + "_range_lineage.png"),\
                #style = {"width":"80hw","height":"30vh"}),
                style = {"height":"360px", "width":"500px"}),
            html.Img(src = dash.get_asset_url("../assets/plots/" + value + "_summary_lineage.png"),\
                style = {"height":"200px", "width":"450px"})]
    