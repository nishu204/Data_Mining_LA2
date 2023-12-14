import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import networkx as nx

dash.register_page(__name__,
                   path='/hits',
                   name='HITS',
                   title='HITS')

# Function to read Google web graph and calculate HITS
def calculate_hits(file_path):
    G = nx.read_edgelist(file_path, create_using=nx.DiGraph(), nodetype=int)
    hits_result = nx.hits(G)
    return hits_result

# Function to create a Dash table from the results
def create_table(data, max_rows=10):
    hub_df = pd.DataFrame(list(data[0].items()), columns=['Page', 'Hub'])
    authority_df = pd.DataFrame(list(data[1].items()), columns=['Page', 'Authority'])
    
    hub_df = hub_df.sort_values(by='Hub', ascending=False).head(max_rows)
    authority_df = authority_df.sort_values(by='Authority', ascending=False).head(max_rows)

    # Define styles
    table_style = {
        'border-spacing': '10px',
        'border-collapse': 'separate',
        'width': '100%',  # Adjust the width as needed
    }

    th_style = {
        'padding': '10px',  # Adjust the padding as needed
    }

    td_style = {
        'padding': '5px',  # Adjust the padding as needed
    }


    return html.Div(children=[
        html.H2(children=''),
        html.Div(children=[
            html.Div(children=[
                html.H3(children='Hub Scores'),
                html.Table(
                    # Header
                    [html.Tr([html.Th(col, style=th_style) for col in hub_df.columns], style = table_style)] +
                    # Body
                    [html.Tr([html.Td(hub_df.iloc[i][col], style=td_style) for col in hub_df.columns], style = table_style) for i in range(min(len(hub_df), max_rows))]
                ),
            ], style={'width': '48%', 'float': 'left', 'margin-right': '2%'}),

            html.Div(children=[
                html.H3(children='Authority Scores'),
                html.Table(
                    # Header
                    [html.Tr([html.Th(col, style=th_style) for col in authority_df.columns], style = table_style)] +
                    # Body
                    [html.Tr([html.Td(authority_df.iloc[i][col], style=td_style) for col in authority_df.columns], style = table_style) for i in range(min(len(authority_df), max_rows))]
                ),
            ], style={'width': '48%', 'float': 'left'}),
        ], style={'margin-bottom': '20px'})
    ])

# Define the Dash app
# app = dash.Dash(__name__)

# Specify the path to the downloaded file
file_path = r'C:\Users\nisha\Desktop\New folder\web-Google.txt'

# Calculate HITS
hits_data = calculate_hits(file_path)

# Define the layout of the app
layout = html.Div(children=[
    html.H1(children='HITS Algorithm Dashboard'),

    # Display the adjacency matrix
    html.Div(children=[
        html.H2(children='Adjacency Matrix'),
        dcc.Markdown(children='''
            The adjacency matrix is not displayed here due to its large size.
            However, it is used internally for HITS calculations.
        ''')
    ]),

    # Display the HITS results in tables
    html.Div(children=[
        html.H2(children='HITS Results'),
        create_table(hits_data)
    ])
])

# if __name__ == '__main__':
#     app.run_server(debug=True)
