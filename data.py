from utils import *

import schedule
import time

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("./data/").resolve()

def load_dataset():
    daily_updates_moh =  pd.read_excel(DATA_PATH.joinpath("daily_updates_metadata.xlsx"))
    county_daily_updates = pd.read_excel(DATA_PATH.joinpath("county_daily_updates.xlsx"), parse_dates=["Date"], index_col='Date')
    data = pd.read_csv(DATA_PATH.joinpath("cases_per_county.csv"))
    data["percentage_cases"] = round(data["cases"]/data["cases"].sum() * 100,2)
    county_prevalence = pd.read_csv(DATA_PATH.joinpath("cases_per_county.csv"))
    daily_cases = pd.read_csv(DATA_PATH.joinpath("covid_daily_data.csv"))
    daily_cases["Date"] = pd.to_datetime(daily_cases["Date"],format = "%d/%m/%Y")
    age_gender_data = pd.read_table(DATA_PATH.joinpath("age_gender_data.txt"),sep = "\t")
    
    return daily_updates_moh, county_daily_updates,data,daily_cases,age_gender_data,county_prevalence

daily_updates_moh, county_daily_updates,data,daily_cases,age_gender_data,county_prevalence = load_dataset()

# schedule.every(2).seconds.do(load_dataset)

# while True:
#     schedule.run_pending()
#     time.sleep(1)
    
    
# layout = html.Div([
            
#     html.Div(id = "home-content"),
    
#     dcc.Interval(
#             id='interval',
#             interval= 43200 * 1000, # in milliseconds update every 12 hrs
#             n_intervals=0,
#                 ),
# ])

# @app.callback(
#         Output("home-content","children"),
#         Input("interval", "n_intervals")
# )

# def update_content(n):
    
#     daily_updates_moh, county_daily_updates, data, county_prevalence,daily_cases,age_gender_data = load_data()