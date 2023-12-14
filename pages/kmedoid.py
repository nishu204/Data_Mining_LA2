import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
from dash import Input, Output, dcc, html, callback
from pyclustering.cluster.kmedoids import kmedoids
from sklearn import datasets

dash.register_page(__name__,
                   path='/kmedoids',
                   name='KMedoids',
                   title='KMedoids')

iris_raw = datasets.load_iris()
iris = pd.DataFrame(iris_raw["data"], columns=iris_raw["feature_names"])

controls = dbc.Card(
    [
        html.Div(
            [
                dbc.Label("X variable"),
                dcc.Dropdown(
                    id="x-variable",
                    options=[
                        {"label": col, "value": col} for col in iris.columns
                    ],
                    value="sepal length (cm)",
                ),
            ]
        ),
        html.Div(
            [
                dbc.Label("Y variable"),
                dcc.Dropdown(
                    id="y-variable",
                    options=[
                        {"label": col, "value": col} for col in iris.columns
                    ],
                    value="sepal width (cm)",
                ),
            ]
        ),
        html.Div(
            [
                dbc.Label("Cluster count"),
                dbc.Input(id="cluster-count", type="number", value=3),
            ]
        ),
    ],
    body=True,
)

layout = dbc.Container(
    [
        html.H1("Iris k-medoids clustering"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls, md=4),
                dbc.Col(dcc.Graph(id="cluster-graph-a"), md=8),
            ],
            align="center",
        ),
    ],
    fluid=True,
)

@callback(
    Output("cluster-graph-a", "figure"),
    [
        Input("x-variable", "value"),
        Input("y-variable", "value"),
        Input("cluster-count", "value"),
    ],
)
def make_graph(x, y, n_clusters):
    # minimal input validation, make sure there's at least one cluster
    df = iris.loc[:, [x, y]]

    # Convert DataFrame to list of points for pyclustering
    points = df.values.tolist()

    # Create K-Medoids instance
    initial_medoids = [i for i in range(n_clusters)]
    kmedoids_instance = kmedoids(points, initial_medoids)

    # Run K-Medoids algorithm
    kmedoids_instance.process()
    clusters = kmedoids_instance.get_clusters()
    medoids = kmedoids_instance.get_medoids()

    data = []

    # Plot clusters
    for i, cluster in enumerate(clusters):
        cluster_points = df.iloc[cluster]
        data.append(
            go.Scatter(
                x=cluster_points[x],
                y=cluster_points[y],
                mode="markers",
                marker={"size": 8},
                name="Cluster {}".format(i),
            )
        )

    # Plot medoids
    medoid_points = df.iloc[medoids]
    data.append(
        go.Scatter(
            x=medoid_points[x],
            y=medoid_points[y],
            mode="markers",
            marker={"color": "#000", "size": 12, "symbol": "diamond"},
            name="Cluster Medoids",
        )
    )

    layout = {"xaxis": {"title": x}, "yaxis": {"title": y}}

    return go.Figure(data=data, layout=layout)

# make sure that x and y values can't be the same variable
def filter_options(v):
    """Disable option v"""
    return [
        {"label": col, "value": col, "disabled": col == v}
        for col in iris.columns
    ]
