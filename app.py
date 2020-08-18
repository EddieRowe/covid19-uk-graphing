from datetime import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from uk_covid19 import Cov19API


app = dash.Dash(__name__)
server = app.server

### cov19api

datastructure = {
    "Date": "date",
    "Area": "areaName",
    "Deaths": "newDeaths28DaysByPublishDate",
    "Cases": "newCasesByPublishDate"
}

all_uk = [
    'areaType=nation'
]

# Instantiating the API object
api = Cov19API(filters=all_uk, structure=datastructure)

data = api.get_json()

# latest website update
release_timestamp = Cov19API.get_release_timestamp()

# format it
release_timestamp_formatted = release_timestamp.replace('Z', '')
date = datetime.fromisoformat(release_timestamp_formatted)
date_ = date.strftime("%d/%m/%Y, %H:%M")
datestring = "Public Health England data, last updated ", date_, "."
### end cov19api

df = data['data'];


fig = px.line(df, x="Date", y="Deaths", color="Area")
fig2 = px.line(df, x="Date", y="Cases", color="Area")

app.layout = html.Div(children=[
    html.H1(children='Covid19 UK Data.'),

    html.Div(children=datestring),
    html.Div(children='Using Dash, Plotly.py, Pandas, and PHE datasets.'),
    
    dcc.Graph(
        id='chart_cases_line',
        figure=fig2
    ),
    
    dcc.Graph(
        id='chart_deaths_line',
        figure=fig
    )
    
])

if __name__ == '__main__':
    app.run_server(debug=True)
