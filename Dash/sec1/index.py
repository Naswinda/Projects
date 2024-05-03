import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from app import app
from apps import scatter_layout, histogram_layout, line_layout, treemap_layout

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/scatter_layout':
        return scatter_layout.layout
    if pathname == '/apps/histogram_layout':
        return histogram_layout.layout
    if pathname == '/apps/treemap_layout':
        return treemap_layout.layout
    if pathname == '/apps/line_layout':
        return line_layout.layout
    if pathname == '/':
        return "Please choose a link"

if __name__ == '__main__':
    app.run_server(debug=False)
