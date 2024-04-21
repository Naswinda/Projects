from dash import Dash, dcc, html
import plotly.express as px
import dask.dataframe as dd

app = Dash(__name__)

df = dd.read_csv('https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')


def filter_df(pop_thresh):
    filt_df = df[df["population"] > pop_thresh].compute()  # Note the use of .compute() function
    return filt_df


def build_graphs():
    pop_thresh = 5 * 10 ** 6
    filt_df = filter_df(pop_thresh)

    fig_out = px.scatter(filt_df, x="gdp per capita", y="life expectancy",
                         size="population", color="continent", hover_name="country",
                         log_x=True, size_max=60)
    return fig_out


fig = build_graphs()

app.layout = html.Div([
    dcc.Graph(
        id='life-exp-vs-gdp',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run(debug=True)