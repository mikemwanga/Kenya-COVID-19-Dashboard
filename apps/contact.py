import dash
from dash import dcc, html,dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from app import app

pcolor = "#FFFAFA"
cardbody_style = {"background-color":pcolor}


layout = html.Div(
    dbc.Row([
        #dbc.Card([
            dbc.Col([
                dbc.CardBody([
                    html.P("Share your feedback with us by commenting below"),
                    dbc.Input(id = "yourname", type = "text",placeholder = "Full Names",debounce=True,required = True,className = "mt-3"),
                    html.Br(),
                    dbc.Input(type = "email", placeholder="Enter email",debounce =True,className = "mt-3"),
                    html.Br(),
                    dbc.Textarea(id = "comment", placeholder = "Comment",debounce = True,required = True,size="sm",className = "mt-3"),
                    dbc.Button("Submit",color = "primary", outline=True, id = "submit",n_clicks=1,className = "mt-2"),
                    dbc.Popover(dbc.PopoverBody("Thank you for your feedback"),target = "submit", trigger = "legacy"),
                ],style = cardbody_style)
            ], width=5)
        #])
        
    ],className = "justify-content-center mt-5 pt-5")
)
