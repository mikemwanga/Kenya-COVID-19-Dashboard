import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output
#connect to main app.py file
from app import app
from app import server

app.title = "Kenya COVID-19 Dashboard"

#connect to your app pages
from apps import home,cases,deaths,vaccination,seroprevalence,variant_trends,phylogeny, contact
#Navbar
navbar =  html.Div([
                    dbc.NavbarSimple([
                        dbc.NavItem(dbc.NavLink("Home", href="/apps/home")),
                        dbc.DropdownMenu([
                        	dbc.DropdownMenuItem("Countrywide", href="/apps/cases/countrywide"),
                        	dbc.DropdownMenuItem("Countywide", href="/apps/cases/countywide"),
                        ],nav=True,in_navbar=True,label="Cases"),
                        dbc.DropdownMenu([
                        	dbc.DropdownMenuItem("Countrywide", href="/apps/deaths/countrywide"),
                        	dbc.DropdownMenuItem("Countywide", href="/apps/deaths/countywide"),
                        ],nav=True,in_navbar=True,label="Deaths"),
                        
                        dbc.NavItem(dbc.NavLink("Vaccination",href = "/apps/vaccination")),
                        
                            dbc.DropdownMenu([
                        	    dbc.DropdownMenuItem("Summary", href="/apps/seroprevalence/summary"),
                        	    dbc.DropdownMenuItem("Population", href="/apps/seroprevalence/population"),
                            ],nav=True,in_navbar=True,label="Seroprevalence"),
                        
                        dbc.NavItem(dbc.NavLink("Variant Trends", href="/apps/variant_trends")),
                        dbc.NavItem(dbc.NavLink("Phylogeny", href="/apps/phylogeny")),
                        #dbc.NavItem(dbc.NavLink("Contact", href = "/apps/contact")
            
                    ],              brand_href="/apps/home", 
                                    brand="Kenya COVID-19 Dashboard",
                                    style={"margin-bottom":5},
                                    color="#333972",dark=True,light=True,
                                    fixed ="top",className = "text-light font-weight-bold"
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
    elif pathname == '/apps/cases/countrywide':
        return dbc.Spinner(cases.countrywide),
    elif pathname == '/apps/cases/countywide':
        return dbc.Spinner(cases.countywide_cases)
    elif pathname == '/apps/deaths/countrywide':
        return deaths.countrywide_deaths
    elif pathname == '/apps/deaths/countywide':
        return deaths.countywide_deaths
    elif pathname == "/apps/vaccination":
        return vaccination.layout
    elif pathname == "/apps/seroprevalence/summary":
        return dbc.Spinner(seroprevalence.layout_summary)
    elif pathname == "/apps/seroprevalence/population":
        return dbc.Spinner(seroprevalence.sero_by_population)
    elif pathname == "/apps/variant_trends":
        return variant_trends.layout
    elif pathname == "/apps/phylogeny":
        return phylogeny.layout
    #elif pathname == "/apps/contact":
        #return contact.layout
    else:
        return home.layout

if __name__ == '__main__':
    app.run_server(debug=True,host="0.0.0.0", port = "3042", threaded=True)