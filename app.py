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
df = pd.read_csv('new_cases.csv')
df2 = pd.read_csv('cum_cases.csv')


# Get and format date
df['Date'] = pd.to_datetime(df['Date'])
date_time = df['Date'].max()
date = date_time.strftime("%d/%m/%Y")

datestring = "PHE data from ", date, "."
info = ""
desc = 'Graphs generated using recent data from Public Health England.'

# Line graph of deaths by date
fig = px.line(df, x="Date", y="Deaths", color="Area", 
            title="Deaths by Nation", 
            width=600, height=350,
            template="plotly_dark"
)

# Set style elements
fig.update_layout(hovermode='x unified', 
                plot_bgcolor='#232627', 
                paper_bgcolor='#232627'
)

# Set hover style
fig.update_traces(hovertemplate = '<br>Deaths: %{y}')

# Line graph of cases by date
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

# Line graph of deaths by date (7 day rolling avg)
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

# Line graph of cases by date (7 day rolling avg)
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

# Assign coords to ltlas
df3 = pd.read_csv('coordinateList', header = None)
df2['lat'] = df3[0];
df2['lon'] = df3[1];

# Scatter graph of total cases by area
fig_scatter = px.scatter_geo(df2, lon=df2['lon'], lat=df2['lat'],
                    color="Cases",
                    title="Total Cumulative Cases by Local Authority", 
                    width=1000, height=800,
                    hover_name="Area",
                    size="Cases",
                    scope="europe",
                    template="plotly_dark",
                    center={"lat": 53.643666, "lon": -3.898219},
                    #animation_frame="Date"
            )

fig_scatter.update_geos(
    resolution=50,
    fitbounds="locations"
)

fig_scatter.update_layout(hovermode='x unified', 
                plot_bgcolor='#232627', 
                paper_bgcolor='#232627',
                margin={"r":0,"t":50,"l":0,"b":0}    
)

fig_scatter.update_traces(hovertemplate = '<b>%{hovertext}</b><br>Cases: %{marker.size}')



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
            
        # Insert graphs
        html.Div(
            className="graphs",
            children=[
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
            ]
        ),
                
        html.Div(
            className="graphs",
            children=[
                dcc.Graph(
                    id='chart_deaths_line',
                    figure=fig,
                    config={
                    'displaylogo': False,
                    'modeBarButtonsToRemove':['toggleSpikelines', 'zoomIn2d', 'zoomOut2d','autoScale2d']
                    }
                ),
                    
                dcc.Graph(
                    id='chart_avgdeaths_line',
                    figure=fig3,
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
                    id='chart_cases_scatter',
                    figure=fig_scatter,
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
