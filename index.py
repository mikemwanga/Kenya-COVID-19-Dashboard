import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input,Output
from app import app
from app import server


app.title = "Kenya COVID-19 Dashboard"

#connect to your app pages
from apps import home, counties,vaccination,variant_trends,phylogeny,seroprevalence#,summary_report#,countysummary#,markdown#,download#cases,deaths,home

#Navbar
navbar =   html.Div([
                    
                    dbc.NavbarSimple([
                        dbc.NavItem(dbc.NavLink("Home", href="/apps/home")),
                        dbc.NavItem(dbc.NavLink("County", href="/apps/counties")),
                        dbc.NavItem(dbc.NavLink("Vaccination",href = "/apps/vaccination")),
                        dbc.NavItem(dbc.NavLink("Seroprevalence",href = "/apps/seroprevalence")),
                        dbc.NavItem(dbc.NavLink("Variants", href="/apps/variant_trends")),
                        dbc.NavItem(dbc.NavLink("Phylogeny", href="/apps/phylogeny")),
                        dbc.DropdownMenu([
                            dbc.DropdownMenuItem("Countrywide",href="/apps/summaryreport"),
                            dbc.DropdownMenuItem("County",href="/apps/countysummary")
                        ],nav=True,in_navbar=True,label="Summary"),

                    ],             brand_href="/apps/home", 
                                    brand="Kenya COVID-19 Dashboard",
                                    style={"margin-bottom":5},
                                    color="#333972",dark=True,light=True,
                                    fixed ="top",#className = "text-light font-weight-bold"
                     ),     
])                   

#app.layout = serve_layout

app.layout = html.Div([
    dcc.Location(id='url', refresh=True),
    navbar,
    html.Div(id='page-content', children=[]),
    
])

@app.callback(Output('page-content', 'children'),
            Input('url', 'pathname')) #,prevent_initial_callback=True

def display_page(pathname):
    
    if pathname == "/apps/home":
        return dbc.Spinner(home.layout,type="border",color="info")
    elif pathname == '/apps/counties':
           return counties.layout
    elif pathname == "/apps/vaccination":
          return dbc.Spinner(vaccination.layout,type="border",color="info")
    elif pathname == "/apps/seroprevalence":
         return dbc.Spinner(seroprevalence.layout,type="border",color="info")
    elif pathname == "/apps/variant_trends":
         return dbc.Spinner(variant_trends.layout,type="border",color="info")
    elif pathname == "/apps/phylogeny":
         return phylogeny.layout
    elif pathname == "/apps/summaryreport":
        return dbc.Spinner(summary_report.layout,type="border",color="info")
    elif pathname == "/apps/countysummary":
        return dbc.Spinner(countysummary.layout,type="border",color="info")
    else:
        return dbc.Spinner(home.layout,type="border",color="info")

if __name__ == '__main__':
    app.run_server(debug=True,host="0.0.0.0", port = "3042", threaded=True)