import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
from sklearn.cluster import Birch
from sklearn.decomposition import PCA
from sklearn.metrics import adjusted_rand_score
from sklearn.preprocessing import StandardScaler

# Load US Census data
url = r"C:\Users\nisha\Desktop\New folder\us+census+data+1990 (1)\USCensus1990.data.csv"  # Replace with the actual path to your data
df = pd.read_csv(url)

# Drop irrelevant columns and handle missing values
df = df.drop(columns=['caseid'])  # Drop 'caseid' column
df = df.dropna()

# Standardize the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df)

# Apply BIRCH algorithm
birch = Birch(n_clusters=2)
df['cluster'] = birch.fit_predict(X_scaled)

# Calculate PCA for visualization
pca = PCA(n_components=2)
df_pca = pd.DataFrame(pca.fit_transform(X_scaled), columns=['PC1', 'PC2'])
df_final = pd.concat([df, df_pca], axis=1)

# Calculate cluster validation accuracy using Adjusted Rand Index
ari_score = adjusted_rand_score(df['iRspouse'], df['cluster'])

# Dash app initialization
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# App layout
app.layout = dbc.Container(
    [
        html.H1("BIRCH Clustering on US Census Data"),
        html.Div(
            [
                dcc.Graph(
                    id='scatter-plot',
                    figure={
                        'data': [
                            {
                                'x': df_final['PC1'],
                                'y': df_final['PC2'],
                                'text': df_final['cluster'],
                                'mode': 'markers',
                                'marker': {'color': df_final['cluster']},
                            }
                        ],
                        'layout': {'title': 'BIRCH Clustering'},
                    },
                ),
            ]
        ),
        html.Div(
            [
                html.H3(f'Adjusted Rand Index: {ari_score:.2f}'),
            ]
        ),
    ],
    fluid=True,
)

if __name__ == '__main__':
    app.run_server(debug=True)
