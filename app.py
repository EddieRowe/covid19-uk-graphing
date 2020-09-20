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

# Load data
df_nation = pd.read_csv('new_cases.csv')
df_ltla_cum_rate_cases = pd.read_csv('cum_cases.csv')
#df_ltla_daily_cases = pd.read_excel('new_cases_ltla_2.xls')
df_ltla_daily_cases = pd.read_csv('new_cases_ltla.csv')

# Assign coords to ltlas
df_ltla_cum_coords = pd.read_csv('coordinateList', header = None)
df_ltla_cum_rate_cases['lat'] = df_ltla_cum_coords[0];
df_ltla_cum_rate_cases['lon'] = df_ltla_cum_coords[1];
# PHE provides different lists of areas for different metrics,
# so I've had to create different lists of associated coordinates.
df_ltla_daily_coords = pd.read_csv('coordinateList_dailyltla', header = None)
df_ltla_daily_cases['lat'] = df_ltla_daily_coords[0];
df_ltla_daily_cases['lon'] = df_ltla_daily_coords[1];

# Get and format date
df_nation['Date'] = pd.to_datetime(df_nation['Date'])
date_time = df_nation['Date'].max()
date = date_time.strftime("%d/%m/%Y")

datestring = "PHE data from ", date, "."
info = ""
desc = 'Graphs generated using recent data from Public Health England.'

# Line graph of deaths by date
fig_line_deaths_raw = px.line(df_nation, x="Date", y="Deaths", color="Area", 
            title="Daily Deaths by Nation", 
            width=600, height=350,
            template="plotly_dark"
)

# Set style elements
fig_line_deaths_raw.update_layout(hovermode='x unified', 
                plot_bgcolor='#232627', 
                paper_bgcolor='#232627'
)

# Set hover style
fig_line_deaths_raw.update_traces(hovertemplate = '<br>Deaths: %{y}')

# Line graph of cases by date
fig_line_cases_raw = px.line(df_nation, x="Date", y="Cases", color="Area", 
            title="Daily Cases by Nation", 
            width=600, height=350,
            template="plotly_dark"
)

fig_line_cases_raw.update_layout(hovermode='x unified', 
                plot_bgcolor='#232627', 
                paper_bgcolor='#232627'
)

fig_line_cases_raw.update_traces(hovertemplate = '<br>Cases: %{y}')


# Calculate 7 day rolling avgs
df_nation['Deaths'] = df_nation['Deaths'].rolling(window=7).mean()
df_nation['Cases'] = df_nation['Cases'].rolling(window=7).mean()
df_nation['Tests'] = df_nation['Tests'].rolling(window=7).mean()

# Line graph of deaths by date (7 day rolling avg)
fig_line_deaths_avg = px.line(df_nation, x="Date", y="Deaths", color="Area", 
            title="Daily Deaths by Nation (7-day rolling average)", 
            width=600, height=350,
            template="plotly_dark"
)

fig_line_deaths_avg.update_layout(hovermode='x unified', 
                plot_bgcolor='#232627', 
                paper_bgcolor='#232627'
)

fig_line_deaths_avg.update_traces(hovertemplate = '<br>Deaths: %{y}')

# Line graph of cases by date (7 day rolling avg)
fig_line_cases_avg = px.line(df_nation, x="Date", y="Cases", color="Area", 
            title="Daily Cases by Nation (7-day rolling average)", 
            width=600, height=350,
            template="plotly_dark"
)

fig_line_cases_avg.update_layout(hovermode='x unified', 
                plot_bgcolor='#232627', 
                paper_bgcolor='#232627'
)

fig_line_cases_avg.update_traces(hovertemplate = '<br>Cases: %{y}')


# Line graph of avg tests by date
fig_line_tests_avg = px.line(df_nation, x="Date", y="Tests", color="Area", 
            title="Daily Tests by Nation (7-day rolling average)", 
            width=600, height=350,
            template="plotly_dark"
)

fig_line_tests_avg.update_layout(hovermode='x unified', 
                plot_bgcolor='#232627', 
                paper_bgcolor='#232627'
)

fig_line_tests_avg.update_traces(hovertemplate = '<br>Tests: %{y}')

# Scatter map of rate of total cases by area
fig_scattermap_ltla_cases_rate = px.scatter_geo(df_ltla_cum_rate_cases, lon=df_ltla_cum_rate_cases['lon'], lat=df_ltla_cum_rate_cases['lat'],
                    color="Rate",
                    title="Total Cases per 100k by Local Authority", 
                    width=1000, height=800,
                    hover_name="Area",
                    size="Rate",
                    scope="europe",
                    template="plotly_dark",
                    center={"lat": 53.643666, "lon": -3.898219},
                    #animation_frame="Date"
            )

fig_scattermap_ltla_cases_rate.update_geos(
    resolution=50,
    fitbounds="locations"
)

fig_scattermap_ltla_cases_rate.update_layout(hovermode='x unified', 
                plot_bgcolor='#232627', 
                paper_bgcolor='#232627',
                margin={"r":0,"t":50,"l":0,"b":0}    
)

fig_scattermap_ltla_cases_rate.update_traces(hovertemplate = '<b>%{hovertext}</b><br>Cases per 100k: %{marker.size}')


# Scatter graph of new cases today by area
fig_scattermap_ltla_cases_daily = px.scatter_geo(df_ltla_daily_cases, lon=df_ltla_daily_cases['lon'], lat=df_ltla_daily_cases['lat'],
                    color="Cases",
                    title="New Cases Today by Local Authority", 
                    width=1000, height=680,
                    hover_name="Area",
                    size="Cases",
                    scope="europe",
                    template="plotly_dark",
                    center={"lat": 53.643666, "lon": -3.898219},
                    #animation_frame="Date"
            )

fig_scattermap_ltla_cases_daily.update_geos(
    resolution=50,
    fitbounds="locations"
)

fig_scattermap_ltla_cases_daily.update_layout(hovermode='x unified', 
                plot_bgcolor='#232627', 
                paper_bgcolor='#232627',
                margin={"r":0,"t":50,"l":0,"b":0}    
)

fig_scattermap_ltla_cases_daily .update_traces(hovertemplate = '<b>%{hovertext}</b><br>Daily Cases: %{marker.size}')




# Webpage layout, (css is loaded from assets/styles.css)
app.layout = html.Div(
    [
        # Title and general information
        html.Div(
            className="centeredtext",
            children=[
                html.H1('COVID-19 UK Data Graphing'),
                html.P(info),
                html.P(desc),
                html.P(datestring)
            ]
        ),
            
            
        html.Div(
            className="graphs",
            children=[
                dcc.Graph(
                    id='chart_scattermap_ltla_cases_daily',
                    figure=fig_scattermap_ltla_cases_daily,
                    config={
                    'displaylogo': False,
                    'modeBarButtonsToRemove':['toggleSpikelines', 'zoomIn2d', 'zoomOut2d','autoScale2d']
                    }
                )
            ]
        ),             
            
     
        html.Div(
            className="graphs",
            children=[
                dcc.Graph(
                    id='chart_line_cases_raw',
                    figure=fig_line_cases_raw,
                    config={
                        'displaylogo': False,
                        'modeBarButtonsToRemove':['toggleSpikelines', 'zoomIn2d', 'zoomOut2d', 'autoScale2d']
                    }
                ),
                
                dcc.Graph(
                    id='chart_line_cases_avg',
                    figure=fig_line_cases_avg,
                    config={
                        'displaylogo': False,
                        'modeBarButtonsToRemove':['toggleSpikelines', 'zoomIn2d', 'zoomOut2d', 'autoScale2d']
                    }
                )
            ]
        ),
                
        html.Div(
            className="graphs",
            children=[
                dcc.Graph(
                    id='chart_line_deaths_raw',
                    figure=fig_line_deaths_raw,
                    config={
                    'displaylogo': False,
                    'modeBarButtonsToRemove':['toggleSpikelines', 'zoomIn2d', 'zoomOut2d','autoScale2d']
                    }
                ),
                    
                dcc.Graph(
                    id='chart_line_deaths_avg',
                    figure=fig_line_deaths_avg,
                    config={
                    'displaylogo': False,
                    'modeBarButtonsToRemove':['toggleSpikelines', 'zoomIn2d', 'zoomOut2d','autoScale2d']
                    }
                )
            ]
        ),
          
        html.Div(
            className="centeredtext",
            children=[
                html.P('The chart below shows 7-day average of the number tests being processed each day by each nation in the UK. This is regardless of whether the test returns positive or negative.')
            ]
        ),          

        html.Div(
            className="graphs",
            children=[             
                dcc.Graph(
                    id='chart_line_tests_avg',
                    figure=fig_line_tests_avg,
                    config={
                        'displaylogo': False,
                        'modeBarButtonsToRemove':['toggleSpikelines', 'zoomIn2d', 'zoomOut2d', 'autoScale2d']
                    }
                )
            ]
        ),         

        html.Div(
            className="centeredtext",
            children=[
                html.P('The map below gives an overall idea of which areas have had the largest proportions of their populations infected since PHE case records began. The metric we use is "cases per 100k" - this allows us to more accurately compare areas, regardless of their actual populations. Bear in mind, this data is not a perfect representation of how many people have had coronavirus.'),
                html.A('View PHE "About the data"', 
                                href='https://coronavirus.data.gov.uk/about-data#daily-and-cumulative-numbers-of-cases', 
                                target='_blank'),
                html.P('')
            ]
        ),

        html.Div(
            className="graphs",
            children=[
                dcc.Graph(
                    id='chart_scattermap_ltla_cases_rate',
                    figure=fig_scattermap_ltla_cases_rate,
                    config={
                    'displaylogo': False,
                    'modeBarButtonsToRemove':['toggleSpikelines', 'zoomIn2d', 'zoomOut2d','autoScale2d']
                    }
                )
            ]
        ),  
               
        # Footer
        html.Div(
            className="centeredtext",
            children=[
                html.P(
                    [
                        'Created by Eddie Rowe -  ',
                        html.A('code.eddierowe.com', 
                                href='https://code.eddierowe.com/', 
                                target='_blank'), 
                        html.Br(),
                        html.A('View source on GitHub.', 
                                href='https://github.com/EddieRowe/covid19-uk-graphing/', 
                                target='_blank')
                    ]
                )
            ]
        )
    ]
)
                            


if __name__ == '__main__':
    app.run_server()
