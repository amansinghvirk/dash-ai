import random
from dash import Dash, dash_table, dcc, html, Input, Output, callback
import pandas as pd
import dash_bootstrap_components as dbc
from src.calls.dash import (
    ai_call_bar_plot_for_categorical_variables_v,
    ai_call_scatter_plot_for_two_variables
)


app = Dash(__name__,
    title="Llama dash app",
    external_stylesheets=[dbc.themes.SOLAR]
)

app.layout = dbc.Container([
    dbc.Row(
        [
            html.Div(
                [
                    html.Div(
                        "AI Based Dashboard",
                        id="click-div",
                        style={"color": "white", "font-weight": "bold"},
                    )
                ]
            )
        ], 
        style={'height': '100px', 'width': '1100px', 'background-color': 'green'}
    ),
    dbc.Row([
        dbc.Col(
            ["Side Panel", html.Button('Magic', id='btn-agent')], 
            width=12,
            style={'height': '80px', 'width': '1100px', 'background-color': 'blue'}
        )
    ]),
    dbc.Row([
        dbc.Col(
            [
                dbc.Row([
                    html.Div(
                        "Question 1",
                        id="question-1",
                        style={"color": "white", "font-weight": "bold"},
                    )
                ]),
                dbc.Row([dcc.Graph(id='plot-1')])

            ], 
            width=6,
            style={'height': '280px', 'width': '500px', 'background-color': 'orange'}
        ),
        dbc.Col(
            [
                dbc.Row([
                    html.Div(
                        "Question 2",
                        id="question-2",
                        style={"color": "white", "font-weight": "bold"},
                    )
                ]),
                dbc.Row([dcc.Graph(id='plot-2')])

            ], 
            width=6,
            style={'height': '280px', 'width': '500px', 'background-color': 'orange'}
        )
    ])
], style={'height': '400px', 'width': '1100px'})


@app.callback(
    Output("question-1", "children"),
    Output('plot-1', 'figure'),
    Output("question-2", "children"),
    Output('plot-2', 'figure'),
    [Input("btn-agent", 'n_clicks')])
def update_plot(n_clicks):

    df = pd.read_csv("./data/electric-consumption.csv")

    question1, fig1 = ai_call_bar_plot_for_categorical_variables_v(df)
    question2, fig2 = ai_call_scatter_plot_for_two_variables(df)

    return question1, fig1 , question2, fig2


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)