#Reference: https://github.com/Coding-with-Adam/Dash-by-Plotly/blob/master/Dash%20Components/Graph/dash-graph.py

from dash import Dash, dcc, html, Input, Output
import plotly.express as px

df = px.data.gapminder()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Dropdown(id='dpdn2', value=['Germany','Brazil'], multi=True, options=[{'label': x, 'value': x} for x in df.country.unique()]),
    html.Div([
        dcc.Graph(id='pie-graph', figure={}, className='six columns', config={'displayModeBar': True}),
        dcc.Graph(id='my-graph', figure={}, clickData=None, hoverData=None,
                  config={
                      'staticPlot': False,     # True, False
                      'scrollZoom': True,      # True, False
                      'doubleClick': 'reset',  # 'reset', 'autosize' or 'reset+autosize', False
                      'showTips': False,       # True, False
                      'displayModeBar': True,  # True, False, 'hover'
                      'watermark': True,
                  },
                  className='four columns'
                  ),
        dcc.Graph(id='bar-graph',figure={}, className='six columns', config={'displayModeBar': True})
    ])
])

@app.callback(
    Output(component_id='my-graph', component_property='figure'),
    Input(component_id='dpdn2', component_property='value'),
)
def update_graph(country_chosen):
    dff = df[df.country.isin(country_chosen)]
    fig = px.line(data_frame=dff, x='year', y='gdpPercap', color='country', hover_data=["lifeExp", "pop", "iso_alpha"], color_discrete_map={'Germany': 'blue', 'Brazil': 'red'})
    fig.update_traces(mode='lines+markers')
    return fig

@app.callback(
    Output(component_id='pie-graph', component_property='figure'),
    [Input(component_id='my-graph', component_property='hoverData'),
     Input(component_id='dpdn2', component_property='value')]
)
def update_pie_graph(hover_data, country_chosen):
    if hover_data is None:
        dff2 = df[df.country.isin(country_chosen)]
        fig2 = px.pie(data_frame=dff2, values='pop', names='country', title='Population', color='country', color_discrete_map={'Germany': 'blue', 'Brazil': 'red'})
        return fig2
    else:
        hov_year = hover_data['points'][0]['x']
        dff2 = df[(df.country.isin(country_chosen)) & (df.year == hov_year)]
        fig2 = px.pie(data_frame=dff2, values='pop', names='country', title=f'Population for: {hov_year}', color='country', color_discrete_map={'Germany': 'blue', 'Brazil': 'red'})
        return fig2

@app.callback(
    Output(component_id='bar-graph', component_property='figure'),
    [Input(component_id='my-graph', component_property='selectedData'),
     Input(component_id='dpdn2', component_property='value')]
)
def update_bar_graph(selected_data, country_chosen):
    if selected_data:
        selected_years = [point['x'] for point in selected_data['points']]
        dff3 = df[(df.country.isin(country_chosen)) & (df.year.isin(selected_years))]
        fig3 = px.bar(data_frame=dff3, x='year', y='gdpPercap', color='country', title='GDP Per Capita for Selected Years', color_discrete_map={'Germany': 'blue', 'Brazil': 'red'})
        return fig3
    else:
        dff3 = df[df.country.isin(country_chosen)]
        fig3 = px.bar(data_frame=dff3, x='year', y='gdpPercap', color='country', title='GDP Per Capita for Selected Countries', color_discrete_map={'Germany': 'blue', 'Brazil': 'red'})
        return fig3

if __name__ == '__main__':
    app.run_server(debug=True)


