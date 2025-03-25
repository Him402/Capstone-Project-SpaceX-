# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the Falcon 9 launch data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown', options=[{'label': 'All Sites', 'value': 'ALL'},
                                                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}],
                                                value='ALL',
                                                placeholder="Select a Launch Site here",
                                                searchable=True
                                                ),
                                html.Br(),
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),
                                
                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',min=0, max=10000, step=1000,
                                                marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
                                                value=[min_payload, max_payload]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
                Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Total Success Launches by all sites')
        return fig
    elif entered_site == 'CCAFS LC-40':
        filtered_df1 = spacex_df[spacex_df['Launch Site']=='CCAFS LC-40']
        outcomes_count1 = filtered_df1.groupby('class').size().reset_index(name='count1')
        fig = px.pie(outcomes_count1, values='count1', 
        names='class', 
        title=(f'Total Success Launches by {entered_site} site'))
        return fig
    elif entered_site == 'CCAFS SLC-40':
        filtered_df2 = spacex_df[spacex_df['Launch Site']=='CCAFS SLC-40']
        outcomes_count2 = filtered_df2.groupby('class').size().reset_index(name='count2')
        fig = px.pie(outcomes_count2, values='count2', 
        names='class', 
        title=(f'Total Success Launches by {entered_site} site'))
        return fig
    elif entered_site == 'KSC LC-39A':
        filtered_df3 = spacex_df[spacex_df['Launch Site']=='KSC LC-39A']
        outcomes_count3 = filtered_df3.groupby('class').size().reset_index(name='count3')
        fig = px.pie(outcomes_count3, values='count3', 
        names='class', 
        title=(f'Total Success Launches by {entered_site} site'))
        return fig
    elif entered_site == 'VAFB SLC-4E':
        filtered_df4 = spacex_df[spacex_df['Launch Site']=='VAFB SLC-4E']
        outcomes_count4 = filtered_df4.groupby('class').size().reset_index(name='count4')
        fig = px.pie(outcomes_count4, values='count4', 
        names='class', 
        title=(f'Total Success Launches by {entered_site} site'))
        return fig
        # return the outcomes piechart for a selected site
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
                [Input(component_id='site-dropdown', component_property='value'),
                Input(component_id='payload-slider', component_property='value')]
                )
def check_sites(entered_site,payload_range):
    if entered_site == 'ALL':
        low, high = payload_range
        mask = (spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
        fig = px.scatter(spacex_df[mask], x='Payload Mass (kg)', y='class', color='Booster Version Category', title = 'Correlation b/w Payload & Success for all sites')
        return fig
    elif entered_site == 'CCAFS LC-40':
        filtered_df1 = spacex_df[spacex_df['Launch Site']=='CCAFS LC-40']
        low, high = payload_range
        mask = (filtered_df1['Payload Mass (kg)'] > low) & (filtered_df1['Payload Mass (kg)'] < high)
        fig = px.scatter(filtered_df1[mask], x='Payload Mass (kg)', y='class', color='Booster Version Category', title = 'Correlation b/w Payload & Success for CCAFS LC-40 sites' )
        return fig
    elif entered_site == 'CCAFS SLC-40': 
        filtered_df2 = spacex_df[spacex_df['Launch Site']=='CCAFS SLC-40']
        low, high = payload_range
        mask = (filtered_df2['Payload Mass (kg)'] > low) & (filtered_df2['Payload Mass (kg)'] < high)
        fig = px.scatter(filtered_df2[mask], x='Payload Mass (kg)', y='class', color='Booster Version Category', title = 'Correlation b/w Payload & Success for CCAFS SLC-40 site')
        return fig
    elif entered_site == 'KSC LC-39A': 
        filtered_df3 = spacex_df[spacex_df['Launch Site']=='KSC LC-39A']
        low, high = payload_range
        mask = (filtered_df3['Payload Mass (kg)'] > low) & (filtered_df3['Payload Mass (kg)'] < high)
        fig = px.scatter(filtered_df3[mask], x='Payload Mass (kg)', y='class', color='Booster Version Category', title = 'Correlation b/w Payload & Success for KSC LC-39A site')
        return fig
    elif entered_site == 'VAFB SLC-4E': 
        filtered_df4 = spacex_df[spacex_df['Launch Site']=='VAFB SLC-4E']
        low, high = payload_range
        mask = (filtered_df4['Payload Mass (kg)'] > low) & (filtered_df4['Payload Mass (kg)'] < high)
        fig = px.scatter(filtered_df4[mask], x='Payload Mass (kg)', y='class', color='Booster Version Category', title = 'Correlation b/w Payload & Success for VAFB SLC-4E site')
        return fig
# Run the app
if __name__ == '__main__':
    app.run()
