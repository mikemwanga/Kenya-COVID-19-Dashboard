import dash
from jupyter_dash import JupyterDash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback
from dash.dependencies import Input,Output
import dash_mantine_components as dmc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from dash_bootstrap_templates import load_figure_template
load_figure_template(["minty"])
#from utils import margin

app = JupyterDash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP])

data = pd.read_csv('./Syndromic_Surveillance_data.csv',low_memory=False)
data[['date_of_admission', 'date_of_discharge']] = data[['date_of_admission', 'date_of_discharge']].\
                                apply(pd.to_datetime, format="%Y-%m-%d")
data[(data['sex'] != 'Male') & (data['sex'] != 'Female')]
data = data[data['date_of_admission'] >'2022-12-31']
data.age_years.fillna(data.calculated_age,inplace=True)
data['month'] = data['date_of_admission'].apply(lambda x: x.strftime('%b-%y'))

#map regions
map_dict = {'Naivasha':'Central',
'Kiambu':'Central','Mbagathi':'Central','Mama_Lucy':'Central','JOOTRH':'Western','Kisumu':'Western','Kakamega':'Western','Busia':'Western',
'Kitale':'Western','Bungoma':'Western','Kisii':'Western'}

data['region'] = data['hospital'].map(map_dict)

central = '#794d65'
western='#c39054'

discrete_color = [central,western]
col_title = "text-start text-secondary fw-bold mb-0 ms-4 mt-2"
section_title = "text-start text-secondary ms-3 text-start fw-bold fs-5"
male_color = '#00698f'# 
female_color = '#de6f1d' # 
gender_color =[female_color,male_color]
gridcolor = '#e5e4e2'
linecolor ='#170B3B'
plot_color = "rgba(0,0,0,0)"
line_class = 'align-items-start mb-0 ms-1'
line_style = {'width':'70%'}

plotly_display = {'displaylogo': False,'scrollZoom':False,
                'modeBarButtonsToRemove': ['pan','autoScale','resetScale2d','zoom2d','zoomIn2d','zoomOut2d', 'hoverCompareCartesian', 
                                            'resetViewMapbox','hoverClosestCartesian', 'toggleSpikelines']}

#group age groups
def age_group(dataframe,column):
        '''Function to generate age groups. returns age groups column in the data frame'''
        dataframe['age_groups'] = pd.qcut(dataframe[column],
                                       [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,1],
                                       labels=['<10','11-20','21-30','31-40','41-50','51-60','61-70','>70'])
        return dataframe
    
data = age_group(data,'age_years')
data['duration'] = (data['date_of_discharge']-data['date_of_admission'])/np.timedelta64(1,'D')

total_central = len(data[data['region'] == 'Central'])
total_western = len(data[data['region'] == 'Western'])

margin = dict(l=10, r=10, t=5, b=5)
total_patients = len(data)
malep = len(data[data['sex'] == 'Male'])
femalep = len(data[data['sex'] == 'Female'])
#total_patients = malep + femalep

male_percentage = round((malep/(total_patients)*100),1)
female_percentage = round((femalep/(total_patients)*100),1)

reg_data = data[['record_id','date_of_admission','hospital','sex','age_years','region','age_groups','month','outcome',
                 'status_at_discharge','date_of_discharge']]


df_all = data.loc[(data['sex'].isin(['Male','Female'])) & (data['date_of_admission'] >'2022-12-31' )]\
    [['age_groups','month','sex','date_of_admission','calculated_age','age_years']]
df_age = df_all[(df_all.age_years > 0) & (df_all.age_years < 100)]
age_sex = df_age.groupby(['sex','age_groups'])[['sex']].count().rename(columns={'sex':'count'}).reset_index()
age_sex_f = age_sex[age_sex['sex'] == 'Female']
age_sex_m = age_sex[age_sex['sex'] == 'Male']


def age_gender_plot(male_data,female_data):
    age_plot= go.Figure()
    age_plot.add_trace(go.Bar(y = female_data["age_groups"], x = female_data["count"]*-1, orientation="h",name = "Female",
                            marker=dict(color=female_color),
                            ))

    age_plot.add_trace(go.Bar(y = male_data["age_groups"], x = male_data["count"], orientation="h",name = "Male",
                            marker=dict(color=male_color)))
    age_plot.update_layout(barmode = "relative",bargap = 0.5,bargroupgap=0,
                            xaxis =  dict(tickvals = [-800,-600,-400,-200,0,200,400,600,800],
                                            ticktext = ["800","600","400","200","0","200","400","600","800"]),
                            legend = dict(orientation = "h",title=None,yanchor='top',y=1.2,xanchor='right',x=1),
                            margin=margin,paper_bgcolor=plot_color,plot_bgcolor=plot_color),
    age_plot.update_traces(width=0.5)
    age_plot.update_yaxes(tickfont = dict(size=12),title =None,title_font = {"size":12},ticks='outside',)
    age_plot.update_xaxes(tickfont = dict(size=12),title = None,gridcolor=gridcolor, linecolor=linecolor,ticks='outside')
    return age_plot

age_plot = age_gender_plot(age_sex_f,age_sex_m)

df = reg_data.groupby(['region','sex'])[['sex']].count().rename(columns={'sex':'count'}).reset_index()
df['gender_proportion'] = df['count'].apply(lambda x: x*100/df['count'].sum())


reg_fig = px.bar(df, y='region',x='gender_proportion', color='sex',barmode='group',range_x=([0,100]),
                 color_discrete_sequence= gender_color,text='count')
reg_fig.update_traces(textposition='outside',textfont_size=10)
reg_fig.update_layout(margin=margin,legend=dict(orientation='h',title=None,yanchor='top',y=1,xanchor='right',x=1),
                      uniformtext_minsize=7, uniformtext_mode='hide',paper_bgcolor=plot_color,plot_bgcolor=plot_color)
reg_fig.update_yaxes(tickfont = dict(size=12),title = None,ticks='outside')
reg_fig.update_xaxes(title ='Proportion(%)',nticks=10, tickfont = dict(size=12),linecolor= linecolor,gridcolor=gridcolor,ticks='outside')


reg_period = reg_data.groupby(['region','month'])[['region']].count().rename(columns={'region':'count'}).reset_index()
reg_period['proportion'] = round(100 * reg_period['count']/reg_period.groupby('region')['count'].transform('sum'),1)

def plot_reg_period(data):
    fig = px.bar(data, x='month',y='proportion',barmode='group',color='region',range_y=([0,100]),
                        color_discrete_sequence= discrete_color,text = 'count')
    fig.update_xaxes(categoryorder='array',categoryarray=['Jan-23','Feb-23','Mar-23','Apr-23','May-23','Jun-23'])
    fig.update_layout(margin=margin,legend=dict(orientation='h', title=None,yanchor='top',y=1.2,xanchor='right',x=1),
                      paper_bgcolor=plot_color,plot_bgcolor=plot_color)
    fig.update_xaxes(tickfont = dict(size=12),title=None,linecolor='gray',ticks='outside',)
    fig.update_yaxes(tickfont = dict(size=12),nticks=6,title='Proportion(%)',gridcolor=gridcolor,ticks='outside',)
    fig.update_traces(textposition='outside',textfont_size=10)
    
    return fig

reg_per_fig =plot_reg_period(reg_period)

val_class = "fs-4 fw-normal ms-3"
col1_class = "ms-2"

####################################################################################################
#data captured
data_campture = data[['record_id','dob_known','date_of_entry','biodata_complete','sex','age_years','region','age_groups','month',\
    'date_of_admission','weight','height','outcome','status_at_discharge','date_of_discharge',
    'd1_present','cause_of_death','temp','heart_rate','resp_rate','blood_pressure_sys','blood_pressure_dia','oxygen_sat']]

def group_value(column,value):
    grouped = data_campture[data_campture[column].isin([value])][['region', column]].groupby('region').count().reset_index()
    return grouped

def group_between(column,min,max):
    grouped = data_campture[data_campture[column].between(min, max)][['region', column]].groupby('region').count().reset_index()
    return grouped

sex_complete = data_campture[data_campture['sex'].isin(['Male','Female'])][['sex','region']].groupby('region').count().reset_index()
#bio_complete = group_value('biodata_complete','Complete')
dob_known  = group_value('dob_known','Yes')
temp = group_between('temp',30,45)
heart_rate = group_between('heart_rate',40,150)
resp_rate = group_between('resp_rate',5,30)
height_complete = group_between('height',50,250)
weight_complete = group_between('weight',40,250)
oxy_rate = group_between('oxygen_sat',20,100)
age_complete = group_between('age_years',18,100)
bp_dialysis = group_between('blood_pressure_dia',50,200)
bp_systolic = group_between('blood_pressure_sys',50,200)

df_demo = pd.merge(dob_known,sex_complete,on='region').\
    merge(height_complete,on='region').\
        merge(weight_complete,on='region').\
            merge(age_complete,on='region')
df_demo.set_index('region',inplace=True)
df_demo = (df_demo.div(total_patients)*100).round(1)

df_vital_signs = pd.merge(temp,resp_rate,on='region').\
    merge(heart_rate,on='region').\
        merge(oxy_rate,on='region').\
            merge(bp_dialysis,on='region').\
                merge(bp_systolic,on='region')
                
df_vital_signs.set_index('region',inplace=True)
df_vital_signs = (df_vital_signs.div(total_patients)*100).round(1)

#heatmap plot
def heatmap_plot(data):
    fig = px.imshow(data,text_auto=True,aspect="auto",range_color=(0,100),
                    color_continuous_scale=px.colors.sequential.amp)#PuBu)amp
    fig.update_layout(margin=margin)
    fig.update_xaxes(title=None,side='top', gridcolor='gray',ticks='outside')
    fig.update_coloraxes(colorbar={'orientation':'h', 'thickness':10, 'y':-0.2})
    fig.update_traces(ygap=1,xgap=1)

    return fig

fig_demo_heatmap = heatmap_plot(df_demo.T)
fig_vital_heatmap = heatmap_plot(df_vital_signs.T)

######hiv status########################
colors = {'Empty':'#DEDEDE','No':'#077c86','Yes':'#e83357','missing':'#db2153',#eeeeee'
          'Negative':'#bfa07f','Positive':'#c93071','Unknown':'#d9a744'}

classname_col = "bg-secondary bg-opacity-10 g-1 justify-content-center p-2 m-2" 

midrow_classname = "g-1 justify-content-center"# p-2 m-2"

style_title = {"font-size":13}

#function for data
def priority_group(data,column1,column2):
    df = data[[column1,column2]].groupby([column1,column2])[[column2]].count().\
        rename(columns={column2:'count'}).reset_index()
    df['prop'] = round(100*df['count']/df.groupby(column1)['count'].transform('sum'),1)
    return df

hiv_data_region = priority_group(data,'region','hiv_status')
hiv_data_month = priority_group(data,'month','hiv_status')
cov_vaccine_region = priority_group(data,'region','received_covid_19_vaccine')
cov_vaccine_month = priority_group(data,'month','received_covid_19_vaccine')

#fucntion for plot
def priority_plot(data,column,yaxis):
    fig = px.bar(data, x='prop', y=yaxis, color=column,
             orientation='h', color_discrete_map=colors)
    fig.update_xaxes(title=None,gridcolor=gridcolor,ticks='outside')
    fig.update_yaxes(title=None,ticks='outside')
    #fig.update_traces(textposition='inside',textfont_size=10)
    fig.update_yaxes(categoryorder='array',categoryarray=['Jan-23','Feb-23','Mar-23','Apr-23','May-23','Jun-23'])
    fig.update_layout(barmode='stack',margin=margin,
                      legend=dict(title=None,orientation='h',yanchor='bottom',y=-0.8,x=0))
    return fig


#reg_per_fig.update_xaxes(categoryorder='array',categoryarray=['Jan-23','Feb-23','Mar-23','Apr-23','May-23','Jun-23']
                         
fig_cov_vacc_region = priority_plot(cov_vaccine_region,'received_covid_19_vaccine','region')
fig_cov_vacc_month = priority_plot(cov_vaccine_month,'received_covid_19_vaccine','month')

fig_hiv_region = priority_plot(hiv_data_region,'hiv_status','region')
fig_hiv_period = priority_plot(hiv_data_month,'hiv_status','month')

####################################################################################################
completion = data[['month','region','biodata_complete','presenting_complaints_and_history_complete','examination_complete',\
    'admission_diagnosis_complete','investigations_complete','discharge_summary_complete']]


def completion_group(column1,column2):
    df = completion[[column1,column2]].groupby([column1,column2])[[column1]].count().\
    rename(columns={column1: 'count'}).reset_index()
    df[(column1+'_'+'prop')] = round(100*df['count']/df.groupby(column2)['count'].transform('sum'),1)
    df.drop('count',axis=1,inplace=True)
    df.set_index('month',inplace=True)
    df.rename(columns={column1:'variable'},inplace=True)
    return df

biodata_month = completion_group('biodata_complete','month')
examination_data_month = completion_group('examination_complete','month')
complaints_history_month = completion_group('presenting_complaints_and_history_complete','month')
admi_diagnosis_month = completion_group('admission_diagnosis_complete','month')
investigations_complete_month = completion_group('investigations_complete','month')
discharge_summary_month = completion_group('discharge_summary_complete','month')


def presenting_symptoms(value):
    sum_len = len(data[value].isin(['Yes','No']))
    df= data[data[value]=='Yes'][['record_id','region',value]]
    df = df.groupby('region')[[value]].count()
    df[value] =  df[value].apply(lambda x: (x/sum_len)*100)
    return df

df_headach = presenting_symptoms('headache')
df_diarrhoea = presenting_symptoms('diarrhoea')
df_cough = presenting_symptoms('cough')
df_chestpain = presenting_symptoms('chest_pain')
df_vomiting = presenting_symptoms('vomiting')
df_fever = presenting_symptoms('fever')
df_vomiting = presenting_symptoms('vomiting')
df_dysuria = presenting_symptoms('dysuria')
df_losscon = presenting_symptoms('loss_of_consciousness')

symp_data = pd.merge(df_headach,df_diarrhoea,on='region').\
    merge(df_cough,on='region').merge(df_chestpain,on='region').\
            merge(df_vomiting,on='region').merge(df_fever,on='region').\
                        merge(df_dysuria,on='region').merge(df_losscon,on='region')


symp_data.rename(columns={'loss_of_consciousness':'Asphyxia'},inplace=True)
df = symp_data.T
figplot= go.Figure()
figplot.add_trace(go.Bar(x = df['Central']*-1,y=df.index, orientation="h",name = "Central",marker=dict(color=central)))
figplot.add_trace(go.Bar(x = df['Western'],y=df.index, orientation="h",name = "Western",marker=dict(color=western)))
figplot.update_layout(barmode = "relative",bargap = 0.5,bargroupgap=0,
                   xaxis =  dict(tickvals = [-15,-10,-5,0,5,10,15],
                                        ticktext = ['15',"10",'5',"0",'5',"10","15",'20']),
                   legend = dict(orientation = "h",title=None,
                                yanchor='top',y=1.3,xanchor='left',x=0.5),
                   margin=margin,paper_bgcolor=plot_color,plot_bgcolor=plot_color)
figplot.update_traces(width=0.5)
figplot.update_yaxes(tickfont = dict(size=12),title = None,ticks='outside')
figplot.update_xaxes(tickfont = dict(size=12),title = "Proportion(%)",ticks='outside',
                     gridcolor=gridcolor,title_font = {"size":12},linecolor=linecolor)


def presenting_symptoms_period(value):
    sum_len = len(data[value].isin(['Yes','No']))
    df= data[data[value]=='Yes'][['record_id','month',value]]
    df = df.groupby('month')[[value]].count()
    df[value] =  round(df[value].apply(lambda x: (100*x/sum_len)),1)
    return df

period_headach = presenting_symptoms_period('headache')
period_diarrhoea = presenting_symptoms_period('diarrhoea')
period_cough = presenting_symptoms_period('cough')
period_chestpain = presenting_symptoms_period('chest_pain')
period_vomiting = presenting_symptoms_period('vomiting')
period_fever = presenting_symptoms_period('fever')
period_vomiting = presenting_symptoms_period('vomiting')
period_dysuria = presenting_symptoms_period('dysuria')
period_losscon = presenting_symptoms_period('loss_of_consciousness')

perioddata= pd.merge(period_headach,period_diarrhoea,on='month').\
    merge(period_cough,on='month').merge(period_chestpain,on='month').\
            merge(period_vomiting,on='month').merge(period_fever,on='month').\
                        merge(period_dysuria,on='month').merge(period_losscon,on='month')

perioddata.rename(columns={'loss_of_consciousness':'Asphyxia'},inplace=True)

fig_period_heatmap = heatmap_plot(perioddata.T)

ring_color = '#3d86b8'
fill_color='#333338'

count_data = data[['date_of_admission','region']].groupby(['region','date_of_admission'])[['date_of_admission']]\
                         .count().rename(columns={'date_of_admission':'Count'}).reset_index()
count_data['cumsum'] = count_data.groupby('region')['Count'].cumsum()
cum_plot = px.line(count_data, x = 'date_of_admission',y='cumsum',color='region',range_x=['2023-01-01','2023-07-01'],
                   color_discrete_sequence = discrete_color,
                   hover_name='region',hover_data={'region':False,'cumsum':True})

cum_plot.update_xaxes(title = None,linecolor='gray',ticks='outside',dtick='M1',tickformat='%b-%y')
cum_plot.update_yaxes(title = None,ticks='outside')
cum_plot.update_layout(margin = margin,legend = dict(orientation='h',title=None,yanchor='top',y=1.2,xanchor='right',x=1))


##Discharge and Outcome
outcome_sex =  priority_group(data,'outcome','sex')
outcome_region = priority_group(data,'outcome','region')

def plot_figure(data):
    '''Function to plot region for alive and dead'''
    
    fig = px.bar(data, y = 'region',x='prop',color='region',barmode='group',range_x=([0,100]),
                 color_discrete_sequence= discrete_color,text='count')
    fig.update_traces(textposition='outside',textfont_size=10)
    fig.update_layout(margin=margin,legend=dict(orientation='h',title=None,yanchor='top',y=1,xanchor='right',x=1),
                      uniformtext_minsize=7, uniformtext_mode='hide',paper_bgcolor=plot_color,plot_bgcolor=plot_color)
    fig.update_yaxes(tickfont = dict(size=12),title = None,ticks='outside')
    fig.update_xaxes(title ='Proportion(%)',nticks=10, tickfont = dict(size=12),linecolor= linecolor,gridcolor=gridcolor,ticks='outside')
    return fig

##outcome discharge
##STATUS AT DISCHARGE
status_at_discharge = data_campture[['status_at_discharge']].value_counts().rename_axis('status').reset_index(name='counts')
status_at_discharge['prop'] = status_at_discharge['counts']/status_at_discharge['counts'].sum()*100

status_at_discharge_plot = px.bar(status_at_discharge.sort_values('prop'),x='prop',y ='status',orientation='h',text='counts')
                                  
status_at_discharge_plot.update_yaxes(title=None)
status_at_discharge_plot.update_layout(margin=margin,paper_bgcolor=plot_color,plot_bgcolor=plot_color)
status_at_discharge_plot.update_traces(textposition='outside',marker_color='indianred')


####################################################################################################
app.layout = html.Div([
    
        dbc.Row([
                    dbc.Col([
                        html.H4('SYNDROMIC DATA SURVEILLANCE',className='text-center'),
                        html.P('A summary of data from a hospital based surveillance program focused on contributing useful information to the Ministry of Health \
                            to allow for monitoring,planning and mobilizing resources for management and control of COVID-19.')
                    ],md=10)
                ],justify='center'),
        
        dbc.Row([
                html.P('PATIENT DEMOGRAPHY',className=section_title),

                    dbc.Col([
                        dbc.Card([
                            html.Br(),
                            dbc.CardBody([
                                html.H3(total_patients),
                                html.Small("Total Patients",className='card-text'),
                            ]),
                            
                            dbc.CardBody([
                                
                                dmc.RingProgress(
                                    sections=[{'value':male_percentage,'color': male_color}], #
                                    label=dmc.Center(dmc.Text(f'{male_percentage}%',color= fill_color)),#fill_color)),
                                    roundCaps=False,
                                ), 
                                                             
                                html.Small('Male Patients',className='card-text'),
                            ]),                            
                            dbc.CardBody([
                                
                                dmc.RingProgress(
                                    sections=[{'value':female_percentage,'color':female_color}],
                                    label=dmc.Center(dmc.Text(f'{female_percentage}%',color=fill_color)),
                                    roundCaps=False,
                                    
                                    style={"marginLeft":3} #,'width':'25px'
                                ),
                                
                                html.Small('Female Patients',className='card-text'),
                            ],className=''),
                            
                        ],body=True,className='h-100 border-0 text-center'),
                        
                        
                    ],xs=8,sm=3,md=2,lg=2,className='justify-content-center rounded-1'),
                    
                    dbc.Col([                       
                        dbc.Card([
                            html.Br(),
                            html.P('PATIENT DISTRIBUTION BY REGION', className = col_title,style = style_title),
                            html.Br(),
                            dbc.CardBody([
                                dcc.Graph(figure=reg_fig,responsive=True,config=plotly_display,style={"height":"15vh"}),                              
                            ]),
                            html.Br(),
                            html.P('PATIENT DISTRIBUTION BY AGE', className = col_title,style = style_title),
                            dbc.CardBody([                                
                                dcc.Graph(figure=age_plot,responsive=True,config=plotly_display,style={"width":"25hw","height":"30vh"})
                            ])
                        ],className='h-100 border-0 text-center'),
                        
                    ],xs=8,md=5,lg=5,className='rounded-1'),
                    
                    dbc.Col([
                        dbc.Card([
                            html.Br(),
                            html.P('MONTHLY PATIENT DISTRIBUTION BY REGION', className = col_title,style = style_title),
                            dbc.CardBody([
                                dcc.Graph(figure=reg_per_fig,responsive=True,config=plotly_display,style={"height":"30vh"})
                            ]), 
                            
                            html.Br(),
                            html.P('CUMULATIVE NUMBER OF PATIENTS', className = col_title,style = style_title),
                            dbc.CardBody([
                                dcc.Graph(figure=cum_plot,responsive=True,config=plotly_display,style={"height":"30vh"})
                            ])                            
                        ],className='h-100 border-0 text-center rounded-1'),                        
                    ],xs=8,md=5,lg=5,className='rounded-1'),                   
                ],justify = "center",className = classname_col),
        
        dbc.Row([
            html.P('PRESENTING SYMPTOMS AT ADMISSION',className=section_title),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        html.P('SYPMTOMS BY REGION', className = col_title,style = style_title),
                        dbc.CardBody([
                            dcc.Graph(figure = figplot,responsive=True,config=plotly_display,
                                      style={"width":"35vw",'height':'35vh'}) 
                        ])
                    ],className='h-100 border-0 text-center rounded-0')
                ], md=6),
            
                dbc.Col([
                    dbc.Card([
                        html.P('SYMPTOMS BY PERIOD', className = col_title,style = style_title),
                        dbc.CardBody([
                            dcc.Graph(figure=fig_period_heatmap,responsive=True,config=plotly_display,
                                      style={"width":"35vw",'height':'35vh'}) #,"height":"36vh"
                        ])
                    ],className='h-100 border-0 text-center rounded-0')
                ], md=6),
            
            ],justify = "center",className =midrow_classname ),
                    
        ],justify = "center",className = classname_col),
                
        dbc.Row([
            html.P('PRIORITY MEASURES AND VITAL SIGNS',className=section_title),
            
            dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                html.P('COMPLETION OF DEMOGRAPHIC MEASURES', className = col_title,style = style_title),                            
                                dbc.CardBody([
                                    dcc.Graph(figure = fig_demo_heatmap,responsive=True,config=plotly_display,\
                                        style={'width':'35vw','height':'35vh'}),
                                ])
                            ],className='h-100 border-0 text-center rounded-0')
                        ],md=6),
                        
                        dbc.Col([  
                            dbc.Card([
                                html.P('RECORDING OF VITAL SIGNS', className = col_title,style = style_title),                            
                                dbc.CardBody([
                                    dcc.Graph(figure = fig_vital_heatmap,responsive=True,config=plotly_display,
                                              style={'width':'35vw','height':'35vh'})
                                ]) 
                            ],className='h-100 border-0 text-center rounded-0')
                        ],md=6),
                    ],justify = "center", className= midrow_classname),
            
            #-------------------------------------
            #html.Br(className='mb-1'),
            #html.Hr(),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.P('COVID-19 VACCINATION BY REGION', className = col_title,style = style_title),
                            dcc.Graph(figure=fig_cov_vacc_region,responsive=True,config=plotly_display,
                                      style={'height':'20vh'}),#'height':'30vh','width':'35hw'}),
                            html.Br(),
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
                            html.P('HIV STATUS BY PERIOD', className = col_title,style = style_title),
                            dcc.Graph(figure=fig_hiv_period,responsive=True,
                                      config=plotly_display,style={'height':'30vh','width':'35vw'})
                        ])
                    ],className='h-100 border-0 text-center rounded-0')
                ],md=6)
            ],justify = "center",className= midrow_classname),#className = classname_col),
                    
        ],justify = "center",className = classname_col),
        
        dbc.Row([
             dbc.Row([
                html.P('OUTCOME AT DISCHARGE',className=section_title),
                html.Small('Demography of patients at dicharge: Alive or Dead. Click the button  to select \
                    category'),
                dbc.Col([
                    #html.P('Select Category',className='mb-0'),
                    dmc.SegmentedControl(
                        id="segmented",
                        value="Alive",
                        data=[{"value": "Alive", "label": "Alive"},{"value": "Dead", "label": "Dead"}],
                     mt=10,color='red',bg='blue'),
                ],width=3),
            ],justify='start',className='mb-3'),
            html.Div(id='outcome-content'),
            
            html.Hr(className='mt-3'),
    
            # dbc.Row([
            #     html.P('OVERALL SUMMARY AT DISCHARGE',className=section_title),
            #     dbc.Col([
            #         dcc.Graph(figure =status_at_discharge_plot,responsive=True)
            #     ]),
                
                
            # ]),
            
        ],justify = "center",className = classname_col), 

    ],className='ms-5 me-5 mt-4')


#--------------------------------------------------------------------------------------------------------------------
@callback(
    Output('outcome-content','children'),
    Input('segmented','value'))

def return_discharge_data(value):
    
    male_alive = outcome_sex[(outcome_sex['outcome'] == value) & (outcome_sex['sex'] == 'Male')]['prop'].iat[0]
    female_alive = outcome_sex[(outcome_sex['outcome'] == value) & (outcome_sex['sex'] == 'Female')]['prop'].iat[0]
    df_region = outcome_region[(outcome_region['outcome'] == value)]

    df_data = data_campture .loc[(data_campture ['outcome'] == value) & (data_campture ['sex'].isin(['Male','Female'])) & \
         (data_campture ['date_of_admission'] >'2022-12-31' )][['age_groups','region','month','sex','date_of_admission','age_years']]
    
    df_age = df_data[(df_data.age_years > 0) & (df_data.age_years < 100)]
    age_sex = df_age.groupby(['sex','age_groups'])[['sex']].count().rename(columns={'sex':'count'}).reset_index()
    age_sex_f = age_sex[age_sex['sex'] == 'Female']
    age_sex_m = age_sex[age_sex['sex'] == 'Male']
    
    alive_death_period = df_data .groupby(['region','month'])[['region']].count().rename(columns={'region':'count'}).reset_index()
    alive_death_period['proportion'] = round(100 * alive_death_period['count']/alive_death_period.groupby('region')['count'].transform('sum'),1)
    
    #print(alive_death_period)
    age_plot_val = age_gender_plot(age_sex_f,age_sex_m)
    region_fig = plot_figure(df_region)
    alive_death_period_fig =plot_reg_period(alive_death_period)
    
    div = html.Div([
            dbc.Row([
                dbc.Col([
                   
                    dbc.Row([
                        html.Br(),
                        #html.Hr(className=line_class,style = line_style ),
                        html.P(['DISTRIBUTION BY GENDER AND AGE DISCHARGED AS ',html.B(value,className='text-uppercase')], \
                            className = col_title,style = style_title),                            
                        dbc.Col([
                            dbc.CardBody([
                                dmc.RingProgress(
                                    sections=[
                                        {'value':male_alive,'color': male_color},
                                        ], #
                                    label=dmc.Center(dmc.Text(f'{male_alive}%',color= fill_color)),#fill_color)),
                                    roundCaps=False,
                                ), 
                                html.Small('Male '+value,className='card-text'),
                            ]),
                        ],md=5),
                        dbc.Col([
                            
                            dbc.CardBody([
                                dmc.RingProgress(
                                    sections=[{'value':female_alive,'color': female_color}], #
                                    label=dmc.Center(dmc.Text(f'{female_alive}%',color= fill_color)),#fill_color)),
                                    roundCaps=False,
                                ), 
                                html.Small('Female '+value,className='card-text'),
                            ]),
                        ],md=5),
                        
                    ],justify='center g-1'),
               
                    dbc.Row([                         
                        dbc.Col([  
                            html.Br(),html.Br(),
                            dcc.Graph(figure =age_plot_val,responsive=True,config=plotly_display,\
                                style={"height":"35vh",'width':'30vw'}),
                        ],md=10)
                    ],justify='center'),                   
                    
                ],md=6),
                dbc.Col([
                    html.Br(),
                    html.P(['DISTRIBUTION BY REGION AND PERIOD AT DISCHARGED AS ', html.B(value,className='text-uppercase')],\
                        className = col_title,style = style_title), 
                    dcc.Graph(figure = region_fig,responsive=True,config=plotly_display,style={"height":"25vh",'width':'35vw'}),
                    
                    html.Br(),
                    dcc.Graph(figure =alive_death_period_fig,responsive=True,config=plotly_display,style={"height":"30vh",'width':'35vw'}),
                ],md=6),
                
            ],justify='center'),
        ])
    
    return div
app.run_server(mode='jupyterlab',debug=True,host='0.0.0.0',port='7788')
