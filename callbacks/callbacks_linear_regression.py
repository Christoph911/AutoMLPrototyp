import json
from main import app
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error

# get stored data, update dropdown, return selected target
@app.callback(
    Output('zielwert-opt-reg', 'options'),
    [Input('get-data-model', 'children'),
     Input('zielwert-div','children')]
)
def get_target(df,dummy):
    print("Daten an Dropdown Übergeben")
    df = json.loads(df)
    df = pd.DataFrame(df['data'], columns=df['columns'])

    target = [{'label': col, 'value': col} for col in df.columns]

    return target




# linear regression, return two figures, store figures in index.py
@app.callback(
    [Output("store-figure-reg", "data"),
    Output('store-figure-feat','data')],
    [Input('start-regression-btn', 'n_clicks')],
    [State('get-data-model', 'children'),
     State("zielwert-opt-reg", "value"),
     State('train-test', 'value'),
     State('metrics', 'value')]
)
def make_regression(n_clicks, df, y, train_test_size, choose_metrics):
    print("started regression")
    # load data
    df = json.loads(df)
    df = pd.DataFrame(df['data'], columns=df['columns'])

    # create model
    Y = df[y]
    X = df.drop(y, axis=1)

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, train_size=train_test_size)

    model = LinearRegression()
    model.fit(X_train, Y_train)

    Y_pred = model.predict(X_test)

    # create Metrics
    global mae, mse, rmse
    # create metrics depends on user input
    if 'mae' in choose_metrics:
        mae = mean_absolute_error(Y_test, Y_pred)
        mae = 'Mean absolute error(MAE): ' + str(mae.round(3))
    else:
        mae = None
    if 'mse' in choose_metrics:
        mse = mean_squared_error(Y_test, Y_pred)
        mse = "Mean squared error(MSE): " + str(mse.round(3))
    else:
        mse =  None
    if 'rmse' in choose_metrics:
        rmse = mean_squared_error(Y_test, Y_pred, squared=False)
        rmse = 'Root mean squared error(RMSE): ' + str(rmse.round(3))
    else:
        rmse = None


    # get feature importance
    importance = model.coef_
    # plot feature importance as bar chart
    fig_feature = go.Figure([
        go.Bar(x=X.columns, y=importance, text=importance.round(2), textposition='outside')
        ]
    )
    fig_feature.update_layout(
        xaxis_title='Feature names',
        yaxis_title='Score',
        template='plotly_white'
    )

    # build figure for results as scatter plot
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
    # return figures
    return dict(figure=fig), dict(figure=fig_feature)

# manage tab content
# get figures and metrics, display output
@app.callback(
    Output("tab-content", "children"),
    [Input("card-tabs-model", "active_tab"),
     Input("store-figure-reg", "data"),
     Input('store-figure-feat', 'data')],
)
def create_tab_content(active_tab, data, data_feat):
    if active_tab and data is not None:
        if active_tab == "tab-1-reg":
            figure = dcc.Graph(figure=data["figure"])
            return figure
        elif active_tab == "tab-2-reg":
            return mae, html.Br(), mse, html.Br(), rmse, html.Br()
        elif active_tab == 'tab-3-reg':
            figure = dcc.Graph(figure=data_feat['figure'])
            return figure
    return data

