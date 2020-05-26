import json
from main import app
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error


@app.callback(
    [Output("store-figure-forest-reg", "data"),
     Output('store-figure-forest-reg-feat','data')],
    [Input('start-forest-reg-btn', 'n_clicks')],
    [State('get-data-model', 'children'),
     State("zielwert-opt", "value"),
     State('number-trees','value'),
     State('train-test', 'value'),
     State('metrics', 'value')]
)
def make_random_forest(n_clicks, df, y, number_trees, train_test_size, choose_metrics):
    print("started random Forest reg")
    df = json.loads(df)
    df = pd.DataFrame(df['data'], columns=df['columns'])
    print(train_test_size)
    target = df[y]
    X = df.drop(y, axis=1)

    # encode string values in target column
    le = LabelEncoder()
    Y = le.fit_transform(target)

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, train_size=train_test_size)

    model = RandomForestRegressor(n_estimators=number_trees)

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
        mse = None
    if 'rmse' in choose_metrics:
        rmse = mean_squared_error(Y_test, Y_pred, squared=False)
        rmse = 'Root mean squared error(RMSE): ' + str(rmse.round(3))
    else:
        rmse = None

    # get feature importance
    importance = model.feature_importances_
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
@app.callback(
    Output("tab-content-forest-reg", "children"),
    [Input("card-tabs-forest-reg", "active_tab"),
     Input("store-figure-forest-reg", "data"),
     Input('store-figure-forest-reg-feat','data')],
)
def create_tab_content(active_tab, data,data_feat):
    if active_tab and data is not None:
        if active_tab == "tab-1-forest-reg":
            figure = dcc.Graph(figure=data["figure"])
            return figure
        elif active_tab == "tab-2-forest-reg":
            return mae, html.Br(), mse, html.Br(), rmse, html.Br()
        elif active_tab == 'tab-3-forest-reg':
            figure = dcc.Graph(figure=data_feat['figure'])
            return figure
    return data