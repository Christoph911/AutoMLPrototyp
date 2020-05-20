import json
from main import app
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.figure_factory as ff
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import recall_score, precision_score, f1_score
from sklearn import metrics

@app.callback(
    Output('zielwert-forest-opt', 'options'),
    [Input("load-data", "n_clicks")],
    [State('get-data-model', 'children')]
)
def get_target(n_clicks, df):
    df = json.loads(df)
    df = pd.DataFrame(df['data'], columns=df['columns'])

    target = [{'label': col, 'value': col} for col in df.columns]

    return target

# get slider value, return train size
@app.callback(
    Output('train-test-forest','value')
)
def get_train_test_size(slider):
    train_test_size = [{'marks':marks} for marks in slider]
    return train_test_size

# get metric values, return selected metrics
@app.callback(
    Output('metrics-forest','value')
)
def get_metrics(get_metrics):
    get_metrics = [{"label":label, "value": val} for val, label in get_metrics]
    print(get_metrics)
    return get_metrics

@app.callback(
    Output("store-figure-forest", "data"),
    [Input('start-forest-btn', 'n_clicks')],
    [State('get-data-model', 'children'),
     State("zielwert-forest-opt", "value"),
     State('number-trees','value'),
     State('train-test-forest', 'value'),
     State('metrics-forest', 'value')]
)
def make_random_forest(n_clicks, df, y,number_trees, train_test_size,choose_metrics):
    print("started random Forest")
    df = json.loads(df)
    df = pd.DataFrame(df['data'], columns=df['columns'])

    target = df[y]
    X = df.drop(y, axis=1)

    # encode string values in target column
    le = LabelEncoder()
    Y = le.fit_transform(target)

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y,train_size=train_test_size)

    model = RandomForestClassifier(n_jobs=1, n_estimators=number_trees)

    model.fit(X_train, Y_train)

    Y_pred = model.predict(X_test)

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
    target_names = target.unique()
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
    Output("tab-content-forest", "children"),
    [Input("card-tabs-forest", "active_tab"),
     Input("store-figure-forest", "data")],
)
def create_tab_content(active_tab, data):
    if active_tab and data is not None:
        if active_tab == "tab-1-forest":
            figure = dcc.Graph(figure=data["figure"])
            return figure
        elif active_tab == "tab-2-forest":
            return recall, html.Br(), precision, html.Br(), f1, html.Br()
    return data