import dash
import dash_bootstrap_components as dbc
from dash import dcc, html,dash_table,callback,Input,Output
import pandas as pd
import plotly.express as px


dbc_css = ("https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css], # LUX, FLATLY LUMEN SPACELAB YETI
                suppress_callback_exceptions=True,prevent_initial_callbacks=False,
                meta_tags=[{"name":"viewport","content":"width=device-width,initial-scale=1.0"}])


variants_data = pd.read_table("../data/kenya_lineages_until180523.tsv", usecols=["strain","date","division","pangolin_lineage"])
variants_data = variants_data[variants_data["division"].notna() & (variants_data["pangolin_lineage"]!="Unassigned")]
variants_data["date"] = pd.to_datetime(variants_data["date"], format ="%d/%m/%Y" )
variant_map = pd.read_table("../data/map_lineages.tsv")
var_type =  dict(zip(variant_map.lineage, variant_map.lineage_group))
variants_data["lineage_type"] = variants_data["pangolin_lineage"].map(var_type)
var_grouped =  variants_data.groupby(["date","division","lineage_type"])[["lineage_type"]].count()\
    .rename(columns={"lineage_type":"Freq"}).reset_index()
    
color_patterns = ['#0000FF','#1f78b4','#00FF00','#008000','#fb9a99','#e31a1c','#fdbf6f','#ff7f00','#cab2d6','#6a3d9a','#ffff99','#b15928',\
                "#FF00FF",'#800080','#808080'] 

app.layout = html.Div([
    dbc.Row([
        
        html.P("Select County"),
        
        dcc.Dropdown(
            options = var_grouped['division'].sort_values().unique(),
            value = "Nairobi",
            id = "selected_county"
        ),
        dbc.Col([
            dcc.Graph("county_var")
        ],width=6)
    ],className = '"mt-5 pt-5')
])


@app.callback(
    Output('county_var','figure'),
    Input('selected_county','value')
)

def render_image(value):
    data = var_grouped[(var_grouped["division"].isin([value]))]# & (var_grouped["date"] > "2020-01-01")]
    data = data.groupby(['lineage_type',data["date"].dt.strftime("%b-%y")])["Freq"].sum().to_frame().reset_index()
    data["date"] = pd.to_datetime(data["date"],format="%b-%y")
    fig = px.bar(data, x = "date",y = "Freq",color="lineage_type", range_x=["2020-01","2023-06"],color_discrete_sequence= color_patterns)
    
    return fig



if __name__ == '__main__':
    app.run_server(debug=True,host="0.0.0.0", port = "2020", threaded=True)