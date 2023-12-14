import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import networkx as nx

dash.register_page(__name__,
                   path='/page',
                   name='PageRank',
                   title='PageRank')

# Function to read Google web graph and calculate PageRank
def calculate_pagerank(file_path):
    G = nx.read_edgelist(file_path, create_using=nx.DiGraph(), nodetype=int)
    pagerank = nx.pagerank(G)
    return pagerank

# Function to create a Dash table from the results
# def create_table(data, max_rows=10):
#     df = pd.DataFrame(list(data.items()), columns=['Page', 'PageRank'])
#     df = df.sort_values(by='PageRank', ascending=False).head(max_rows)
#     return html.Table(
#         # Header
#         [html.Tr([html.Th(col) for col in df.columns])] +
#         # Body
#         [html.Tr([html.Td(df.iloc[i][col]) for col in df.columns]) for i in range(min(len(df), max_rows))]
#     )

def create_table(data, max_rows=10):
    df = pd.DataFrame(list(data.items()), columns=['Page', 'PageRank'])
    df = df.sort_values(by='PageRank', ascending=False).head(max_rows)

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

    # Create the HTML table
    return html.Table(
        # Header
        [html.Tr([html.Th(col, style=th_style) for col in df.columns], style=table_style)] +
        # Body
        [html.Tr([html.Td(df.iloc[i][col], style=td_style) for col in df.columns], style=table_style) for i in range(min(len(df), max_rows))]
    )




# Define the Dash app
# app = dash.Dash(__name__)

# Specify the path to the downloaded file
file_path = r'C:\Users\nisha\Desktop\New folder\web-Google.txt'

# Calculate PageRank
pagerank_data = calculate_pagerank(file_path)

# Define the layout of the app
layout = html.Div(children=[
    html.H1(children='PageRank Dashboard'),

    # Display the adjacency matrix
    html.Div(children=[
        html.H2(children='Adjacency Matrix'),
        dcc.Markdown(children='''
            The adjacency matrix is not displayed here due to its large size.
            However, it is used internally for PageRank calculations.
        ''')
    ]),

    # Display the PageRank results in a table
    html.Div(children=[
        html.H2(children='PageRank Results'),
        create_table(pagerank_data)
    ])
])

# if __name__ == '__main__':
#     app.run_server(debug=True)
