import json
from main import app
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegressionCV
from sklearn.metrics import recall_score, precision_score, f1_score, confusion_matrix
from sklearn.preprocessing import StandardScaler
import plotly.figure_factory as ff
import sklearn.metrics as metrics


# get stored data, update dropdown, return selected target
@app.callback(
    Output('zielwert-opt-log', 'options'),
    [Input('get-data-model', 'children'),
     Input('zielwert-div', 'children')]
)
def get_target(df, dummy):
    print("Daten an Dropdown Übergeben")
    df = json.loads(df)
    df = pd.DataFrame(df['data'], columns=df['columns'])

    target = [{'label': col, 'value': col} for col in df.columns]

    return target


@app.callback(
    Output("store-figure-log", "data"),
    [Input('start-logistic-regression-btn', 'n_clicks')],
    [State('get-data-model', 'children'),
     State("zielwert-opt-log", "value"),
     State('train-test', 'value'),
     State('metrics', 'value')]
)
def make_log_regression(n_clicks, df, y, train_test_size, choose_metrics):
    print("started logistic regression")
    df = json.loads(df)
    df = pd.DataFrame(df['data'], columns=df['columns'])

    Y = df[y]
    X = df.drop(y, axis=1)

    # scale data with standard scaler
    sc = StandardScaler()
    X = sc.fit_transform(X)

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, train_size=train_test_size)

    model = LogisticRegressionCV()
    model.fit(X_train, Y_train)

    Y_pred = model.predict(X_test)

    # create Metrics
    global recall, precision, f1

    # create metrics depends on user input
    if 'recall' in choose_metrics:
        recall = recall_score(Y_test, Y_pred, average='micro')
        recall = 'Recall Score: ' + str(recall.round(3))
    else:
        recall = None
    if 'precision' in choose_metrics:
        precision = precision_score(Y_test, Y_pred, average='micro')
        precision = 'Precision Score: ' + str(precision.round(3))
    else:
        precision = None
    if 'f1' in choose_metrics:
        f1 = f1_score(Y_test, Y_pred, average='micro')
        f1 = 'F1 Score: ' + str(f1.round(3))
    else:
        f1 = None

    # create confusion matrix
    confusion_matrix = metrics.confusion_matrix(Y_test, Y_pred)
    # convert results into int
    confusion_matrix = confusion_matrix.astype(int)
    # get target names
    target_names = Y.unique()
    # split target names by comma and return list
    target_names = ' '.join(target_names).split()

    # set variables for matrix
    z = confusion_matrix
    x = target_names
    y = target_names

    # change each element of z to type string for annotations
    z_text = [[str(y) for y in x] for x in z]

    # set up figure
    fig = ff.create_annotated_heatmap(z, x=x, y=y, annotation_text=z_text, colorscale='Blues')

    # add title and margin
    fig.update_layout(title_text='Confusion matrix',
                      margin=dict(t=50, l=200)
                      )
    # add colorbar
    fig['data'][0]['showscale'] = True

    return dict(figure=fig)


# manage tab content
@app.callback(
    Output("tab-content-log", "children"),
    [Input("card-tabs-logistic-reg", "active_tab"),
     Input("store-figure-log", "data")],
)
def create_tab_content(active_tab, data):
    if active_tab and data is not None:
        if active_tab == "tab-1-log-reg":
            figure = dcc.Graph(figure=data["figure"])
            return figure
        elif active_tab == "tab-2-log-reg":
            return recall, html.Br(), precision, html.Br(), f1, html.Br()
    return data
