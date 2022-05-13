import pandas as pd
import dash
import dash.html as html
import dash.dcc as dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

df = pd.read_csv('spacex_launch_dash.csv')

print(df.head())
max_payload = df['Payload Mass (kg)'].max()
min_payload = df['Payload Mass (kg)'].min()


launch_sites = df['Launch Site'].value_counts().keys()
print(launch_sites)




# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                             options=[{'label': 'All Sites', 'value': 'ALL'},
                                                      {'label': launch_sites[0], 'value': launch_sites[0]},
                                                      {'label': launch_sites[1], 'value': launch_sites[1]},
                                                      {'label': launch_sites[2], 'value': launch_sites[2]},
                                                      {'label': launch_sites[3], 'value': launch_sites[3]}],
                                             value = 'ALL',
                                             placeholder = 'Select a launch site here',
                                             searchable = True
                                             ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload_slider',
                                                min=0, max=10000, step=1000,
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback( [Output(component_id='success-pie-chart', component_property='figure'),
                Output(component_id='success-payload-scatter-chart', component_property='figure')],
               [Input(component_id='site-dropdown', component_property='value'),
                Input(component_id='payload_slider', component_property='value')]
             )

def get_charts(entered_site, payload_mass):
    filtered = df[df['Launch Site'] == entered_site]
    if entered_site == 'ALL':
        fig = px.pie(df[['Launch Site', 'class']], values='class', 
        names='Launch Site', 
        title='Total success launches by site')
        fig2 = px.scatter(df, x = 'Payload Mass (kg)', y = 'class', 
                          color = 'Booster Version Category',
                          title = 'Correlation between Payload and Success for all sites')
        fig2.update_xaxes(range=payload_mass)
        return  fig, fig2
    else:
        fig = px.pie(filtered[['Launch Site','class']], values=filtered['class'].value_counts(), 
        names=filtered['class'].value_counts().keys(), 
        title='Total Success launches for site {0}'.format(entered_site))
        fig2 = px.scatter(filtered, x = 'Payload Mass (kg)', y = 'class', 
                          color = 'Booster Version Category',
                          title='Correlation between Payload and Success for site{0}'.format(entered_site))
        fig2.update_xaxes(range=payload_mass)
        return fig, fig2
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output    

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)