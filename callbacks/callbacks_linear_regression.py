import json
from main import app
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.graph_objs as go
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, explained_variance_score, r2_score


@app.callback(
    [Output('zielwert-opt', 'options'),
     Output('train-test-opt', 'options')],
    [Input('load-data', 'n_clicks')],
    [State('get-data-model', 'children')]
)
def update_date_dropdown(n_clicks, df):
    print("Daten an Dropdown Übergeben")
    df = json.loads(df)
    df = pd.DataFrame(df['data'], columns=df['columns'])
    train_test_size = [{'label': '75% Train-size/25% Test-size', 'value': 0.25},
                       {'label': '60% Train-size/40% Test-size', 'value': 0.4}]

    options_y = [{'label': col, 'value': col} for col in df.columns]

    return options_y, train_test_size

# simple regression on input data and return figure
@app.callback(
    Output("store-figure-reg", "data"),
    [Input('start-regression-btn', 'n_clicks')],
    [State('get-data-model', 'children'),
     State("zielwert-opt", "value"),
     State('train-test-opt', 'value')]
)
def make_regression(n_clicks, df, y, train_test_size):
    print("started regression")
    # load data
    df = json.loads(df)
    df = pd.DataFrame(df['data'], columns=df['columns'])

    # create model
    Y = df[y]
    X = df.drop(y, axis=1)

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=train_test_size)

    model = LinearRegression()
    model.fit(X_train, Y_train)

    Y_pred = model.predict(X_test)

    global evs, mse, r2
    evs = explained_variance_score(Y_test, Y_pred)
    mse = mean_squared_error(Y_test, Y_pred)
    r2 = r2_score(Y_pred, Y_pred)

    # build figure
    fig = go.Figure(
        data=[
            go.Scatter(
                x=Y_test,
                y=Y_pred,
                mode="markers",
                marker={"size": 8}
            )
        ]
    )
    fig.update_layout(
        xaxis_title='Actual ' + y,
        yaxis_title='Predict ' + y,
        template='plotly_white'
    )

    return dict(figure=fig)

# manage tab content
@app.callback(
    Output("tab-content", "children"),
    [Input("card-tabs-model", "active_tab"),
     Input("store-figure-reg", "data")],
)
def create_tab_content(active_tab, data):
    if active_tab and data is not None:
        if active_tab == "tab-1-reg":
            figure = dcc.Graph(figure=data["figure"])
            return figure
        elif active_tab == "tab-2-reg":
            metrics = html.P([  'Explained variance score: ' + str(evs.round(3)), html.Br(),
                                "Mean Squared Error: ", str(mse.round(3)), html.Br(),
                                'R^2 score: ' + str(r2.round(3)), html.Br()
                              ])
            return metrics
    return data

