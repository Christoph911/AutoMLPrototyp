import json
from main import app
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score

@app.callback(
    [Output('dropdownX-forest-opt', 'options'),
     Output('train-test-forest', 'options')],
    [Input("load-data", "n_clicks")],
    [State('get-data-model', 'children')]
)
def update_date_dropdown(n_clicks, df):
    df = json.loads(df)
    df = pd.DataFrame(df['data'], columns=df['columns'])
    train_test_size = [{'label': '75% Train-size/25% Test-size', 'value': 0.25},
                       {'label': '60% Train-size/40% Test-size', 'value': 0.4}]

    optionsX = [{'label': col, 'value': col} for col in df.columns]

    return optionsX, train_test_size


@app.callback(
    Output("store-figure-forest", "data"),
    [Input('start-forest-btn', 'n_clicks')],
    [State('get-data-model', 'children'),
     State("dropdownX-forest-opt", "value"),
     State('train-test-forest', 'value')]
)
def make_random_forest(n_clicks, df, y, train_test_size):
    print("started random Forest")
    df = json.loads(df)
    df = pd.DataFrame(df['data'], columns=df['columns'])

    Y = df[y]
    X = df.drop(y, axis=1)

    # encode string values in target column
    le = LabelEncoder()
    Y = le.fit_transform(Y)

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=train_test_size)

    model = RandomForestClassifier(n_jobs=1, n_estimators=10)
    model.fit(X_train, Y_train)

    Y_pred = model.predict(X_test)

    global report, acc
    acc = accuracy_score(Y_test, Y_pred)

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
            metrics = html.P([
                "Accuracy Scoore: ", str(acc.round(3)), html.Br(),
                'Confusion Matrix:', html.Br(), str("T"), html.Br()
            ])
            return metrics
    return data