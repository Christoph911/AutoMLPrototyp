import os
#CAVE: stellt error Messages und warnings für TF aus!
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import json
from main import app
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow import keras
import keras.backend.tensorflow_backend as tb
tb._SYMBOLIC_SCOPE.value = True


@app.callback(
    Output('zielwert-opt-nn', 'options'),
    [Input('load-data-nn','n_clicks')],
    [State('get-data-model', 'children')]
)
def update_date_dropdown(df, n_clicks):
    print("Daten an Dropdown Übergeben")
    df = json.loads(df)
    df = pd.DataFrame(df['data'], columns=df['columns'])

    options_y = [{'label': col, 'value': col} for col in df.columns]

    return options_y

@app.callback(
    Output("store-figure-nn", "data"),
    [Input('start-nn-btn', 'n_clicks')],
    [State('get-data-model', 'children'),
     State("zielwert-opt-nn", "value")]
)
def create_neural_network(n_clicks, df, y):
    print("started neural network")
    df = json.loads(df)
    df = pd.DataFrame(df['data'], columns=df['columns'])

    # MinMaxScaler for  preprocessing
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_train = scaler.fit_transform(df)
    multiplied_by = scaler.scale_[13]
    added = scaler.min_[13]
    # scaler result to dataFame
    scaled_train_df = pd.DataFrame(scaled_train, columns=df.columns.values)

    # build model
    model = keras.Sequential(
        [
            keras.layers.Dense(50,activation='relu'),
            keras.layers.Dense(100,activation='relu')
        ]
    )

    model.compile(optimizer='adam',loss=tf.keras.losses.mean_squared_error)

    Y = scaled_train_df.loc[:,[y]]
    X = scaled_train_df.drop([y], axis=1).values

    # Train the model
    model.fit(
        X[10:],
        Y[10:],
        epochs=10,
        shuffle=True,
        verbose=2
    )

    # predict
    prediction = model.predict(X[:1])
    y_0 = prediction[0][0]
    print('Prediction with scaling - {}', format(y_0))
    y_0 -= added
    y_0 /= multiplied_by
    print("Housing Price Prediction  - ${}".format(y_0))

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
    Output("tab-content-nn", "children"),
    [Input("card-tabs-nn", "active_tab"),
     Input("store-figure-nn", "data")],
)
def create_tab_content(active_tab, data):
    if active_tab and data is not None:
        if active_tab == "tab-1-nn":
            figure = dcc.Graph(figure=data["figure"])
            return figure
        elif active_tab == "tab-2-nn":
            metrics = html.P(['metrics'])
            return metrics
    return data
