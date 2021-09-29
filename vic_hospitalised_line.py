#%%

import os
import requests
import pandas as pd
# from modules.yachtCharter import yachtCharter
import datetime
from yachtcharter import yachtCharter

chart_key = 'oz-corona-live-page-hospitalised-percentage-victoria'

print("Checking covidlive")

#%%

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
r = requests.get('https://covidlive.com.au/covid-live.json', headers=headers)

#%%

## Grab Covid Live Data

data = r.json()

df = pd.read_json(r.text)
# 'REPORT_DATE', 'LAST_UPDATED_DATE', 'CODE', 'NAME', 'CASE_CNT',
#        'TEST_CNT', 'DEATH_CNT', 'RECOV_CNT', 'MED_ICU_CNT', 'MED_VENT_CNT',
#        'MED_HOSP_CNT', 'SRC_OVERSEAS_CNT', 'SRC_INTERSTATE_CNT',
#        'SRC_CONTACT_CNT', 'SRC_UNKNOWN_CNT', 'SRC_INVES_CNT', 'PREV_CASE_CNT',
#        'PREV_TEST_CNT', 'PREV_DEATH_CNT', 'PREV_RECOV_CNT', 'PREV_MED_ICU_CNT',
#        'PREV_MED_VENT_CNT', 'PREV_MED_HOSP_CNT', 'PREV_SRC_OVERSEAS_CNT',
#        'PREV_SRC_INTERSTATE_CNT', 'PREV_SRC_CONTACT_CNT',
#        'PREV_SRC_UNKNOWN_CNT', 'PREV_SRC_INVES_CNT', 'PROB_CASE_CNT',
#        'PREV_PROB_CASE_CNT', 'ACTIVE_CNT', 'PREV_ACTIVE_CNT', 'NEW_CASE_CNT',
#        'PREV_NEW_CASE_CNT', 'VACC_DIST_CNT', 'PREV_VACC_DIST_CNT',
#        'VACC_DOSE_CNT', 'PREV_VACC_DOSE_CNT', 'VACC_PEOPLE_CNT',
#        'PREV_VACC_PEOPLE_CNT', 'VACC_AGED_CARE_CNT', 'PREV_VACC_AGED_CARE_CNT',
#        'VACC_GP_CNT', 'PREV_VACC_GP_CNT'

df = df.loc[df['NAME'] == "Victoria"]

#%%

df['REPORT_DATE'] = pd.to_datetime(df['REPORT_DATE'],format="%Y-%m-%d")
df = df.sort_values(by='REPORT_DATE', ascending=True)

updated_date = df['REPORT_DATE'].max()
df['REPORT_DATE'] = df['REPORT_DATE'].dt.strftime("%Y-%m-%d")
# print(df)
updated_date = datetime.datetime.strftime(updated_date, "%d %B %Y")

#%%

zdf = df.copy()

zdf['New_cases'] = zdf['CASE_CNT'].diff(1)
# zdf['New_over_cases'] = zdf['SRC_OVERSEAS_CNT'].diff(1)
# zdf['New_local_cases'] = zdf['New_cases'] - zdf['New_over_cases']




zdf['Local_last_14'] = zdf['New_cases'].rolling(window=14).sum()

zdf['Hospitalised_percent'] = (zdf['MED_HOSP_CNT'] / zdf['Local_last_14'])*100

zdf = zdf[['REPORT_DATE', 'Hospitalised_percent']]

zdf.columns = ['Date', 'Hospitalisation rate']


zdf = zdf.loc[zdf['Date'] > "2021-06-01"]


zdf.fillna('', inplace=True)

print(zdf)

template = [
	{
	"title": "Covid hospitalisation rate in Victoria",
	"subtitle": f"Showing the number of hospitalised Covid cases divided by the number of cases over the previous two weeks, including overseas acquired cases. Last updated {updated_date}.",
	"footnote": "",
	"dateFormat": "%Y-%m-%d",
	"periodDateFormat": "%d/%m",
	"source": "CovidLive.com.au, Guardian analysis",
	"margin-left": "30",
	"margin-top": "30",
	"margin-bottom": "20",
	"margin-right": "10"
	}
]

yachtCharter(template=template, 
			data=zdf.to_dict('records'),
			chartId=[{"type":"linechart"}],
			chartName=f"{chart_key}",
            options=[{"colorScheme":"guardian", "lineLabelling":"FALSE"}])
            