import json
from main import app
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegressionCV
from sklearn.metrics import recall_score, precision_score, f1_score, roc_auc_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
import plotly.figure_factory as ff
import sklearn.metrics as metrics
from callbacks.callbacks_master import error_message_get_target
import dash_bootstrap_components as dbc
import numpy as np
import plotly.express as px


# get stored data, update dropdown, return selected target
@app.callback(
    [Output('zielwert-opt-log', 'options'),
     Output('error-message-target-log', 'children')],
    [Input('get-data-model', 'children'),
     Input('zielwert-div', 'children')]
)
def get_target(df, dummy):
    try:
        print("Daten an Dropdown Übergeben")
        df = json.loads(df)
        df = pd.DataFrame(df['data'], columns=df['columns'])

        target = [{'label': col, 'value': col} for col in df.columns]

        return target, None
    except:
        return None, error_message_get_target


@app.callback(
    [Output("store-figure-log", "data"),
     Output('store-fig-roc-log', 'data'),
     Output('error-message-model-log', 'children')],
    [Input('start-logistic-regression-btn', 'n_clicks')],
    [State('get-data-model', 'children'),
     State("zielwert-opt-log", "value"),
     State('train-test', 'value'),
     State('metrics', 'value')]
)
def make_log_regression(n_clicks, df, y, train_test_size, choose_metrics):
    try:
        print("started logistic regression")
        df = json.loads(df)
        df = pd.DataFrame(df['data'], columns=df['columns'])

        Y = df[y]
        X = df.drop(y, axis=1)

        # label encoder for y-column
        label_encoder = LabelEncoder()
        Y = label_encoder.fit_transform(Y)

        # scale data with standard scaler
        sc = StandardScaler()
        X = sc.fit_transform(X)

        # train/test/split
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, train_size=train_test_size)

        # create and fit model
        model = LogisticRegressionCV()
        model.fit(X_train, Y_train)
        # predict
        Y_pred = model.predict(X_test)

        # check for binary classification task and build roc curve if true
        if len(np.unique(Y)) <= 2:
            # predict proba and other metrics for for roc-curve
            Y_pred_proba = model.predict_proba(X_test)
            preds = Y_pred_proba[:, 1]
            fpr, tpr, threshold = metrics.roc_curve(Y_test, preds)
            auc = metrics.roc_auc_score(Y_test, preds)

            # create roc-curve figure
            fig_roc = px.area(
                x=fpr, y=tpr,
                title=f'ROC Curve (AUC={auc:.4f})',
                labels=dict(x='False Positive Rate', y='True Positive Rate'),
                width=800, height=600
            )

            fig_roc.add_shape(
                type='line', line=dict(dash='dash'),
                x0=0, x1=1, y0=0, y1=1
            )

            fig_roc.update_yaxes(scaleanchor="x", scaleratio=1)
            fig_roc.update_xaxes(constrain='domain')
        else:
            fig_roc = html.Div("")

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
        # reverse label encoder for matrix
        Y = label_encoder.inverse_transform(Y)
        # convert y values to string
        Y = Y.astype(str)
        # get target names
        target_names = np.unique(Y)

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

        return dict(figure=fig), dict(figure=fig_roc), None


    except Exception as e:

        error_message_model = dbc.Modal(
            [
                dbc.ModalHeader("Fehler!"),
                dbc.ModalBody(["Es ist ein Fehler während des Trainingsprozesses aufgetreten:", html.Br(),
                               html.H6(str(e)), html.Br(),
                               " Bitte stell darüber hinaus sicher, dass der verwendete Datensatz"
                               " keine Null-Values enthält "
                               "und das korrekte Modell für die Problemstellung ausgewählt wurde", html.Br(),
                               ]),
                dbc.ModalFooter("")
            ],
            is_open=True,
        )
        return None, None, error_message_model


# manage tab content
@app.callback(
    Output("tab-content-log", "children"),
    [Input("card-tabs-logistic-reg", "active_tab"),
     Input("store-figure-log", "data"),
     Input("store-fig-roc-log", "data")],
)
def create_tab_content(active_tab, data, roc):
    if active_tab and data is not None:
        if active_tab == "tab-1-log-reg":
            figure = dcc.Graph(figure=data["figure"])
            return figure
        elif active_tab == "tab-2-log-reg":
            return recall, html.Br(), precision, html.Br(), f1, html.Br()
        elif active_tab == 'tab-3-log-reg':
            figure = dcc.Graph(figure=roc["figure"])
            return figure
    return data
