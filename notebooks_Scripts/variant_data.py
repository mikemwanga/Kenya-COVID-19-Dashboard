#SCRIPT USED TO PROCESS DATA FOR VARIANT PLOTS IN THE VARIANT SECTION OF THE DASHBOARD
#LINK TO VARIANT SECTION : https://kcd.kemri-wellcome.org/apps/variants.html/
#THE VARIANT MAP FILE SHOULD ALWAYS BE UPDATED WITH INFORMATION

#PROCEDURE
#1. DOWNLOAD KENYA DATA FROM GISAID AND EXTRACT THE TAR FILES. DELETE .FASTA AND KEEP .TSV. I ALWAYS LIMIT MY DATA TO JANUARY - DATE 2023.
#2. MAP THE LINEAGES TO WHO ASSIGNED NAMES ALL THE 2023 ARE OMICRONS.
#3. ALD_DATA REFERES TO PREVIOUS UNUPDATED DATASETS
# ENSURE PANDAS IS INSTALLED

import pandas as pd

data = pd.read_table('metadata.tsv',parse_dates=['date'], \
                date_parser=lambda x: pd.to_datetime(x, format='%Y-%m-%d'))

#process lineage data
lineage_data = data[['strain','date','country','division','pangolin_lineage']]
lineage_data = lineage_data[lineage_data['pangolin_lineage'] != 'Unassigned']
lineage_data.to_csv('../data/kenya_lineages3.tsv',sep='\t',index=False)


#process variant data
variant_map = pd.read_table("../data/map_lineages.tsv")
var_type =  dict(zip(variant_map.lineage, variant_map.lineage_group))
old_data = pd.read_table('../data/variant_data_kenya.tsv',parse_dates=['Month'], \
                date_parser=lambda x: pd.to_datetime(x, format='%Y-%m-%d'))


data = data[['strain', 'date','division','pangolin_lineage']]
data['variant'] = 'Omicron'
data = data[data['pangolin_lineage'] != 'Unassigned']
data["lineage_type"] = data["pangolin_lineage"].map(var_type)
data['Month'] =data['date'] - pd.offsets.MonthBegin(1)
data = data[['Month','variant','lineage_type']].groupby(['Month','variant'])[['lineage_type']].count().\
        rename(columns={'lineage_type':'Frequency'}).reset_index()
frequency_per_month = data.groupby('Month')['Frequency'].sum()
data['percentage'] = data.apply(lambda row: row['Frequency']/frequency_per_month[row['Month']], axis=1)

old_data = old_data[old_data['Month'] < '2023-01-01'] #remove all 2023

data = pd.concat([old_data, data],ignore_index=True)

data.to_csv('../data/variant_data_kenya.tsv',sep='\t',index=False)