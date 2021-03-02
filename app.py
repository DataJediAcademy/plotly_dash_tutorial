import plotly.graph_objects as go
from plotly.subplots import make_subplots

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import dash
import pandas as pd
# -----------------------------------------------------------------------------------------------------
# Start our app and import external stylesheet
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets,
                title='Data Jedi Covid Dashboard',
                meta_tags=[{"name": "viewport", "content": "width=device-width"}]
                )
# -----------------------------------------------------------------------------------------------------
# Import and clean data
covid_df = pd.read_csv("./data/owid-covid-data.csv")

# -----------------------------------------------------------------------------------------------------
# Create function that takes data and plots it


def plot_figure(start_date, end_date, data=covid_df, location='Nigeria'):
    df = data.query(f"date >= '{start_date}' & date <= '{end_date}' & location == '{location}'")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['date'], y=df['new_cases_per_million'], mode='lines',
                             name='New Cases per million'))
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                      title=f"{location} Covid-19 New Cases per million",
                      )
    return fig

# -----------------------------------------------------------------------------------------------------
# App layout


app.layout = html.Div(
    [
        html.Div(
            [
                html.Img(
                    src=app.get_asset_url("DATA-JEDI.png"),
                    className="two columns",
                    id="datajedi-logo",
                ),
                html.H2(
                    "Covid-19 Dashboard",
                    id="title",
                    className="ten columns",
                    style={"margin-left": "3%"},
                ),

            ],
            className="row",
        ),

        html.Div(
            [
                html.Div(
                    [
                        html.P("Date Range:"),
                        dcc.DatePickerRange(
                            id='date-range-picker',
                            min_date_allowed=covid_df['date'].min(),
                            max_date_allowed=covid_df['date'].max(),
                            start_date=covid_df['date'].min(),
                            end_date=covid_df['date'].max(),
                            display_format='DD/MM/YY',
                        ),
                        html.H6("Chart Details"),
                        html.P("This graph helps us explore how Covid-19 has affected the world. The data can be "
                               "downloaded from Our World in Data"),
                    ],
                    # id='left-columns',
                    # className='three columns',
                ),
                html.Div(
                    [dcc.Graph(id='covid_chart')],
                    id='right-columns',
                    # className="nine columns",
                ),
            ],
            className="row",
        ),
    ]
)
# -----------------------------------------------------------------------------------------------------
# Create callbacks to make our app interactive


@app.callback(
    Output('covid_chart', 'figure'),
    [Input('date-range-picker', 'start_date'),
     Input('date-range-picker', 'end_date'),
     ]
)
def update_risk_graph(start_date, end_date):
    return plot_figure(start_date=start_date, end_date=end_date)

# -----------------------------------------------------------------------------------------------------
# Launch our app on our local machine


if __name__ == '__main__':
    app.run_server(debug=True)
