from datetime import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from uk_covid19 import Cov19API
import pandas as pd


app = dash.Dash(__name__)
server = app.server
app.title = "Covid19 UK Data Graphing"

### PHE API
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

# date formatting
release_timestamp_formatted = release_timestamp.replace('Z', '')
date = datetime.fromisoformat(release_timestamp_formatted)
date_ = date.strftime("%d/%m/%Y, %H:%M")
datestring = "Latest PHE data from ", date_, "."
### end of PHE API

df = data['data'];
# convert to pandas dataframe for rolling avg later
df = pd.DataFrame(df)

fig = px.line(df, x="Date", y="Deaths", color="Area", 
              title="Deaths by Nation", 
              width=800, height=400)

fig.update_layout(hovermode='x')

fig2 = px.line(df, x="Date", y="Cases", color="Area", 
               title="Cases by Nation", 
               width=800, height=400)

fig2.update_layout(hovermode='x')


# 7 day rolling avg deaths
df['Deaths'] = df['Deaths'].rolling(window=7).mean()

fig3 = px.line(df, x="Date", y="Deaths", color="Area", 
               title="Deaths by Nation (7-day rolling average)", 
               width=800, height=400)
fig3.update_layout(hovermode='x')



app.layout = html.Div(children=[
    html.H1(children='Covid19 UK Data Graphing', style={'textAlign': 'center'}),

    html.Div(children='Using Dash, Plotly, and Pandas, with the latest data from Public Health England.', 
             style={'textAlign': 'center'}),

    html.Div(children=datestring, style={'textAlign': 'center'}),
    
    html.Div(children=dcc.Link('View source on GitHub.', href='https://github.com/EddieRowe/covid19-uk-graphing', target='_blank'), style={'textAlign': 'center'}),
    
    dcc.Graph(
        id='chart_cases_line',
        figure=fig2,
        config={
        'displaylogo': False,
        'modeBarButtonsToRemove':['toggleSpikelines', 'zoomIn2d', 'zoomOut2d', 'autoScale2d']
    }
    ),
    
    dcc.Graph(
        id='chart_deaths_line',
        figure=fig,
        config={
        'displaylogo': False,
        'modeBarButtonsToRemove':['toggleSpikelines', 'zoomIn2d', 'zoomOut2d', 'autoScale2d']
        }
    ),
        
    dcc.Graph(
        id='chart_avgdeaths_line',
        figure=fig3,
        config={
        'displaylogo': False,
        'modeBarButtonsToRemove':['toggleSpikelines', 'zoomIn2d', 'zoomOut2d', 'autoScale2d']
        }
    )
    
    
], style={'margin': 'auto', 'width': '50%'})

if __name__ == '__main__':
    app.run_server()
