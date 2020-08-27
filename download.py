from datetime import datetime
from uk_covid19 import Cov19API
import pandas as pd

### PHE API stuff
# Specify data to grab
datastructure = {
"Date": "date",
"Area": "areaName",
"Deaths": "newDeaths28DaysByPublishDate",
"Cases": "newCasesByPublishDate"
}

datastructure2 = {
"Area": "areaName",
"Cases": "cumCasesByPublishDate"
}

# Specify region type (nation/region/ltla)
all_uk = [
'areaType=nation'
]

all_ltla = [
'areaType=ltla'
]

# Instantiate API object
phe_api = Cov19API(filters=all_uk, structure=datastructure)
data = phe_api.get_json()

phe_api2 = Cov19API(filters=all_ltla, structure=datastructure2, latest_by="newCasesByPublishDate")
data2 = phe_api2.get_json()

# Specify dataframe
df = data['data'];
# Convert to pandas dataframe
df = pd.DataFrame(df)

df2 = data2['data'];
df2 = pd.DataFrame(df2)

# Save data
df.to_csv('new_cases.csv')
df2.to_csv('cum_cases.csv')
