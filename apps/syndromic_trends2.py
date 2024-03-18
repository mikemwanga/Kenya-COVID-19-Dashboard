from data_processing import *
from utils import *
from html.parser import HTMLParser
#*********************************************************************************************************************

space = html.B(className='mb-4')
line = html.Hr()
layout = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Row([
                    dbc.Col([
                    html.H4('Adult Syndromic Surveillance',className = col_title),
                    
                    html.P('A summary of data from a hospital based surveillance program focused on contributing useful information to the Ministry of Health \
                                to allow for monitoring,planning and mobilizing resources for management and control of COVID-19. Data was collected between \
                           January to December 2023.'),
                    html.Hr(),
                    ],md=12)
            ],justify="center",className='mt-4'),

            dcc.Tabs([
                dcc.Tab([
                    dbc.Row([
                        html.Br(className='mt-1'),
                        html.P('Summary of Admitted Patients',className=section_title),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H3(total_patients),
                                    dmc.Space(h=45),
                                    html.Small("Total Patients Admitted",className='card-text, mt-0'),
                                    html.Hr(),
                                ]),
                            ],body=True,className='h-100 border-0 text-center')
                        ]),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.P([html.H3(malep), html.H5(f'{male_percentage}%')]),
                                    html.Small("Male Patients",className='card-text, mt-0'),
                                    html.Hr(),
                                ]),
                            ],body=True,className='h-100 border-0 text-center'),
                        ]),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.P([html.H3(femalep), html.H5(f'{female_percentage}%')]),
                                    html.Small("Female Patients",className='card-text,mt-0'),
                                    html.Hr(),
                                ]),
                            ],body=True,className='h-100 border-0 text-center')
                        ]),
                    ],justify = "center",className= midrow_classname),
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                
                                html.P('DISTRIBUTION OF PATIENTS BY REGION AND AGE', className = col_title,style = style_title),
                                html.Br(className='mt-5'),
                                dbc.CardBody([
                                    dcc.Graph(figure=reg_fig,responsive=True,config=plotly_display,style={"height":"25vh"} ),     #                        
                                ]),
                            ],className='h-100 border-0 text-center',style={'align-items':'bottom'}), 
                        ]),
                        dbc.Col([
                            dbc.Card([
                                
                                html.P('DISTRIBUTION OF PATIENTS BY GENDER AND AGE', className = col_title,style = style_title),
                                html.Br(),
                                dbc.CardBody([                                
                                    dcc.Graph(figure=age_plot,responsive=True,config=plotly_display,style={"height":"30vh"})
                                ])
                            ],className='h-100 border-0 text-center'), #border-0
                        ]),
                    ],justify = "center",className= midrow_classname),
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                html.Br(),
                                html.P('MONTHLY PATIENT DISTRIBUTION BY REGION', className = col_title,style = style_title),
                                dbc.CardBody([
                                    dcc.Graph(figure=reg_per_fig,responsive=True,config=plotly_display,
                                            style={"height":"45vh"})
                                ]),                           
                            ],className='h-100 border-0 text-center'),
                        ]),
                        # html.Hr(),
                    ],justify = "center",className= midrow_classname),
                ],label='Patient Demography',style=tab_style,selected_style=tab_selected_style),
                dcc.Tab([
                    html.P('Documentation of Vital Measures Countrywide',className=section_title),
                    dbc.Row([
                        dbc.Col([
                            
                            dbc.Card([    
                                html.P('COUNTRYWIDE DOCUMENTATION',className = col_title,style = style_title),
                                dbc.CardBody([
                                    dcc.Graph(figure=documentation_plot,responsive=True,config=plotly_display,style={"height":"35vh"} ), 
                                ])
                            ],body=True,className='border-0'),
                        ])
                    ],justify = "center",className= midrow_classname),
                    line,
                    html.P('Documentation of Vital Measures by Region',className=section_title),
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                html.P('COAST REGION',className = col_title,style = style_title), 
                                dbc.CardBody([
                                    dcc.Graph(figure=coast_documentation_plot,responsive=True,config=plotly_display,
                                            style={"height":"25vh"} ), 
                                ]),
                            ],body=True,className='border-0'),
                        ],className='border-0'),
                        dbc.Col([
                            dbc.Card([
                                html.P('WESTERN REGION',className=col_title,style = style_title), 
                                dbc.CardBody([
                                    dcc.Graph(figure=western_documentation_plot,responsive=True,config=plotly_display,
                                            style={"height":"25vh"} ), 
                                ]),
                            ],body=True,className='border-0'),
                        ],className='border-0'),
                        dbc.Col([
                            dbc.Card([
                                html.P('CENTRAL REGION',className=col_title,style = style_title),  
                                dbc.CardBody([
                                    dcc.Graph(figure=central_documentation_plot,responsive=True,config=plotly_display,
                                            style={"height":"25vh"} ), 
                                ]),
                            ],body=True,className='border-0'),
                        ],className='border-0')
                    ],justify = "center",className= midrow_classname),                                       
                ],label='Vitals',style=tab_style,selected_style=tab_selected_style),
                dcc.Tab([
                    html.P('Documentation of Demographic Measures Countrywide',className=section_title),
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                    html.P('COUNTRYWIDE DOCUMENTATION',className = col_title,style = style_title),
                                    dbc.CardBody([
                                        dcc.Graph(figure=demographic_documentation_plot,responsive=True,config=plotly_display,
                                                  style={"height":"35vh"} ), 
                                    ]),
                            ],className='border-0 text-start'),
                        ],className='border-0')
                    ],justify = "center",className= midrow_classname),
                    line,
                    html.P('Documentation of Demographic Measures by Region',className=section_title),
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                html.P('COAST REGION',className = col_title,style = style_title), 
                                dbc.CardBody([
                                    dcc.Graph(figure=coast_demo_plot,responsive=True,config=plotly_display,
                                            style={"height":"25vh"} ), 
                                ]),
                            ],body=True,className='border-0 text-center'),
                        ],className='border-0'),
                        dbc.Col([
                            dbc.Card([
                                html.P('CENTRAL REGION',className = col_title,style = style_title),
                                dbc.CardBody([
                                    dcc.Graph(figure=central_demo_plot,responsive=True,config=plotly_display,
                                            style={"height":"25vh"} ), 
                                ]),
                            ],body=True,className='border-0 text-center'),
                        ],className='border-0'),
                        dbc.Col([
                            dbc.Card([
                                html.P('WESTERN REGION',className = col_title,style = style_title),
                                dbc.CardBody([
                                    dcc.Graph(figure=western_demo_plot,responsive=True,config=plotly_display,
                                            style={"height":"25vh"} ), 
                                ]),
                            ],body=True,className='border-0 text-center'),
                        ],className='border-0'),                        
                    ],justify = "center",className= midrow_classname),

                ],label='Demographic Measures',style=tab_style,selected_style=tab_selected_style),
                dcc.Tab([
                    line,
                    html.P('Documentation of Priority Measures Countrywide',className=section_title),
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                html.P('COUNTRYWIDE DOCUMENTATION',className = col_title,style = style_title),
                                dbc.CardBody([
                                    dcc.Graph(figure=priority_measure_df_plot,responsive=True,config=plotly_display,
                                              style={"height":"35vh"} ), 
                                ])
                            ],className='border-0'),
                        ])
                    ],justify = "center",className= midrow_classname)  ,

                    line,
                    html.P('Documentation of Priority Measures by Region',className=section_title),

                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                            html.P('DOCUMENTATION IN COAST REGION',className=col_title,style = style_title),
                                dbc.CardBody([
                                    dcc.Graph(figure=coast_priority_plot,responsive=True,config=plotly_display,
                                          style={"height":"25vh"} ), 
                                ])
                            ],className='border-0')
                            
                        ]),
                        dbc.Col([
                            dbc.Card([
                                html.P('DOCUMENTATION IN CENTRAL REGION',className=col_title,style = style_title),
                                dbc.CardBody([
                                    dcc.Graph(figure=central_priority_plot,responsive=True,config=plotly_display,
                                            style={"height":"25vh"} ), 
                                ])
                            ],className='border-0')
                        ]),
                        dbc.Col([
                            dbc.Card([
                                html.P('DOCUMENTATION IN WESTERN REGION',className=col_title,style = style_title),
                                dbc.CardBody([
                                    dcc.Graph(figure=western_priority_plot,responsive=True,config=plotly_display,
                                            style={"height":"25vh"} ), 
                                ])
                            ],className='border-0')
                            
                        ]),
                        html.Hr(),
                    ],justify = "center",className= midrow_classname),

                    html.P('Documentation of COVID-19 and HIV Status',className=section_title),
                    dbc.Row([
                        
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.P('COVID-19 VACCINATION BY REGION', className = col_title,style = style_title),
                                    dcc.Graph(figure=fig_cov_vacc_region,responsive=True,config=plotly_display,
                                              style={'height':'20vh'}),#'height':'30vh','width':'35hw'}),
                                    html.Br(),
                                    html.Hr(),
                                    html.P('COVID-19 VACCINATION BY PERIOD', className = col_title,style = style_title),
                                    dcc.Graph(figure = fig_cov_vacc_month,responsive=True,config=plotly_display,
                                              style={'height':'30vh'}),#'height':'30vh','width':'35vw'})
                                ]),
                            ],className='border-0 text-center rounded-0')
                        ],md=6),
                        
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.P('HIV STATUS BY REGION', className = col_title,style = style_title),
                                    dcc.Graph(figure=fig_hiv_region,responsive=True,config=plotly_display,
                                              style={'height':'20vh','width':'35vw'}),
                                    html.Br(),
                                    html.Hr(),
                                    html.P('HIV STATUS BY PERIOD', className = col_title,style = style_title),
                                    dcc.Graph(figure=fig_hiv_period,responsive=True,
                                              config=plotly_display,style={'height':'30vh','width':'35vw'})
                                ])
                            ],className='h-100 border-0 text-center rounded-0')
                        ],md=6),

                        html.Hr(),
                    ],justify = "center",className= midrow_classname),
                ],label='Priority Measures',style=tab_style,selected_style=tab_selected_style),
                dcc.Tab([
                    line,
                    dbc.Row([
                        html.Br(className='mt-1'),
                        html.P('TRENDS IN MORTALITY ACROSS HEALTH FACILITIES',className=section_title),
                        dbc.Col([
                            dbc.Card([
                                html.P('COUNTRYWIDE TRENDS IN MORTALITY',className=col_title,style = style_title),
                                html.P('Summary of discharged patients, alive and dead across all the studied health facilities in the Country',
                                       className=description_text, style=description_style_title),
                                space,
                                dcc.Graph(figure=outcome_plot,responsive=True,config=plotly_display,
                                        style={"height":"35vh"} ),
                            ],className='border-0'),

                        ],md=6,className=''),

                        dbc.Col([
                            dbc.Card([
                            html.P('COUNTRYWIDE TRENDS IN MORTALITY BY GENDER',className=col_title,style = style_title),
                            html.P('Observed death cases between male and female patients across all the studied health facilities in the Country',
                                   className=description_text, style=description_style_title),
                            space,
                            dcc.Graph(figure=outcome_death_sex_plot,responsive=True,config=plotly_display,
                                        style={"height":"35vh"} )
                            ],className='border-0'),
                        ],md=6,className=''),
                    ],justify=''),
                    line,
                    dbc.Row([
                        html.P('TRENDS IN MORTALITY BY REGION',className=section_title),
                        
                        dbc.Col([
                            dbc.Card([
                                html.P('TRENDS IN DEATHS IN COAST REGION',className=col_title,style = style_title),
                                space,
                                dcc.Graph(figure=coast_outcome_plot,responsive=True,config=plotly_display,style={"height":"35vh"} )
                            ],className='border-0')
                        ]),
                        dbc.Col([
                            dbc.Card([
                                html.P('TRENDS IN DEATHS IN CENTRAL REGION',className=col_title,style = style_title),
                                space,
                                dcc.Graph(figure=central_outcome_plot,responsive=True,config=plotly_display,style={"height":"35vh"} )
                            ],className='border-0')
                        ]),
                        dbc.Col([
                            dbc.Card([
                                html.P('TRENDS IN DEATHS IN WESTERN REGION',className=col_title,style = style_title),
                                space,
                                dcc.Graph(figure=western_outcome_plot,responsive=True,config=plotly_display,
                                          style={"height":"35vh"} )
                            ],className='border-0')
                        ])
                    ],justify='center',className= midrow_classname),
                ],label='Outcome',style=tab_style,selected_style=tab_selected_style),
                dcc.Tab([
                    html.P('We acknowledge the following health facilities for providing the dataset',className='mt-3 ms-2'),
                    
                    dbc.Row([
                        dbc.Col([
                            dcc.Markdown(
                                '''
                                * Jaramogi Oginga Odinga Teaching and Referral Hospital,
                                * Naivasha County Referral Hospital,
                                * Kiambu Level 5 Hospital,
                                * Machakos Level 5 Hospital,
                                * Mama Lucy Kibaki Hospital,
                                * Mbagathi Hospital, 
                                * Kerugoya County Referral Hospital,
                                * Kilifi County Referral Hospital                            
                                '''
                            )
                        ]),
                        dbc.Col([
                            dcc.Markdown(
                                '''
                                * Coast General Teaching and Referral Hospital,
                                * Kisumu County Hospital,
                                * Kakamega County General & Teaching Referral Hospital,
                                * Busia County Referral Hospital,
                                * Kitale County Referral Hospital,
                                * Bungoma County Hospital,
                                * Kisii Teaching and Referral Hospital                              
                                '''
                            )
                        ]),
                        
                    ],justify = "center",className = classname_col)
                      
                ],label='Data Source',style=tab_style,selected_style=tab_selected_style)

            ])
        ],md=10)
    ],justify='center',className = classname_col),
    reference
],className='ms-5 me-5 mt-4')