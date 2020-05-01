import json
from main import app
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.graph_objs as go
import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier


@app.callback(
    [Output('dropdownX-forest-opt', 'options'),
     Output('train-test-forest', 'options')],
    [
        Input('stored-data', 'children'),
        Input("load-data", "n_clicks")

    ]
)
def update_date_dropdown(df, n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    elif n_clicks is not None:
        df = json.loads(df)
        df = pd.DataFrame(df['data'], columns=df['columns'])
        train_test_size = [{'label': '75% Train-size/25% Test-size', 'value': 0.25},
                           {'label': '60% Train-size/40% Test-size', 'value': 0.4}]

        optionsX = [{'label': col, 'value': col} for col in df.columns]

        return optionsX, train_test_size
    else:
        raise PreventUpdate


# TODO: One Hot Encoding implementieren
@app.callback(
    Output("forest-graph", "figure"),
    [Input('table-new', 'children'),
     Input("dropdownX-forest-opt", "value"),
     Input('train-test-forest', 'value'),
     Input('card-tabs-forest', 'active_tab'),
     Input('start-forest-btn', 'n_clicks'),
     ],
)
def make_random_forest(df, y, train_test_size, active_tab, n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    elif n_clicks is not None:
        print("started random Forest")
        df = json.loads(df)
        df = pd.DataFrame(df['data'], columns=df['columns'])

    if active_tab == 'tab-1-forest':
        Y = df[y]
        X = df.drop(y, axis=1)

        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=train_test_size)

        model = RandomForestClassifier(n_jobs=1, n_estimators=10)
        model.fit(X_train, Y_train)

        Y_pred = model.predict(X_test)

        data = [
            go.Scatter(
                x=Y_test,
                y=Y_pred,
                mode="markers",
                marker={"size": 8},
            )

        ]

        layout = {"xaxis": {"title": "Actual " + y}, "yaxis": {"title": "Predicted " + y},'template':'plotly_white'}

        return go.Figure(data=data, layout=layout)

    else:
        raise PreventUpdate
