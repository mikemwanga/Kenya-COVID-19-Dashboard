from utils import *

cardbody_style = {"background-color":pcolor}

layout = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Spinner([
            html.Iframe(src = "https://nextstrain.org/community/veclab/ncov-kenya@main/kenya",style={"height": "1062px", "width": "100%"})
        ])
        ])

    ],style = cardbody_style,className = "ms-2 me-2 mt-5 pt-5"), 
    
    hm.reference
])
