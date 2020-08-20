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
   

### PHE API
datastructure = {
    "Date": "date",
    "Area": "areaName",
    "Deaths": "newDeaths28DaysByPublishDate",
    "Cases": "newCasesByPublishDate"
}

datastructure2 = {
    "Area": "areaName",
    "Deaths": "newDeaths28DaysByPublishDate"
}

datastructure3 = {
    "Area": "areaName",
    "Deaths": "newDeaths28DaysByPublishDate"
}


all_uk = [
    'areaType=nation'
]

all_ltlas = [
    'areaType=ltla'
]

all_regions = [
    'areaType=region'
]

# Instantiating the API object
phe_api = Cov19API(filters=all_uk, structure=datastructure)
data = phe_api.get_json()

#phe_api2 = Cov19API(filters=all_ltlas, structure=datastructure2, latest_by="newDeaths28DaysByPublishDate")
#data2 = phe_api2.get_json()

#phe_api3 = Cov19API(filters=all_regions, structure=datastructure3)
#data3 = phe_api3.get_json()

# latest website update
release_timestamp = Cov19API.get_release_timestamp()

# date formatting
release_timestamp_formatted = release_timestamp.replace('Z', '')
date = datetime.fromisoformat(release_timestamp_formatted)
date_time = date.strftime("%d/%m/%Y, %H:%M")
date_ = date.strftime("%d/%m/%Y")
datestring = "Latest PHE data from ", date_time, " GMT."
### end of PHE API


df = data['data'];
# convert to pandas dataframe for rolling avg later
df = pd.DataFrame(df)


#df2 = data2['data']
#df2 = pd.DataFrame(df2)

#df3 = data3['data']
#df3 = pd.DataFrame(df3)


#total_day_deaths = df2.sum(axis = 0)[1]
#total_cum_deaths = df3.sum(axis = 0)[1]

#drop useless data
###df2 = df2.drop('Date', axis=1)
###df2 = df2.drop('Cases', axis=1)
#df2 = df2.dropna()

#indexNames = df2[df2['Deaths'] <== 0].index
#df2.drop(indexNames, inplace=True)


#df3.sort_values(by=['Deaths'], inplace=True, ascending=False)
#df3 = df3[:10]



#fig_death_ltla = px.pie(df2, names="Area", values="Deaths", 
#              title="Today's Deaths " + "(" + str(total_day_deaths) + ") on " + date_ + " by Local Region", 
#              width=600, height=400,
#              template="plotly_dark",
#              color_discrete_sequence=px.colors.cyclical.Twilight)

#fig_death_ltla.update_layout(hovermode='x unified', 
#                  plot_bgcolor='#232627', 
#                  paper_bgcolor='#232627'
#                  )
#fig_death_ltla.update_traces(
#                  hovertemplate = '%{label} <br>Deaths: %{value}'
#                  )

#fig_deathtotal_ltla = px.pie(df3, names="Area", values="Deaths", 
#              title="Today's Deaths" + " (" + str(total_cum_deaths) + ") " + "by Local Region (Top 10)", 
#              width=600, height=400,
#              template="plotly_dark",
#              color_discrete_sequence=px.colors.sequential.Plotly3)

#fig_deathtotal_ltla.update_layout(hovermode='x unified', 
#                  plot_bgcolor='#232627', 
#                  paper_bgcolor='#232627'
#                  )

#fig_deathtotal_ltla.update_traces(
#                  hovertemplate = '%{label} <br>Deaths: %{value}'
#                  )

fig = px.line(df, x="Date", y="Deaths", color="Area", 
              title="Deaths by Nation", 
              width=600, height=400,
              template="plotly_dark",
              color_discrete_sequence=px.colors.qualitative.Plotly)

fig.update_layout(hovermode='x unified', 
                  plot_bgcolor='#232627', 
                  paper_bgcolor='#232627'
                  )

fig.update_traces(
                  hovertemplate = '<br>Deaths: %{y}'
                  )


fig2 = px.line(df, x="Date", y="Cases", color="Area", 
               title="Cases by Nation", 
               width=600, height=400,
              template="plotly_dark")




fig2.update_layout(hovermode='x unified', 
                  plot_bgcolor='#232627', 
                  paper_bgcolor='#232627')

fig2.update_traces(
                  hovertemplate = '<br>Cases: %{y}'
                  )

# 7 day rolling avg deaths
df['Deaths'] = df['Deaths'].rolling(window=7).mean()

fig3 = px.line(df, x="Date", y="Deaths", color="Area", 
               title="Deaths by Nation (7-day rolling average)", 
               width=1000, height=400,
              template="plotly_dark")

fig3.update_layout(hovermode='x unified', 
                  plot_bgcolor='#232627', 
                  paper_bgcolor='#232627')

fig3.update_traces(
                  hovertemplate = '<br>Deaths: %{y}'
                  )


app.layout = html.Div(children=[
    
    html.H1(children='COVID-19 UK Data Graphing', style={'textAlign': 'center'}),

    html.P(children='Graphs generated using the latest data from Public Health England.', 
             style={'textAlign': 'center'}),

    html.P(children=datestring, style={'textAlign': 'center'}),
    
    html.Div(children=dcc.Link('View source on GitHub.', href='https://github.com/EddieRowe/covid19-uk-graphing', target='_blank'), style={'textAlign': 'center'}),
    
    html.Br(),

    
    
    html.Div([
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
    )], style = {'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
        
        html.Div([
    dcc.Graph(
        id='chart_avgdeaths_line',
        figure=fig3,
        config={
        'displaylogo': False,
        'modeBarButtonsToRemove':['toggleSpikelines', 'zoomIn2d', 'zoomOut2d', 'autoScale2d']
        }
    )], style = {'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
        
        
#        html.Div([
#    dcc.Graph(
#        id='chart_cases_map',
#        figure=fig_death_ltla,
#        config={
#        'displaylogo': False,
#        'modeBarButtonsToRemove':['toggleSpikelines', 'zoomIn2d', 'zoomOut2d', 'autoScale2d']
#    }
#    ),
#        
#        dcc.Graph(
#        id='chart_cases_map2',
#        figure=fig_deathtotal_ltla,
#        config={
#        'displaylogo': False,
#        'modeBarButtonsToRemove':['toggleSpikelines', 'zoomIn2d', 'zoomOut2d', 'autoScale2d']
#    }
#    )
#        
#        ], style = {'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
    
    html.Br(),
    
    html.Div(children=dcc.Link('code.eddierowe.com', href='https://code.eddierowe.com', target='_blank'), style={'textAlign': 'center'}),
    
    html.Br()
    
    
], style={'margin': 'auto', 'width': '50%'})

if __name__ == '__main__':
    app.run_server()
