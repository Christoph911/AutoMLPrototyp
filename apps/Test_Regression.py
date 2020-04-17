import base64
import io

import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_table
import plotly.graph_objs as go

import pandas as pd
import sklearn
from dash.exceptions import PreventUpdate
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
server = app.server


# import dataset
def parse_data(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'Fehler beim Dateiupload!'
        ])

    return df

# dropdown options
# TODO: Callbacks redundanter code. bessere Lösung?
@app.callback(
    [Output('opt-dropdownX', 'options'),
     Output('model', 'options')],
    [
        Input('upload', 'contents'),
        Input('upload', 'filename')

    ]
)
def update_date_dropdown(contents, filename):
    optionsX = []
    model = [{'label': "Lineare Regression", 'value': "regression"},
             {'label': "Random Forest", 'value': "forest"}]
    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)

        optionsX = [{'label': col, 'value': col} for col in df.columns]

    return optionsX, model

@app.callback(
    Output("regression-graph", "figure"),
    [Input('button', 'n_clicks')],

    [State("opt-dropdownX", "value"),
     State("model","value"),
     State('upload', 'contents'),
     State('upload', 'filename')
     ],
)
def make_regression(n_clicks, x,model, contents, filename):
    layout = None
    data = []
    if contents is None or filename is None or x is None or model is None:
        raise PreventUpdate
    if model == "regression":
        if contents:
            contents = contents[0]
            filename = filename[0]
            contents = parse_data(contents, filename)

            Y = contents[x]
            print(Y)
            X = contents.drop(x,axis=1)
            print(X)

            X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.33)

            model = LinearRegression()
            model.fit(X_train,Y_train)

            Y_pred = model.predict(X_test)

            mse = sklearn.metrics.mean_squared_error(Y_test, Y_pred)
            print(mse)


            data = [
                go.Scatter(
                    x=Y_test,
                    y=Y_pred,
                    mode="markers",
                    marker={"size": 8},
                )

            ]

            layout = {"xaxis": {"title": "Actual " + x}, "yaxis": {"title": "Predicted" + x}}

                #title=f"Score: {filename}, MSE: {mse:.3f} (Test Data)",
    elif model == "forest":
        print("Ich und mein Holz")

    elif model == None:
        print("Bitte Model auswählen")


    return go.Figure(data=data, layout=layout)




# masterlayout
app.layout = html.Div(
    [
        dcc.Upload(
            id="upload",
            children=dbc.Button("hochladen"),
            multiple=True
        ),
        dbc.FormGroup(
            [
                dbc.Label("Zielwert"),
                dcc.Dropdown(
                    id="opt-dropdownX",
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Modellauswahl"),
                dcc.Dropdown(
                    id="model",
                ),
            ]
        ),
        html.Button('Click Me', id='button'),
        dcc.Graph(id="regression-graph"),
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)
