import json
from main import app
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.graph_objs as go
import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression



@app.callback(
    [Output('zielwert-opt', 'options'),
     Output('train-test-opt', 'options')],
    [Input('get-data-model', 'children'),
     Input('load-data','n_clicks')]
)
def update_date_dropdown(df,n_clicks):
    print("Daten an Dropdown Übergeben")
    if n_clicks is None:
        raise PreventUpdate
    elif n_clicks is not None:
        df = json.loads(df)
        df = pd.DataFrame(df['data'], columns=df['columns'])
        train_test_size = [{'label': '75% Train-size/25% Test-size', 'value': 0.25},
                           {'label': '60% Train-size/40% Test-size', 'value': 0.4}]

        options_y = [{'label': col, 'value': col} for col in df.columns]

        return options_y, train_test_size
    else:
        raise PreventUpdate


# TODO: mse ausgeben lassen
# simple regression on input data and return figure
@app.callback(
    Output("regression-graph", "figure"),
    [Input('get-data-model', 'children'),
     Input("zielwert-opt", "value"),
     Input('train-test-opt', 'value'),
     Input('card-tabs-model', 'active_tab'),
     Input('start-regression-btn', 'n_clicks'),
     ],
)
def make_regression(df, y, train_test_size, active_tab, n_clicks):
    mse = None
    if n_clicks is None:
        raise PreventUpdate
    elif n_clicks is not None:
        print("started regression")
        df = json.loads(df)
        df = pd.DataFrame(df['data'], columns=df['columns'])

    if active_tab == 'tab-1-reg':

        Y = df[y]
        X = df.drop(y, axis=1)

        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=train_test_size)

        model = LinearRegression()
        model.fit(X_train, Y_train)

        Y_pred = model.predict(X_test)

        mse = sklearn.metrics.mean_squared_error(Y_test, Y_pred)

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
