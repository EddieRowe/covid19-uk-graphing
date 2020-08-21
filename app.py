from datetime import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from uk_covid19 import Cov19API
import pandas as pd

app = dash.Dash(__name__)
server = app.server
app.title = "COVID-19 UK Data Graphing"
   

### PHE API stuff
# specify data to grab
datastructure = {
    "Date": "date",
    "Area": "areaName",
    "Deaths": "newDeaths28DaysByPublishDate",
    "Cases": "newCasesByPublishDate"
}

# specify region type (nation/region/ltla)
all_uk = [
    'areaType=nation'
]

# Instantiate API object
phe_api = Cov19API(filters=all_uk, structure=datastructure)
data = phe_api.get_json()

# latest website update
release_timestamp = Cov19API.get_release_timestamp()

# date formatting
release_timestamp_formatted = release_timestamp.replace('Z', '')
date = datetime.fromisoformat(release_timestamp_formatted)
date_time = date.strftime("%d/%m/%Y, %H:%M")
date_ = date.strftime("%d-%m-%Y")
datestring = "Latest PHE data from ", date_time, " GMT."
### end of PHE API stuff

# specify dataframe
df = data['data'];
# convert to pandas dataframe
df = pd.DataFrame(df)


# line graph of deaths by date
fig = px.line(df, x="Date", y="Deaths", color="Area", 
              title="Deaths by Nation", 
              width=600, height=350,
              template="plotly_dark"
)

# set style elements
fig.update_layout(hovermode='x unified', 
                  plot_bgcolor='#232627', 
                  paper_bgcolor='#232627'
)

# set hover style
fig.update_traces(hovertemplate = '<br>Deaths: %{y}')

# line graph of cases by date
fig2 = px.line(df, x="Date", y="Cases", color="Area", 
               title="Cases by Nation", 
               width=600, height=350,
              template="plotly_dark"
)

fig2.update_layout(hovermode='x unified', 
                  plot_bgcolor='#232627', 
                  paper_bgcolor='#232627'
)

fig2.update_traces(hovertemplate = '<br>Cases: %{y}')

# Calculate 7 day rolling avgs
df['Deaths'] = df['Deaths'].rolling(window=7).mean()
df['Cases'] = df['Cases'].rolling(window=7).mean()

# line graph of deaths by date (7 day rolling avg)
fig3 = px.line(df, x="Date", y="Deaths", color="Area", 
               title="Deaths by Nation (7-day rolling average)", 
               width=600, height=350,
               template="plotly_dark"
)

fig3.update_layout(hovermode='x unified', 
                  plot_bgcolor='#232627', 
                  paper_bgcolor='#232627'
)

fig3.update_traces(hovertemplate = '<br>Deaths: %{y}')

# line graph of cases by date (7 day rolling avg)
fig4 = px.line(df, x="Date", y="Cases", color="Area", 
               title="Cases by Nation (7-day rolling average)", 
               width=600, height=350,
               template="plotly_dark"
)

fig4.update_layout(hovermode='x unified', 
                  plot_bgcolor='#232627', 
                  paper_bgcolor='#232627'
)

fig4.update_traces(hovertemplate = '<br>Cases: %{y}')


# Webpage layout, (css is loaded from assets/styles.css)
app.layout = html.Div(children=
    [
    
        # Title and general information
        html.H1(children='COVID-19 UK Data Graphing', 
                style={'textAlign': 'center'}
        ),

        html.P(children='Graphs generated using the latest data from Public Health England.', 
            style={'textAlign': 'center'}
        ),

        html.P(children=datestring, style={'textAlign': 'center'}),
        
        html.Div(children=dcc.Link('View source on GitHub.', href='https://github.com/EddieRowe/covid19-uk-graphing', target='_blank'), 
                style={'textAlign': 'center'}
        ),
            
        # Insert graphs
        html.Div(
            [
                dcc.Graph(
                    id='chart_cases_line',
                    figure=fig2,
                    config={
                        'displaylogo': False,
                        'modeBarButtonsToRemove':['toggleSpikelines', 'zoomIn2d', 'zoomOut2d', 'autoScale2d']
                    }
                ),
            
                dcc.Graph(
                    id='chart_avgcases_line',
                    figure=fig4,
                    config={
                        'displaylogo': False,
                        'modeBarButtonsToRemove':['toggleSpikelines', 'zoomIn2d', 'zoomOut2d', 'autoScale2d']
                    }
                )
            ], 
            style = {'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
        ),
            
        html.Div(
            [
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
            ], 
            style = {'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
        ),
            
            
        html.Div(children=dcc.Link('code.eddierowe.com', href='https://code.eddierowe.com', target='_blank'), 
                style={'textAlign': 'center'}
        ),
        
        html.Br()
    ], 
    style={'margin': 'auto', 'width': '50%'}
)

if __name__ == '__main__':
    app.run_server()
