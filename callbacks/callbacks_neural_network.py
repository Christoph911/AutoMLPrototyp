import json
from main import app
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.graph_objs as go
import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow import keras
#from keras import Sequential
#from keras.layers import Dense
import keras.backend.tensorflow_backend as tb
from keras.models import model_from_json
tb._SYMBOLIC_SCOPE.value = True
from tensorflow.keras import Sequential


@app.callback(
    Output('zielwert-opt-nn', 'options'),
    [Input('get-data-model', 'children'),
     Input('load-data-nn','n_clicks')]
)
def update_date_dropdown(df,n_clicks):
    print("Daten an Dropdown Übergeben")
    if n_clicks is None:
        raise PreventUpdate
    elif n_clicks is not None:
        df = json.loads(df)
        df = pd.DataFrame(df['data'], columns=df['columns'])

        options_y = [{'label': col, 'value': col} for col in df.columns]

        return options_y
    else:
        raise PreventUpdate

# TODO: mse ausgeben lassen
# simple regression on input data and return figure
@app.callback(
    Output("nn-graph", "figure"),
    [Input('get-data-model', 'children'),
     Input("zielwert-opt-nn", "value"),
     Input('card-tabs-nn', 'active_tab'),
     Input('start-nn-btn', 'n_clicks'),
     ],
)
def create_neural_network(df,y,active_tab,n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    elif n_clicks is not None:
        print("started neural network")
        df = json.loads(df)
        df = pd.DataFrame(df['data'], columns=df['columns'])

    if active_tab == 'tab-1-nn':
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

        return prediction

    else:
        raise PreventUpdate