import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, callback, Input, Output
from scipy.cluster.hierarchy import linkage, dendrogram
from sklearn import datasets
import pandas as pd
import plotly.graph_objs as go

dash.register_page(__name__,
                   path='/hierarchical-clustering',
                   name='Hierarchical Clustering',
                   title='Hierarchical Clustering')

iris_raw = datasets.load_iris()
iris = pd.DataFrame(iris_raw["data"], columns=iris_raw["feature_names"])

controls = dbc.Card(
    [
        html.Div(
            [
                dbc.Label("Select Clustering Method"),
                dcc.Dropdown(
                    id="clustering-method",
                    options=[
                        {"label": "AGNES (Agglomerative Nesting)", "value": "agnes"},
                        {"label": "DIANA (Divisive Analysis)", "value": "diana"},
                    ],
                    value="agnes",
                ),
            ]
        ),
    ],
    body=True,
)

layout = dbc.Container(
    [
        html.H1("Hierarchical Clustering on Iris Dataset"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls, md=4),
                dbc.Col(dcc.Graph(id="dendrogram"), md=8),
            ],
            align="center",
        ),
    ],
    fluid=True,
)

@callback(
    Output("dendrogram", "figure"),
    [Input("clustering-method", "value")]
)
def update_dendrogram(method):
    # Hierarchical clustering
    if method == "agnes":
        linkage_matrix = linkage(iris, "ward")  # AGNES
        dendro_title = "AGNES Dendrogram"
    elif method == "diana":
        linkage_matrix = linkage(iris, "single")  # DIANA
        dendro_title = "DIANA Dendrogram"
    else:
        raise ValueError("Invalid clustering method selected.")

    fig = go.FigureWidget()

    dendrogram_trace = go.Dendrogram(
        orientation='left',
        labels=iris.index,
        linkage_matrix=linkage_matrix
    )

    fig.add_trace(dendrogram_trace)

    fig.update_layout(title_text=dendro_title, xaxis_title="Distance", yaxis_title="Samples")

    return fig

# Uncomment the following lines to run the app
# app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
# app.layout = layout
# if __name__ == "__main__":
#     app.run_server(debug=True)




