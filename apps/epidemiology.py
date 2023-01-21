import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

pcolor = "#FFFAFA"
cardbody_style = {"background-color":pcolor}

layout = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Spinner([
            html.Iframe(src = "https://nextstrain.org/community/blab/ncov-africa@main/south-africa",style={"height": "1062px", "width": "100%"})
        ])
        ])

    ],style = cardbody_style,className = "ms-2 me-2 mt-5 pt-5")
])
#http://0.0.0.0:4000/ncov-kenya/kenya
#https://nextstrain.org/community/blab/ncov-africa@main/south-africa