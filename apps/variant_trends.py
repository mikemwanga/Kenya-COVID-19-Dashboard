import dash
from utils import *

# Reading the data
legend = dict(orientation = "h",title=None,yanchor  = "bottom", xanchor = "left",y=-0.3,
                                                    font = dict(size=8))

variant_data = pd.read_table(DATA_PATH.joinpath("variant_month_data.txt"))
variants_kenya = pd.read_table(DATA_PATH.joinpath("variant_data_kenya.tsv"))
variants_kenya["Month"] = pd.to_datetime(variants_kenya["Month"], format = "%Y-%m-%d")
kenya_data = pd.read_table(DATA_PATH.joinpath("kenya.metadata_0111_120122.tsv"))
variants_data = pd.read_table(DATA_PATH.joinpath("kenya_lineages_until130323.tsv"))
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
fig_var = px.bar(variants_kenya, x = "Month", y = "percentage", color="variant",range_x=["2020-01-01","2023-03-01"],
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
lineages.index = pd.to_datetime(lineages.index)
recent_lineages = lineages[lineages.index >= "2022-11-01"].reset_index()
lineage_map = dict(zip(variant_map.lineage, variant_map.lineage_group))
recent_lineages["lineage_group"] = recent_lineages["pangolin_lineage"].map(lineage_map)
recent_lineages = recent_lineages[recent_lineages["lineage_group"] != "Unassigned"] #drop columns with unassigned annotations
recent_lineages = recent_lineages.groupby(["date","lineage_group"])[["lineage_group"]].count().rename(columns = {"lineage_group":"Frequency"}).reset_index()

#do the plot
sars_lineages = px.scatter(recent_lineages, x = "date",y = "lineage_group",size= "Frequency", color = "lineage_group",\
                    range_x=["2022-10-15","2023-03-01"])
sars_lineages.update_layout(margin=margin, showlegend = False)
sars_lineages.update_xaxes(title = None,linecolor = "black",tickfont = dict(size=10), nticks=6)
sars_lineages.update_yaxes(title = None, linecolor = "black",tickfont = dict(size=10),gridcolor = gridcolor)

layout = html.Div([
    
    dbc.Row([
            dbc.Col([
            html.Div([
                html.Label("Select Metrics", style = {"font-size":12},className = "text-primary mb-0 pb-0"),
                dcc.Dropdown(
                    id = "variant_view",
                    options = [
                        {"label":"Trends in SARS-CoV-2 Variants", "value":"variants"},
                        {"label":"Varint by Region","value":"region"}
                    ],
                    value = "variants"
                )
            ],style={"width":"100%","font-size":12})
            ],width=3)
    ],justify="end", className = "mt-5 pt-5 me-5 pe-5"),
    html.Div(id = "variants_lineages" ),
    hm.reference
])

variants_figure = html.Div([
            dbc.Row([
                dbc.Col([
                    html.Label("Temporal prevalence of SARS-COV-2 variants in Kenya", 
                    style = {"text-align":"start","font-size":14},className = "fw-bold text-dark ms-4"),
            
                    dcc.Graph(figure = fig_var,responsive = True,style = {"height":"330px", "width":"550px"}),
                
                    
                ],width = 6,lg=5, className = "border-end"),
                dbc.Col([
                    html.Label("SARS-COV-2 lineages since November 2022", 
                    style = {"text-align":"start","font-size":14},className = "fw-bold text-dark ms-4"),
                    html.Br(),html.Br(),
                    dcc.Graph(figure = sars_lineages,responsive = True,style = {"height":"250px", "width":"500px"}),
                ], width=5,lg=4),
                
                #html.Hr(),
                
            ],justify = "center", className = "mt-2 pt-2"), 
            
            
            dbc.Row([
                dbc.Col([
                    html.Label("SARS-CoV-2 Lineages Growth Rate Estimation", 
                    style = {"text-align":"center","font-size":14},className = "fw-bold text-dark"),

                    html.Label(["This section shows Bayesian estimate of growth rate for selected SARS-CoV-2 lineages recently observed in Kenya and globally. Data \
                        used are frequency of grouped lineages that are categorized based on region of isolation"], 
                    style = {"text-align":"start","font-size":14},className = "fw-normal text-dark"),
                ],width = 11,lg=9)
            ],justify = "center", className = "mt-2 pt-2"),
            
            #set a dropdown to select 
            dbc.Row([
                dbc.Col([
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
                    ],style={"width":"100%","font-size":12})
                ],width=3)
            ],justify="end", className = "mt-1 pt-1 me-5 pe-5"),
            
            dbc.Row([
                dbc.Col([
                    html.Div(id = "range_lineage")#,style = {"height":"400px", "width":"400px"})
                ], width=6,lg=5,style = {"margin-right":"0px"},className = "border-end mt-2 pt-2", align="center"),
                dbc.Col([
                    html.Div(id = "summary_lineage")
                ],width=5,lg=4,style = {"margin-right":"0px"},className = "mt-2 pt-2", align="center"),
            ],justify = "center", className = "mt-0 pt-0"),
            
            # dbc.Row([
                
            #     dbc.Col([
            #         html.Img(src = dash.get_asset_url("../assets/plots/range_lineage.png"),style = {"height":"400px", "width":"400px"})
            #     ], width=6,lg=5, style = {"margin-right":"0px"},className = "border-end mt-2 pt-2", align="center"),
            #     dbc.Col([
            #         html.Img(src = dash.get_asset_url("../assets/plots/summary_lineage.png"),style = {"height":"400px", "width":"400px"} )
                
            #     ], width=5, lg=4,style = {"margin-left":"0px"},className = "border-start mt-2 pt-2",align="center"),
            # ],justify = "center", className = "mt-0 pt-0")     
        ])

lineages_figure = html.Div([
            dbc.Row([
                html.Label(f"SARS-CoV-2 lineages observed in Kenya in the last two months (November - December 2022)",
                     style = {"text-align":"center","font-size":14},className = "fw-bold text-dark ms-4"),
                dcc.Graph(figure = fig_kenya,responsive = True,style = {"height":"400px", "width":"800px"})
            ],justify = "center", className = "ms-5 mt-2 pt-2"),       
        ])


@app.callback(
    Output("variants_lineages", "children"),
    Input("variant_view","value")
)

def render_plots(value):
    if value == "variants":
        return variants_figure
    

@app.callback(
    [Output("range_lineage", "children"),
    Output("summary_lineage","children")],
    Input("lineage_warning","value")
)

def load_images(value):
    if value in ["BQ.1_XBB_AY","BA.4_BA.5_BF","BA.1_BN_BA.2","B.1_CH.1"]:
        return [html.Img(src = dash.get_asset_url("../assets/plots/" + value + "_range_lineage.png"),style = {"height":"400px", "width":"550px"}),
                html.Img(src = dash.get_asset_url("../assets/plots/" + value + "_summary_lineage.png"),style = {"height":"230px", "width":"500px"})]