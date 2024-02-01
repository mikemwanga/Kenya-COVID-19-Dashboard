import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input,Output
from app import app
from app import server
import dash_mantine_components as dmc

app.title = "Kenya COVID-19 Dashboard"
#connect to your app pages
from apps import home,counties,vaccination,seroprevalence,variants,syndromic_trends2,phylogeny #syndromic_trends,
#home,,syndromic_trends,
tab_nav = "text-light fw-light"
style = {"text-decoration": "none"}
#Navbar
navbar =   html.Div([
                    
                    dbc.NavbarSimple([
                        dbc.NavItem(dbc.NavLink(html.A("Home", href="/apps/home.html/", className= tab_nav,style=style))),
                        dbc.NavItem(dbc.NavLink(html.A("County", href="/apps/counties.html/", className= tab_nav,style=style))),
                        dbc.NavItem(dbc.NavLink(html.A("Vaccination",href = "/apps/vaccination.html/",className= tab_nav,style=style))),
                        dbc.NavItem(dbc.NavLink(html.A("Seroprevalence",href = "/apps/seroprevalence.html/",className= tab_nav,style=style))),
                        #dbc.NavItem(dbc.NavLink(html.A("ASS",href = "/apps/syndromic.html/",className= tab_nav,style=style))),
                        dbc.NavItem(dbc.NavLink(html.A("Variants", href="/apps/variants.html/",className= tab_nav,style=style))),
                        # dbc.NavItem(dbc.NavLink(html.A("Syndromic-Surveillance", href="/apps/syndromic_trends.html/",className= tab_nav,style=style))),
                        dbc.NavItem(dbc.NavLink(html.A("Syndromic-Surveillance", href="/apps/syndromic_trends2.html/",className= tab_nav,style=style))),
                        dbc.NavItem(dbc.NavLink(html.A("Phylogeny", href="/apps/phylogeny.html/",className= tab_nav,style=style))),
                        #dbc.NavItem(dbc.NavLink(html.A("Home2", href="/apps/home2.html/", className= tab_nav,style=style))),
                        #dbc.DropdownMenu([
                         #   dbc.DropdownMenuItem("Countrywide",href="/apps/summaryreport"),
                          #  dbc.DropdownMenuItem("County",href="/apps/countysummary")
                        #],nav=True,in_navbar=True,label="Summary"),
                        # 
                        ],             brand_href="/apps/home.html",
                                    
                                      
                                    brand="Kenya COVID-19 Dashboard",
                                    style={"margin-bottom":5},
                                    color="#1DA1F2",light=True,dark=True,#, # #333972 
                                    fixed ="top",className = "text-light fw-light"),     
])                   
app.layout = html.Div([
    dcc.Location(id='url', refresh=True),
    navbar,
    html.Div(id='page-content', children=[]),
])
@app.callback(Output('page-content', 'children'),
            Input('url', 'pathname'),
            prevent_initial_callback=True)
            

def display_page(pathname):
    
    if pathname == "/apps/home.html/":
        return dcc.Loading(home.layout)
    elif pathname == '/apps/counties.html/':
            return dcc.Loading(counties.layout)
    elif pathname == "/apps/vaccination.html/":
          return dcc.Loading(vaccination.layout)
    elif pathname == "/apps/seroprevalence.html/":
         return dcc.Loading(seroprevalence.layout)
    elif pathname == "/apps/variants.html/":
         return dcc.Loading(variants.layout)
    elif pathname == "/apps/syndromic_trends.html/":
          return dcc.Loading(syndromic_trends.layout)
    elif pathname == "/apps/syndromic_trends2.html/":
          return dcc.Loading(syndromic_trends2.layout)
    elif pathname == "/apps/phylogeny.html/":
         return dcc.Loading(phylogeny.layout)
    else:
        return dcc.Loading(home.layout)



if __name__ == '__main__':
    app.run_server(debug=True,host="0.0.0.0", port = "3045", threaded=True)
