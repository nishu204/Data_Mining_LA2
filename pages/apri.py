import dash
from dash import dcc, html, dash_table, callback
from dash.dependencies import Input, Output
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
from ucimlrepo import fetch_ucirepo

dash.register_page(__name__,
                   path='/apr',
                   name='Apriori Algorithm',
                   title='Apriori Algorithm')

# Fetch dataset
congressional_voting_records = fetch_ucirepo(id=105)
X = congressional_voting_records.data.features

# Convert categorical data to one-hot encoding
encoder = OneHotEncoder(drop='first', sparse=False)
X_encoded = encoder.fit_transform(X)

# Convert one-hot encoded data back to DataFrame for display
X_encoded_df = pd.DataFrame(X_encoded, columns=encoder.get_feature_names_out(X.columns))

# Define the app
# app = dash.Dash(__name__)

# Define layout
layout = html.Div([
    html.H1("Association Rules Dashboard"),

    html.Label("Select Support Threshold:"),
    dcc.Slider(
        id='support-slider',
        min=0.01,
        max=0.1,
        step=0.01,
        marks={i/100: str(i/100) for i in range(1, 51)},
        value=0.1
    ),

    html.Label("Select Confidence Threshold:"),
    dcc.Slider(
        id='confidence-slider',
        min=0.1,
        max=1.0,
        step=0.1,
        marks={i/10: str(i/10) for i in range(1, 11)},
        value=0.5
    ),

    html.Label("Select Maximum Rule Length:"),
    dcc.Slider(
        id='max-rule-length-slider',
        min=1,
        max=10,
        step=1,
        marks={i: str(i) for i in range(1, 11)},
        value=5
    ),

    html.Div(id='output'),

    dash_table.DataTable(id='association-rules-table',
                         columns=[
                             {'name': 'Frequent Itemsets', 'id': 'Frequent Itemsets'},
                             {'name': 'Num Rules Generated', 'id': 'Num Rules Generated'}
                         ],
                         style_table={'height': '300px', 'overflowY': 'auto'},
                         ),
])

# Define callback to update results table
@callback(
    Output('association-rules-table', 'data'),
    [Input('support-slider', 'value'),
     Input('confidence-slider', 'value'),
     Input('max-rule-length-slider', 'value')]
)
def update_results(support, confidence, max_rule_length):
    # Apply Apriori algorithm
    te = TransactionEncoder()
    te_ary = te.fit_transform(X_encoded_df)
    df_encoded = pd.DataFrame(te_ary, columns=te.columns_)
    
    frequent_itemsets = apriori(df_encoded, min_support=support, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=confidence)
    
    # Filter rules based on max rule length
    rules = rules[rules['antecedents'].apply(lambda x: len(x) <= max_rule_length)]
    
    # Count the number of rules
    num_rules = len(rules)
    
    # Tabulate results
    result_table = pd.DataFrame({
        'Frequent Itemsets': [", ".join(map(str, itemset)) for itemset in frequent_itemsets['itemsets']],
        'Num Rules Generated': num_rules
    })

    return result_table.to_dict('records')


# if __name__ == '__main__':
#     app.run_server(debug=True)

