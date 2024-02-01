from utils import *

data = pd.read_csv(DATA_PATH.joinpath('Syndromic_Surveillance_data_2023_12_18.csv'),low_memory=False)
data[['date_of_admission', 'date_of_discharge']] = data[['date_of_admission', 'date_of_discharge']].\
                                apply(pd.to_datetime, format="%Y-%m-%d")
data[(data['sex'] != 'Male') & (data['sex'] != 'Female')]
data = data[data['date_of_admission'] >= '2023-04-01']
# data.age.fillna(data.calculated_age,inplace=True)
data['month'] = data['date_of_admission'].apply(lambda x: x.strftime('%b-%y'))

#map regions
map_dict = {
'JOOTRH':'Western','Naivasha':'Central', 'Kiambu':'Central', 'Machakos':'Central','Mama Lucy':'Central',
'Mbagathi':'Central', 'Kerugoya':'Central', 'Kisumu':'Western', 'Kakamega':'Western', 'Busia':'Western', 'Kitale':'Western',
'Bungoma':'Western', 'Kisii':'Western', 'CGTRH':'Coast', 'Kilifi':'Coast',
'Jaramogi Oginga Odinga Teaching and Referral Hospital' : 'Western','Naivasha County Referral Hospital':'Central',
'Kiambu Level 5 Hospital':'Central','Machakos Level 5 Hospital':'Central',
'Mama Lucy Kibaki Hospital':'Central', 'Mbagathi Hospital':'Central',
'Kerugoya County Referral Hospital':'Central',
'Coast General Teaching and Referral Hospital':'Coast','Kisumu County Hospital':'Western',
'Kakamega County General & Teaching Referral Hospital':'Western',
'Busia County Referral Hospital':'Western',
'Kitale County Referral Hospital':'Western','Bungoma County Hospital':'Western',
'Kisii Teaching and Referral Hospital':'Western'}

data['region'] = data['hospital'].map(map_dict)
central = '#794d65'
western='#c39054'
coast = '#3182bd'

title_font = 15
tick_font = 14
data['region'] = data['hospital'].map(map_dict)

#group age groups
def age_group(dataframe,column):
        '''Function to generate age groups. returns age groups column in the data frame'''
        dataframe['age_groups'] = pd.cut(dataframe[column],
                                       [0,17,20,30,40,50,60,100],
                                       labels = ['10-17','18-20','21-30','31-40','41-50','51-60','>60'])
        return dataframe
data = age_group(data,'age')
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

titlefont = {"size":14}
reg_data = data[['record_id','date_of_admission','hospital','sex','age','region','age_groups','month','outcome',
                 'status_at_discharge','date_of_discharge']]

df_all = data.loc[(data['sex'].isin(['Male','Female'])) & (data['date_of_admission'] >='2023-04-01' )]\
    [['age_groups','month','sex','date_of_admission','age']]
df_age = df_all[(df_all.age > 10) & (df_all.age < 100)]
age_sex = df_age.groupby(['sex','age_groups'])[['sex']].count().rename(columns={'sex':'count'}).reset_index()
age_sex_f = age_sex[age_sex['sex'] == 'Female']
age_sex_f['prop'] = round(age_sex_f['count']/age_sex_f['count'].sum()*100,0)
age_sex_m = age_sex[age_sex['sex'] == 'Male']
age_sex_m['prop'] = round(age_sex_m['count']/age_sex_m['count'].sum()*100,0)
# print(age_sex_m)

def age_gender_plot(male_data,female_data):
    age_plot= go.Figure()
    age_plot.add_trace(go.Bar(y = female_data["age_groups"], x = female_data["prop"]*-1, orientation="h",name = "Female",
                            marker=dict(color=female_color)))
    age_plot.add_trace(go.Bar(y = male_data["age_groups"], x = male_data["prop"], orientation="h",name = "Male",
                            marker=dict(color=male_color)))
    age_plot.update_layout(barmode = "relative",bargap = 0.5,bargroupgap=0,
                            xaxis =  dict(tickvals = [-60,-40,-20,0,20,40,60],
                                            ticktext = ["60","40","20","0","20","40","60"]),
                            legend = dict(orientation = "h",title=None,yanchor='top',y=1.2,xanchor='right',x=1),
                            margin=margin,paper_bgcolor=plot_color,plot_bgcolor=plot_color),
    age_plot.update_traces(width=0.5)
    age_plot.update_yaxes(tickfont = dict(size=tick_font),title ='Age in Years',title_font = titlefont,
                          ticks='outside',linecolor= linecolor)
    age_plot.update_xaxes(tickfont = dict(size=tick_font),title = 'Proportion(%)',gridcolor=gridcolor, 
                          linecolor=linecolor,ticks='outside',nticks=20)
    return age_plot

age_plot = age_gender_plot(age_sex_f,age_sex_m)

df = reg_data.groupby(['region','sex'])[['sex']].count().rename(columns={'sex':'count'}).reset_index()
df['gender_proportion'] = df['count'].apply(lambda x: x*100/df['count'].sum())

reg_fig = px.bar(df, y='region',x='gender_proportion', color='sex',barmode='group',range_x=([0,100]),
                 color_discrete_sequence= gender_color,text='count')
reg_fig.update_traces(textposition='outside',textfont_size=12)
reg_fig.update_layout(margin=margin,legend=dict(orientation='h',title=None,yanchor='top',y=1,xanchor='right',x=1),
                      uniformtext_minsize=7, uniformtext_mode='hide',paper_bgcolor=plot_color,plot_bgcolor=plot_color)
reg_fig.update_yaxes(tickfont = dict(size=tick_font),title = None,ticks='outside',linecolor= linecolor)
reg_fig.update_xaxes(title ='Proportion(%)',nticks=10, tickfont = dict(size=tick_font),linecolor= linecolor,gridcolor=gridcolor,
                     ticks='outside')
reg_period = reg_data.groupby(['region','month'])[['region']].count().rename(columns={'region':'count'}).reset_index()
reg_period['proportion'] = round(100 * reg_period['count']/reg_period.groupby('region')['count'].transform('sum'),1)
reg_period['month']=pd.to_datetime(reg_period['month'], format="%b-%y").sort_values()

# print(reg_period)
def plot_reg_period(data):
    fig = px.bar(data, x='month',y='count',barmode='group',color='region',range_y=[0, data['count'].max()+200],
                        color_discrete_sequence= discrete_color,text = 'count')
    fig.update_xaxes(categoryorder='array')#,categoryarray=['Jan-23','Feb-23','Mar-23','Apr-23','May-23','Jun-23'])
    fig.update_layout(margin=margin,legend=dict(orientation='h', title=None,yanchor='top',y=1.2,xanchor='right',x=1),
                      paper_bgcolor=plot_color,plot_bgcolor=plot_color)
    fig.update_xaxes(tickfont = dict(size=12),title=None,linecolor='gray',nticks=20,ticks='outside',tickformat='%b-%y')
    fig.update_yaxes(tickfont = dict(size=12),nticks=8,title='Frequency',linecolor= linecolor,gridcolor=gridcolor,ticks='outside')
    fig.update_traces(textposition='outside',textfont_size=12)
    return fig
reg_per_fig =plot_reg_period(reg_period)

####################################################################################################
#data captured
data_campture = data[['record_id','dob_known','date_of_entry','biodata_complete','sex','age','region','age_groups','month',\
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
age_complete = group_between('age',18,100)
# bp_dialysis = group_between('blood_pressure_dia',50,200)
# bp_systolic = group_between('blood_pressure_sys',50,200)

df_demo = pd.merge(dob_known,sex_complete,on='region').\
    merge(height_complete,on='region').\
        merge(weight_complete,on='region').\
            merge(age_complete,on='region')
df_demo.set_index('region',inplace=True)
df_demo = (df_demo.div(total_patients)*100).round(1)

df_vital_signs = pd.merge(temp,resp_rate,on='region').\
    merge(heart_rate,on='region').\
        merge(oxy_rate,on='region')#.\
            # merge(bp_dialysis,on='region').\
            #     merge(bp_systolic,on='region')
                
df_vital_signs.set_index('region',inplace=True)
df_vital_signs = (df_vital_signs.div(total_patients)*100).round(1)

#heatmap plot
def heatmap_plot(data,yname):
    fig = px.imshow(data,text_auto=True,aspect="auto",range_color=(0,100),
                    color_continuous_scale=px.colors.sequential.amp)#PuBu)amp
    fig.update_layout(margin=margin)
    fig.update_yaxes(title=yname,title_font=titlefont)
    fig.update_xaxes(title=None,side='top', gridcolor='gray',ticks='outside')
    fig.update_coloraxes(colorbar={'title':'Proportion(%)','orientation':'h', 'thickness':7, 'y':-0.4, 'titleside':'bottom'})
    fig.update_traces(ygap=1,xgap=1)

    return fig

fig_demo_heatmap = heatmap_plot(df_demo.T,'Variable')
fig_vital_heatmap = heatmap_plot(df_vital_signs.T,'Vital Signs')

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
    fig.update_xaxes(title='Proportion(%)',title_font=titlefont,gridcolor=gridcolor,ticks='outside')
    fig.update_yaxes(title=yaxis,title_font=titlefont,ticks='outside')
    fig.update_yaxes(categoryorder='array',categoryarray=['Jan-23','Feb-23','Mar-23','Apr-23','May-23','Jun-23'])
    fig.update_layout(barmode='stack',margin=margin,
                      legend=dict(title=None,orientation='h',yanchor='top',y=1.5,x=0))
    return fig
                         
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

symp_data.rename(columns={'loss_of_consciousness':'LoC'},inplace=True)

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
figplot.update_yaxes(tickfont = dict(size=tick_font),title = 'Symptoms',title_font = titlefont,ticks='outside')
figplot.update_xaxes(tickfont = dict(size=tick_font),title = "Proportion(%)",ticks='outside',
                     gridcolor=gridcolor,title_font = titlefont,linecolor=linecolor)

#***************************************************
documentation_data = data[['record_id','region','month','temp','blood_pressure_sys','resp_rate','oxygen_sat','heart_rate']]
monthly_records = documentation_data[['record_id','month']].groupby('month')[['record_id']].count()
temp = documentation_data[['month','temp']].replace(-1,None).groupby('month')['temp'].count()
blood_pressure = documentation_data[['month','blood_pressure_sys']].replace(-1,None).groupby('month')['blood_pressure_sys'].count().reset_index()
resp_rate = documentation_data[['month','resp_rate']].replace(-1,None).groupby('month')['resp_rate'].count().reset_index()
oxygen_sat = documentation_data[['month','oxygen_sat']].replace(-1,None).groupby('month')['oxygen_sat'].count().reset_index()
heart_rate = documentation_data[['month','heart_rate']].replace(-1,None).groupby('month')['heart_rate'].count().reset_index()
documentation = pd.merge(monthly_records, temp,on='month' ).merge(blood_pressure, on='month', how='outer').\
            merge(resp_rate, on='month',how='outer').\
            merge(oxygen_sat,on='month',how='outer').merge(heart_rate,on='month',how='outer')
documentation.set_index('month', inplace=True)
div_col = 'record_id'
rename_dictionary = {'temp':'Temperature','resp_rate':'Respiratory rate','oxygen_sat':'Oxygen rate',
                              'heart_rate':'Heart rate','blood_pressure_sys':'Blood Pressure'}
for col in ['temp','resp_rate','oxygen_sat', 'blood_pressure_sys','heart_rate']:
    documentation[col] = round(documentation[col]/documentation[div_col] * 100,1)
documentation.drop(columns = 'record_id', inplace=True)
documentation.index = pd.to_datetime(documentation.index, format="%b-%y")
documentation.sort_index(inplace=True)
documentation = documentation.rename(columns=rename_dictionary)
def plot_line_documentation(data,columns,colorpattern):
    '''Function to plot line graphs'''
    fig = px.line(data, x=data.index, y = columns, range_y=(0,105),markers=True,
                  color_discrete_map=colorpattern)
    fig.update_xaxes(tickformat='%b-%y', color='black', linecolor='black', ticks='outside',gridcolor=gridcolor,nticks=15,
                 tickfont = dict(size=14),title=None)
    fig.update_yaxes(ticks='outside',color='black',tickfont = dict(size=14),linecolor='black',title='Documentation(%)',
                 title_font=dict(size=16))
    fig.update_layout(margin=margin, legend=dict(orientation='h',title=None, y=-0.3))
    return fig

colnames = ['Temperature','Respiratory rate','Oxygen rate','Heart rate','Blood Pressure']
documentation_color = {'Temperature':'#1f78b4','Blood Pressure':'#ff7f00', 
                       'Respiratory rate':'#33a02c','Oxygen rate':'#e31a1c','Heart rate':'#6a3d9a'}
documentation_plot = plot_line_documentation(documentation,colnames,
                        documentation_color )
#**********************************************************************************
#DOCUMENTATION BY REGION**
region = data[['record_id','region','month']].groupby(['month','region'])[['record_id']].count().\
    rename(columns={'record_id':'Freq'}).reset_index()
region = region.pivot_table(values='Freq',index='month',columns='region').rename_axis(None,axis=1).reset_index()
region.set_index('month',inplace=True)

# print(region)
def region_summary(region_name):
    region_data = documentation_data[documentation_data['region'] == region_name].replace(-1, None)\
        [['record_id','month','temp','blood_pressure_sys','resp_rate','oxygen_sat','heart_rate']].\
            groupby(['month'])[['temp','blood_pressure_sys','resp_rate','oxygen_sat','heart_rate']].count()
    for col in region_data.columns:
        region_data [col] = round(region_data [col]/region[region_name]*100,1)
    
    region_data.index = pd.to_datetime(region_data.index, format="%b-%y").sort_values()

    return region_data

coast = region_summary('Coast').rename(columns =rename_dictionary)
western = region_summary('Western').rename(columns =rename_dictionary)
central = region_summary('Central').rename(columns =rename_dictionary)

tempcolor = documentation_color['Temperature']
oxycolor = documentation_color['Oxygen rate']
respcolor =  documentation_color['Respiratory rate']
heartcolor =  documentation_color['Heart rate']
bloodcolor = documentation_color['Blood Pressure']
# def region_plot():
#     fig = make_subplots(rows=1, cols=3, shared_yaxes=False,y_title='Documentation(%)',
#                         subplot_titles=('Coast','Western','Central'))
#     fig.add_trace(go.Scatter(x = coast.index, y=coast['Temperature'],name = 'Temperature',
#                             marker_color = tempcolor),row=1, col=1)
#     fig.append_trace(go.Scatter(x = coast.index, y=coast['Oxygen rate'],name = 'Oxygen rate',
#                                 marker_color =oxycolor ),row=1, col=1)
#     fig.append_trace(go.Scatter(x = coast.index, y=coast['Respiratory rate'],name = 'Respiratory rate',
#                                 marker_color = respcolor),row=1, col=1)
#     fig.append_trace(go.Scatter(x = coast.index, y=coast['Heart rate'],name = 'Heart rate',
#                                 marker_color =heartcolor ),row=1, col=1)
#     fig.append_trace(go.Scatter(x = coast.index, y=coast['Blood Pressure'],name = 'Blood Pressure',
#                                 marker_color = bloodcolor),row=1, col=1)

#     fig.add_trace(go.Scatter(x = western.index, y=western['Temperature'],showlegend=False,
#                             marker_color = tempcolor),row=1, col=2)
#     fig.append_trace(go.Scatter(x = western.index, y=western['Oxygen rate'],showlegend=False,
#                                 marker_color =oxycolor),row=1, col=2)
#     fig.append_trace(go.Scatter(x = western.index, y=western['Respiratory rate'],showlegend=False,
#                                 marker_color =respcolor),row=1, col=2)
#     fig.append_trace(go.Scatter(x = western.index, y=western['Heart rate'],showlegend=False,
#                                 marker_color =heartcolor),row=1, col=2)
#     fig.append_trace(go.Scatter(x = western.index, y=western['Blood Pressure'],showlegend=False,
#                                 marker_color =bloodcolor),row=1, col=2)

#     fig.add_trace(go.Scatter(x = central.index, y=central['Temperature'],showlegend=False,
#                             marker_color = tempcolor),row=1, col=3)
#     fig.append_trace(go.Scatter(x = central.index, y=central['Oxygen rate'],showlegend=False,
#                                 marker_color = oxycolor),row=1, col=3)
#     fig.append_trace(go.Scatter(x = central.index, y=central['Respiratory rate'],showlegend=False,
#                                 marker_color = respcolor),row=1, col=3)
#     fig.append_trace(go.Scatter(x = central.index, y=central['Heart rate'],showlegend=False,
#                                 marker_color = heartcolor),row=1, col=3)
#     fig.append_trace(go.Scatter(x = central.index, y=central['Blood Pressure'],showlegend=False,
#                                 marker_color = bloodcolor ),row=1, col=3)
#     fig.update_layout(margin=dict(r=8,b=2,t=20),
#                       legend = dict(orientation='h',y=-0.3))#l=10, r=10, t=5, b=5))
#     fig.update_xaxes(tickformat='%b-%y',linecolor=linecolor,ticks='outside')
#     fig.update_yaxes(nticks=10, range=[0,105],gridcolor=gridcolor,linecolor=linecolor,ticks='outside')
    
#     return fig

# region_documentation_plot = region_plot()

def plot_line_documentation_region(data,columns,colorpattern):
    '''Function to plot line graphs'''
    fig = px.line(data, x=data.index, y = columns, range_y=(0,105),markers=True,
                  color_discrete_map=colorpattern)
    fig.update_xaxes(tickformat='%b-%y', color='black', linecolor='black', ticks='outside',
                     gridcolor=gridcolor,nticks=5,
                 tickfont = dict(size=14),title=None)
    fig.update_yaxes(ticks='outside',color='black',tickfont = dict(size=14),linecolor='black',title='Documentation(%)',
                 title_font=dict(size=16))
    fig.update_layout(margin=margin, showlegend=False)#, legend=dict(orientation='h',title=None))
    return fig

coast_documentation_plot = plot_line_documentation_region(coast, colnames,
                        documentation_color)
central_documentation_plot = plot_line_documentation_region(central, colnames,
                        documentation_color)
western_documentation_plot = plot_line_documentation_region(western, colnames,
                        documentation_color)
#**********************************************************************************
#SET DATA FOR WEIGHT AND HEIGHT PLOT
documentation_color = {'height':'#1f78b4','weight':'#ff7f00'}
demo_dcm = data[['record_id','month','weight','height']]
weight = demo_dcm[demo_dcm['weight'] > 1][['month','weight']]
weight = weight.groupby('month')['weight'].count().reset_index()
height = demo_dcm[demo_dcm['height'] > 1][['month','height']]
height = height.groupby('month')['height'].count().reset_index()
demographic_documentation = pd.merge(monthly_records, height, on='month',how='outer').merge(weight, on='month',how='outer')

for col in ['weight','height']:
    demographic_documentation[col] = round(demographic_documentation[col]/demographic_documentation['record_id']*100,1)

demographic_documentation.set_index('month',inplace=True)
demographic_documentation.index = pd.to_datetime(demographic_documentation.index, format="%b-%y").sort_values()

demographic_documentation_plot = plot_line_documentation(demographic_documentation,['weight','height'],documentation_color )

#**************************************************************************

priority_measure_df = data[['record_id','month','hiv_status','received_covid_19_vaccine','chronic_illness']].fillna(0)#.set_index('record_id')
priority_measure_df['hiv_status'] = priority_measure_df['hiv_status'].\
    map({'Positive':1,'Unknown':1,'Negative':1,'Empty':None,0:None})
priority_measure_df['received_covid_19_vaccine'] = priority_measure_df['received_covid_19_vaccine'].\
    map({'Yes':1,'No':1,'Indeterminate':1,'Empty':None,0:None})
priority_measure_df['chronic_illness'] = priority_measure_df['chronic_illness'].\
    map({'Yes':1,'No':1,'Empty':None,0:None})
priority_measure_df =  priority_measure_df.groupby('month')[['record_id','hiv_status','received_covid_19_vaccine','chronic_illness']].count()
for col in ['hiv_status','received_covid_19_vaccine','chronic_illness']:
    priority_measure_df[col] = round(priority_measure_df[col]/priority_measure_df['record_id'] *100,1)
priority_measure_df.index= pd.to_datetime(priority_measure_df.index, format="%b-%y").sort_values()
priority_measure_df.rename(columns = {'hiv_status':'HIV status','received_covid_19_vaccine':'COVID Vaccination',
                                      'chronic_illness':'Comorbodities'}, inplace=True)

priority_color = color_discrete_map={'HIV status':'#1f78b4','COVID Vaccination':'#ff7f00','Comorbodities':'#6a3d9a'}
priority_measure_df_plot = plot_line_documentation(priority_measure_df,['HIV status','COVID Vaccination','Comorbodities'],priority_color )
#*********************************************************************************************************************

outcome_data = data[['record_id','month','outcome','sex','age','region']].set_index('record_id')

outcome_deaths  = outcome_data[outcome_data['outcome'] == 'Dead']
outcome_deaths['month']= pd.to_datetime(outcome_deaths['month'], format="%b-%y").sort_values()
outcome_deaths_sex = outcome_deaths[['month','sex']].groupby(['sex','month'])[['sex']].count().rename(columns={'sex':'Freq'}).reset_index()
outcome_deaths_sex['month']= pd.to_datetime(outcome_deaths_sex['month'], format="%b-%y").sort_values()

outcome_deaths_region = outcome_deaths[['month','region']].groupby(['region','month'])[['region']].count().\
                        rename(columns={'region':'Freq'}).reset_index()

def plot_stack_bar(data,color_col,color_pattern):
    fig = px.bar(data, x = 'month', y='Freq',color=color_col)
    fig.update_xaxes(tickformat='%b-%y', color='black', linecolor='black', ticks='outside',
                 tickfont = dict(size=tick_font),title=None,nticks=20)
    fig.update_yaxes(ticks='outside',color='black',tickfont = dict(size=tick_font),linecolor='black',title='Counts',
                 title_font=dict(size=16))
    fig.update_layout(margin=margin,width=600,legend=dict(orientation='h',title=None, xanchor='left',x=0.3))
    return fig

outcome_death_sex_color = {'Male':male_color,'Female':female_color}
outcome_deaths_region_color = {'Central':central, 'Western':western,'Coast':coast}
outcome_death_sex_plot = plot_stack_bar(outcome_deaths_sex, 'sex', outcome_death_sex_color)
outcome_deaths_region_plot = plot_stack_bar(outcome_deaths_region, 'region', outcome_deaths_region_color)

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
    fig.update_xaxes(title='Proportion(%)',title_font=titlefont,gridcolor=gridcolor,ticks='outside')
    fig.update_yaxes(title=yaxis,title_font=titlefont,ticks='outside')
    fig.update_yaxes(categoryorder='array',categoryarray=['Jan-23','Feb-23','Mar-23','Apr-23','May-23','Jun-23'])
    fig.update_layout(barmode='stack',margin=margin,
                      legend=dict(title=None,orientation='h',yanchor='top',y=1.5,x=0))
    return fig
                         
fig_cov_vacc_region = priority_plot(cov_vaccine_region,'received_covid_19_vaccine','region')
fig_cov_vacc_month = priority_plot(cov_vaccine_month,'received_covid_19_vaccine','month')

fig_hiv_region = priority_plot(hiv_data_region,'hiv_status','region')
fig_hiv_period = priority_plot(hiv_data_month,'hiv_status','month')
#*********************************************************************************************************************
layout = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Row([
                    dbc.Col([
                    html.H4('Adult Syndromic Surveillance',className = col_title),
                    html.Hr(),
                    html.P('A summary of data from a hospital based surveillance program focused on contributing useful information to the Ministry of Health \
                                to allow for monitoring,planning and mobilizing resources for management and control of COVID-19. Data was collected between January to December 2023.')
                    ],md=11)
            ],justify="center"),#, className = "mb-2 ms-4 me-4 ps-4 pe-4 mt-5 pt-5"

            dcc.Tabs([
                dcc.Tab([
                    dbc.Row([
                        # html.P('PATIENT DEMOGRAPHY',className=section_title),
                        html.P('Summary of patients admitted in all health facilities during the study period'),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H3(total_patients),
                                    dmc.Space(h=45),
                                    html.Small("Total Patients",className='card-text, mt-0'),
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
                        # html.Hr(className='mt-0'),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                
                                html.P('PATIENT DISTRIBUTION BY REGION', className = col_title,style = style_title),
                                html.Br(className='mt-5'),
                                # dbc.CardBody([
                                    dcc.Graph(figure=reg_fig,responsive=True,config=plotly_display,style={"height":"25vh"} ),     #                        
                                # ]),
                            ],className='h-100 border-0 text-center',style={'align-items':'bottom'}), 
                        ]),
                        dbc.Col([
                            dbc.Card([
                                
                                html.P('PATIENT DISTRIBUTION BY AGE', className = col_title,style = style_title),
                                html.Br(),
                                # dbc.CardBody([                                
                                    dcc.Graph(figure=age_plot,responsive=True,config=plotly_display,style={"height":"30vh"})
                                # ])
                            ],className='h-100 border-0 text-center'), #border-0
                        ]),
                        html.Hr(className='mb-2 mt-2'),
                    ]),
                    dbc.Row([
                        dbc.Card([
                            html.Br(),
                            html.P('MONTHLY PATIENT DISTRIBUTION BY REGION', className = col_title,style = style_title),
                            dbc.CardBody([
                                dcc.Graph(figure=reg_per_fig,responsive=True,config=plotly_display,
                                          style={"height":"45vh"})
                            ]),                           
                        ],className='h-100 border-0 text-center'),
                        html.Hr(),
                    ]),
                ],label='Patient Demography',style=tab_style,selected_style=tab_selected_style),

                dcc.Tab([
                    html.Br(className='mt-2'),
                    dbc.Row([
                        html.Br(className='mt-2'),
                        html.P('DOCUMENTATION OF PRIORITY MEASURES',className=section_title),
                        html.P('Summary of documentation of temperature,respiratory rate, oxygen rate, heart rate and blood pressure\
                                   on patient cards'),
                        html.P('Countrywide Documentation'),
                        dbc.CardBody([
                                dcc.Graph(figure=documentation_plot,responsive=True,config=plotly_display,style={"height":"35vh"} ), 
                        ]),
                    ]),

                    # dbc.Row([
                    #     html.P('Regional Documentation'),
                    #     dbc.Col([
                    #         dbc.CardBody([
                    #             dcc.Graph(figure=region_documentation_plot,responsive=True,config=plotly_display,style={"height":"45vh"} ), 
                    #         ]),
                    #     ])
                    # ], className = 'mt-2'),

                    dbc.Row([
                        html.P('Regional Documentation'),
                        dbc.Col([
                            dbc.CardBody([
                                dcc.Graph(figure=coast_documentation_plot,responsive=True,config=plotly_display,
                                          style={"height":"30vh"} ), 
                            ]),
                        ]),
                        dbc.Col([
                            dbc.CardBody([
                                dcc.Graph(figure=western_documentation_plot,responsive=True,config=plotly_display,
                                          style={"height":"30vh"} ), 
                            ]),
                        ]),
                        dbc.Col([
                            dbc.CardBody([
                                dcc.Graph(figure=central_documentation_plot,responsive=True,config=plotly_display,
                                          style={"height":"30vh"} ), 
                            ]),
                        ])
                    ], className = 'mt-2'),

                    html.Hr(),

                    
                    
                ],label='Vitals',style=tab_style,selected_style=tab_selected_style),
                dcc.Tab([
                    dbc.Card([
                            html.P('Summary of documentation of weight and height on patient cards'),
                            dbc.CardBody([
                                dcc.Graph(figure=demographic_documentation_plot,responsive=True,config=plotly_display,style={"height":"50vh"} ), 
                            ]),
                            html.Hr(),
                    ],className='border-0 text-start',style={"width": "80rem"}),
                ],label='Demographic Measures',style=tab_style,selected_style=tab_selected_style),
                dcc.Tab([
                    dbc.Row([
                        
                        dbc.Card([
                            html.P('Summary of documentation of patient HIV status, COVID-19 vaccination status other \
                                   comorbidities on patient cards'),
                            dbc.CardBody([
                                dcc.Graph(figure=priority_measure_df_plot,responsive=True,config=plotly_display,style={"height":"40vh"} ), 
                            ])
                        ],className='border-0 text-center',style={"width": "80rem"}),
                    ])  ,
                    dbc.Row([
                        html.Hr(),
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
                        ],md=6),

                        html.Hr(),
                    ],justify = "center",className= midrow_classname),
                ],label='Priority Measures',style=tab_style,selected_style=tab_selected_style),
                dcc.Tab([
                    dbc.Row([
                        html.Br(className='mt-2'),
                        html.P('TRENDS IN MORTALITY ACROSS THE HEALTH FACILITIES',className=section_title),
                        dbc.Col([

                            html.P('Trends in mortality by sex'),

                            dcc.Graph(figure=outcome_death_sex_plot,responsive=True,config=plotly_display,
                                          style={"height":"40vh"} )
                        ],md=6,className=''),


                        dbc.Col([
                            html.P('Trends in mortality by region'),
                            dcc.Graph(figure=outcome_deaths_region_plot,responsive=True,config=plotly_display,
                                      style={"height":"40vh"} ), 

                        ],md=6,className='')
                    ],justify='between')


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
    ],justify='center')

],className='ms-5 me-5 mt-4')