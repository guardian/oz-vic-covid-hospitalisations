#%%

import os
import requests
import pandas as pd
from yachtcharter import yachtCharter
import datetime
chart_key = "oz-covid-icu-capacity-victoria"

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

df = df.loc[df['CODE'] == "VIC"]

df = df.loc[df['REPORT_DATE'] >= "2021-08-01"].copy()

#%%
df = df[['REPORT_DATE','MED_ICU_CNT']]

df.columns = ['Date', 'ICU number']
# print(df)


today = datetime.datetime.today()
today = datetime.datetime.strftime(today, "%Y-%m-%d")
startDate = '2021-08-01'

twenty_five = 437*0.25
fifty = 437*0.5

thresholds = [
	{"y1":twenty_five,"y2":twenty_five,"x1":startDate, "x2":today, "text":"Quarter"},
	{"y1":fifty,"y2":fifty,"x1":startDate, "x2":today, "text":"Half"},
	{"y1":437,"y2":437,"x1":startDate, "x2":today, "text":"Full"},
	]

# %%


df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values(by='Date', ascending=True)

updated_date = df['Date'].max()
df['Date'] = df['Date'].dt.strftime("%Y-%m-%d")
# print(df)
updated_date = datetime.datetime.strftime(updated_date, "%-d %B %Y")


template = [
	{
	"title": "Covid ICU numbers in Victoria v ICU capacity",
	"subtitle": f"Showing the number of Covid cases in ICU over time, along with thresholds based on stated ICU capacity. Last updated {updated_date}.",
	"footnote": "",
    "dateFormat": "%Y-%m-%d",
	"source": "<a href='https://covidlive.com.au/' target='_blank'>Covidlive.com.au</a>",
	"margin-left": "50",
	"margin-top": "30",
	"margin-bottom": "20",
	"margin-right": "10",
    "maxY": "500"
	}
]

yachtCharter(template=template, 
			data=df.to_dict('records'),
			chartId=[{"type":"linechart"}],
            lines= thresholds,
			chartName=f"{chart_key}",
            options=[{"colorScheme":"guardian", "lineLabelling":"Tr"}])