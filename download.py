from datetime import datetime
from uk_covid19 import Cov19API
import pandas as pd

# Specify data to grab
datastruct = {
"Date": "date",
"Area": "areaName",
"Deaths": "newDeaths28DaysByPublishDate",
"Cases": "newCasesByPublishDate",
"Tests": "newTestsByPublishDate"
}

datastruct2 = {
"Area": "areaName",
"Cases": "cumCasesByPublishDate",
"Rate": "cumCasesByPublishDateRate"
}

datastruct3 = {
"Area": "areaName",
"Cases": "newCasesByPublishDate"
}

# Specify region type (nation/region/ltla)
all_uk = [
'areaType=nation'
]

all_ltla = [
'areaType=ltla'
]

# Instantiate API object
phe_api = Cov19API(filters=all_uk, structure=datastruct)
data = phe_api.get_json()

phe_api2 = Cov19API(filters=all_ltla, structure=datastruct2, latest_by="newCasesByPublishDate")
data2 = phe_api2.get_json()

phe_api3 = Cov19API(filters=all_ltla, structure=datastruct3, latest_by="newCasesByPublishDate")
data3 = phe_api3.get_json()

# Specify dataframe
df = data['data'];
# Convert to pandas dataframe
df = pd.DataFrame(df)

df2 = data2['data'];
df2 = pd.DataFrame(df2)

df3 = data3['data'];
df3 = pd.DataFrame(df3)

# Save data
df.to_csv('new_cases.csv')
df2.to_csv('cum_cases.csv')
df3.to_csv('new_cases_ltla.csv')

# Debug
#for entry in df3['Area'] :
#    print(entry)

#for entry in df2['Area'] :
#    print(entry)
