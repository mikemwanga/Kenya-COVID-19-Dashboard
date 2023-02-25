import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input,Output
from app import app
from app import server

app.title = "Kenya COVID-19 Dashboard"

#connect to your app pages
from apps import home, counties,vaccination,seroprevalence,variant_trends#,phylogeny#summary_report #cases,deaths,home
#Navbar
navbar =  html.Div([
                    dbc.NavbarSimple([
                        dbc.NavItem(dbc.NavLink("Home", href="/apps/home")),
                        dbc.NavItem(dbc.NavLink("County", href="/apps/counties")),
                        dbc.NavItem(dbc.NavLink("Vaccination",href = "/apps/vaccination")),
                        dbc.NavItem(dbc.NavLink("Seroprevalence",href = "/apps/seroprevalence")),
                        dbc.NavItem(dbc.NavLink("Variant Trends", href="/apps/variant_trends")),
                        dbc.NavItem(dbc.NavLink("Phylogeny", href="/apps/phylogeny")),
                        #dbc.NavItem(dbc.NavLink("Summary Report", href="/apps/summaryreport"))
            
                    ],             brand_href="/apps/home", 
                                    brand="Kenya COVID-19 Dashboard",
                                    style={"margin-bottom":5},
                                    color="#333972",dark=True,light=True,
                                    fixed ="top",#className = "text-light font-weight-bold"
                                    )          
])                   

app.layout = html.Div([
    
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content', children=[])
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')], prevent_initial_callback=True)
def display_page(pathname):
    if pathname == "/apps/home":
        return home.layout
    elif pathname == '/apps/counties':
          return counties.layout
    elif pathname == "/apps/vaccination":
          return vaccination.layout
    elif pathname == "/apps/seroprevalence":
         return seroprevalence.layout
    elif pathname == "/apps/variant_trends":
         return variant_trends.layout
    # elif pathname == "/apps/phylogeny":
    #     return dbc.Spinner(phylogeny.layout)
    else:
        return home.layout

if __name__ == '__main__':
    app.run_server(debug=True,host="0.0.0.0", port = "3042", threaded=True)