from utils import *

variant_growth_rate_fy4 = pd.read_table(DATA_PATH.joinpath("FY.4_posterior_plot_data.tsv"))
variant_growth_rate_xbb = pd.read_table(DATA_PATH.joinpath("XBB_posterior_plot_data.tsv"))
variant_growth_rate_ge = pd.read_table(DATA_PATH.joinpath("GE.1_posterior_plot_data.tsv"))
variant_growth_rate_eg = pd.read_table(DATA_PATH.joinpath("EG.5_posterior_plot_data.tsv"))
plotsize={"width":"40hw","height":"25vh"}

def load_varaint_data():
    
    global variant_growth_rate_fy4,variant_growth_rate_xbb
    variants_kenya = pd.read_table(DATA_PATH.joinpath("variant_data_kenya.tsv"))
    variants_kenya["Month"] = pd.to_datetime(variants_kenya["Month"], format = "%Y-%m-%d")
    variants_data = pd.read_table(DATA_PATH.joinpath("kenya_lineages4.tsv"))
    variants_data['date'] = pd.to_datetime(variants_data['date'],format="%Y-%m-%d")
    variants_data = variants_data[variants_data['pangolin_lineage'] != 'Unassigned']

    variant_map = pd.read_table(DATA_PATH.joinpath("map_lineages.tsv"))
    var_type =  dict(zip(variant_map.lineage, variant_map.lineage_group))
    variants_data["lineage_type"] = variants_data["pangolin_lineage"].map(var_type)
    
    county_lineages = variants_data[variants_data["date"] > "2023-01-01"][['date','division','pangolin_lineage','lineage_type']]
    county_lineages  =county_lineages.groupby(['division','lineage_type'])[['lineage_type']].count().rename(columns={'lineage_type':'Freq'}).reset_index()
    county_lineages['lineage_type_prop'] = round(county_lineages['Freq']/county_lineages[['division','Freq']].\
                         groupby('division')['Freq'].transform('sum') *100,1)
    

    return variants_kenya,variants_data,variant_map,county_lineages


def growth_rate(data):
    fig = px.scatter(data, x='week_prior_to',y='area',color='levelFlag2',
                     color_discrete_map={'No Growth':'#9acd32','Slow Growth':'#ffc40c','Growing':'#da2c43'})
    fig.update_traces(marker=dict(size=20, symbol='square'))
    fig.update_xaxes(title = 'Week Prior To',linecolor = "black",tickfont = dict(size=10),nticks=10)
    fig.update_yaxes(title = None, linecolor = "black",tickfont = dict(size=10),gridcolor = gridcolor,tickson="boundaries",
                     ticks='outside',ticklen=60,tickcolor=gridcolor)
    
    fig.update_layout(margin=margin,
                     legend=dict(orientation = "h",yanchor="bottom",xanchor = "left",y=-0.4,title=None),
                     font = dict(size=10))#,title=None,yanchor  = "bottom", xanchor = "left",y=-0.4,
    return fig



def do_figure(data,counties):
    # if len(counties) < 4 :
    #     return print('Only accepts 4 counties')
    figures=[]
    for county in counties:
        data_f = data[data['division'].isin([county])]
        data_f = data_f.sort_values('lineage_type_prop',ascending=False)
        plot = px.bar(data_f.head(),y='lineage_type',x='lineage_type_prop',
                     orientation = "h",range_x=[0,100])
        plot.update_xaxes(title='Proportion(%)',title_font = {"size":10},tickfont = dict(size=10),linecolor=gridcolor)
        plot.update_yaxes(title=None,tickfont = dict(size=10),categoryorder ="total ascending")
        plot.update_layout(margin=margin_county,title = county,modebar_remove=['zoom', 'pan'])
        plot.update_traces( width=0.6) #textposition = "outside", textfont_size=10,cliponaxis=True,
        
        figures.append(plot)
    return figures
                     
                                        
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
    Output("variant-content","children"),
    Input("interval-component", "n_intervals")
)

def update_content(n_intervals):
    
    variants_kenya,variants_data,variant_map,county_lineages = load_varaint_data()
    
    legend = dict(orientation = "h",title=None,yanchor  = "bottom", xanchor = "left",y=-0.4,
                                                    font = dict(size=8))
    
    next_month = max(variants_kenya['Month']) + pd.offsets.MonthBegin(1)    
    fig_var = px.bar(variants_kenya, x = "Month",y = "percentage", color="variant",range_x=["2020-01-01",next_month],
                     color_discrete_sequence = ["#1b9e77","#d95f02","#7570b3","#e7298a","#8111A5","#e6ab02","#a6761d"],
                     hover_name='variant',hover_data={'Month':True,'Frequency':True,'variant':False,'percentage':False}
                     )
    fig_var.update_xaxes(nticks = 10,linecolor = "black",ticks="outside",tickfont = dict(size=10),title = None,
                         tickformat='%b-%y')
    fig_var.update_yaxes(linecolor = "black",ticks="outside",tickfont = dict(size=12),title ="Proportion", title_font = {"size":12})
    fig_var.update_layout(legend=legend,margin = margin,hoverlabel=hoverlabel)
    
    
                          #,hoverlabel=hoverlabel,hover_name='variant',hover_data=['Month'])


    lineages = variants_data[["date","pangolin_lineage"]]#.set_index("date")#.h
    lineage_map = dict(zip(variant_map.lineage, variant_map.lineage_group))
    lineages["lineage_group"] = lineages["pangolin_lineage"].map(lineage_map)
    lineages = lineages[lineages["lineage_group"] != "Unassigned"] #drop columns with unassigned annotations
    lineages = lineages.groupby(["date","lineage_group"])[["lineage_group"]].count().\
        rename(columns = {"lineage_group":"Frequency"}).reset_index()   

    maxdate = max(lineages['date'] - pd.offsets.MonthBegin(0))

    sars_lineages = px.scatter(lineages, x = "date",y = "lineage_group",size= "Frequency", color = "lineage_group",\
                        range_x=["2023-01-01",maxdate],color_discrete_sequence=color_patterns)
    
    sars_lineages.update_layout(margin=margin, showlegend = False)
    sars_lineages.update_xaxes(title = None,linecolor = "black",tickfont = dict(size=10), nticks=6,tickformat='%b-%y',ticks="outside")
    sars_lineages.update_yaxes(title = None, linecolor = "black",tickfont = dict(size=10),gridcolor = gridcolor,
                               categoryorder='category descending')
    
    counties = ['Nairobi','Kilifi','Kiambu','Mombasa','Kisumu','Lamu']
    data = county_lineages[county_lineages['division'].isin(counties)]
    fig1,fig2,fig3,fig4,fig5,fig6 = do_figure(data,counties)
    

    variants_layout = html.Div([
        
        dbc.Row([
            dbc.Col([
                html.P('VARIANT DISTRIBUTION IN KENYA',className = col_title_start),
                dbc.Row([

                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.Label("Temporal prevalence of SARS-COV-2 variants in Kenya", 
                                    style = {"text-align":"start","font-size":14},className = "fw-bold text-dark ms-4"),

                                dcc.Loading(dcc.Graph(figure = fig_var,responsive = True,style = {"width":"50hw","height":"50vh"},config= plotly_display)),
                            ])
                        ], className = "h-100 border-0 text-center rounded-0")
                    ],xs = 12,md=7, lg=7),

                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.Label("Kenya SARS-COV-2 lineages: 2023-2024", 
                                    style = {"text-align":"start","font-size":14},className = "fw-bold text-dark ms-4"),
                                html.Br(),html.Br(),
                                dcc.Loading(dcc.Graph(figure = sars_lineages,responsive = True,style = {"width":"60hw","height":"50vh"},config= plotly_display)),
                            ]),
                        ],className = "h-100 border-0 text-center rounded-0")

                    ],xs=12, md=5,lg=5),
                ],justify = "center",className='mt-1'),
            ],width=12)
        ],justify = "center",className = classname_col),
        
        dbc.Row([
            
            dbc.Col([
                html.P('VARIANT PREVALENCE AT COUNTY LEVELS (Jan 2022 to Date)',className = col_title_start),
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(figure = fig1,responsive=True,style=plotsize,config= plotly_display)
                    ],xs=9,md=4,lg=4),
                    dbc.Col([
                        dcc.Graph(figure =fig2,responsive=True,style=plotsize,config= plotly_display)
                    ],xs=9,md=4,lg=4),
                    dbc.Col([
                        dcc.Graph(figure =fig5,responsive=True,style=plotsize,config= plotly_display)
                    ],xs=9,md=4,lg=4),
                ],justify='center',className='g-2 mt-1'),
                
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(figure =fig3,responsive=True,style=plotsize,config= plotly_display)
                    ],xs=9,md=4,lg=4),
                    dbc.Col([
                        dcc.Graph(figure =fig4,responsive=True,style=plotsize,config= plotly_display)
                    ],xs=9,md=4,lg=4),
                    dbc.Col([
                        dcc.Graph(figure =fig6,responsive=True,style=plotsize,config= plotly_display)
                    ],xs=9,md=4,lg=4)
                ],justify='center',className='g-2 mt-1')
                
            ],width=10),
            
        ],justify = "center",className = classname_col),
        
        dbc.Row([
            dbc.Col([
                html.Label("SARS-CoV-2 Lineages Growth Rate Estimation", 
                style = {"text-align":"center","font-size":14},className = "fw-bold text-dark"),
                html.Label(["This section shows Bayesian estimate of growth rate for selected SARS-CoV-2 lineages recently observed in Kenya and globally. Data \
                    used are frequency of grouped lineages that are categorized based on region of isolation"], 
                style = {"text-align":"start","font-size":14},className = "fw-normal text-dark"),
            ],xs = 10,md=9,lg=8),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.Row([
                            
                            dbc.Col([
                                html.Div([
                                html.Label("Select analyzed lineage-groups", style = {"font-size":12},className = "text-primary mb-0 pb-0"),
                                    dcc.Dropdown(
                                        id = "lineage_warning",
                                        options = [
                            
                                            {"label":"FY.4-like","value":"FY.4"},
                                            {"label":"XBB-like","value":"XBB-like"},
                                            {"label":"GE.1-like","value":"GE_1-like"},
                                            {"label":"EG.5-like","value":"EG_5-like"},
                                        ],
                                        value = "FY.4",
                                        )    
                                       
                                ],style={"font-size":12,"margin-start":"200px" ,"margin-bottom":"5px","width":"80%"}), #"width":"100%",
                            ],xs=4,md=3, className = "ms-3 mt-3")
                            
                        ],justify="start"),
                        
                        dbc.Row([
                            dbc.Col([
                                dbc.CardBody([                                  
                                    
                                    html.P("Flag per Country/Region",className = col_title),
                                    html.Br(),
                                    dcc.Graph(id = "range_lineage",responsive=True,style={"width":"60%","height":'100%'},config= plotly_display) 
                                ])
                            ],xs=10,md=10),
                            
                        ],justify = "center")
                        
                    ],className = "border-0 rounded-0")
                    
                    
                ],xs=12, md=12,lg=12)
           
            ],justify = "center"),
            
        ],justify = "center",className = classname_col)
        
    ])
    
    return variants_layout

gr_fy4 = growth_rate(variant_growth_rate_fy4)
gr_xbb = growth_rate(variant_growth_rate_xbb)
gr_ge1 = growth_rate(variant_growth_rate_ge)
gr_eg = growth_rate(variant_growth_rate_eg)

@app.callback(
        Output("range_lineage", "figure"),
        #Output("summary_lineage","children")],
        Input("lineage_warning","value")
)
def load_images(value):
    if value in ["FY.4"]:
        return gr_fy4
    elif value == 'XBB-like':
        return gr_xbb
    elif value == 'GE_1-like':
        return gr_ge1
    elif value == 'EG_5-like':
        return gr_eg
        