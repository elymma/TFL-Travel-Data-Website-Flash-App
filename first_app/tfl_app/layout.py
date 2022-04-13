import dash
from dash import html, Output, Input
from dash import dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from pathlib import Path

# App styling details
external_stylesheets = [dbc.themes.LUX]
app = dash.Dash(__name__, routes_pathname_prefix="/tfl_app/", external_stylesheets=external_stylesheets)
background = "#F8F9F9"

# Data processing and chart creation

# Import data
df_file = Path(__file__).parent.joinpath("data", "cleaned_tfl_dataset_EDIT.xlsx")
df = pd.read_excel(df_file)

# Group dataset by recording period year
df.by_year = df.groupby(df["Period ending"].map(lambda x: x.year))
# Sum the number of journeys for each year
df.by_year_sums = df.by_year.sum()
# Convert index ("Period ending") to a column
df.by_year_sums.reset_index(level=0, inplace=True)
# Create a list of the years
df.years_list = df.by_year_sums["Period ending"].tolist()
# Create the figures
fig_line = px.line(df, x="Period ending", y="Journeys (m)", color="Travel Mode", title="Travel Mode Usage Over Time")
fig_pie = px.pie(df, values="Journeys (m)", names="Travel Mode", title="Distribution of Travel Modes")
fig_box = px.box(df, x="Travel Mode", y="Journeys (m)", color="Travel Mode", title="Variation in Travel Modes")

# App components and layout

# Create website header
header = [
    dbc.Row([
        dbc.Col(html.Div(
            dbc.Button("[logo]", outline=True, color="secondary"),
        ), lg=2),
        dbc.Col(html.Div([
            html.H1("TFL TRAVEL DASHBOARD")]), width={"size": 6}),
        dbc.Col(html.Div([
            dbc.Button("message", outline=True, color="secondary"),
            dbc.Button("profile", outline=True, color="secondary"),
            dbc.Button("log out", outline=True, color="secondary"),
        ]), lg=4),
    ])
]

# Create dropdown
dropdown = [
    dcc.Dropdown(id="select-year",
                 options=[{"label": x, "value": x} for x in df.years_list],
                 multi=True,
                 value=df.years_list[0],
                 style={'width': '70%'}
                 )
]

# Create app layout
layout = dbc.Container(children=[
    html.Div(style={"backgroundColor": background}, children=[

    dbc.Container([
        dbc.Row(
            html.Br()
        ),
        dbc.Row(
            header,
            justify="between",
        ),
        dbc.Row(
            html.Br()
        ),
        dbc.Row([
            dbc.Col(dropdown, lg=6, xs=12),
            dbc.Col(html.Div(id="dd_output_container")),
        ]),
        dbc.Row(
            html.Br()
        ),
        dbc.Row([
            dbc.Col(html.Div([dcc.Graph(id="line", figure=fig_line)], style={"border": "1px Gainsboro solid"}), lg=8,
                    xs=12),
            dbc.Col(html.Div(
                html.Div(id="stats-card", style={"border": "1px Gainsboro solid"})), lg=4, xs=12)
        ]),
        dbc.Row(
            html.Br()
        ),
        dbc.Row([
            dbc.Col(html.Div([dcc.Graph(id="box", figure=fig_box)], style={"border": "1px Gainsboro solid"}),
                    lg=6,
                    xs=12),
            dbc.Col(html.Div([dcc.Graph(id="pie", figure=fig_pie)], style={"border": "1px Gainsboro solid"}),
                    lg=6,
                    xs=12),
        ]),
        dbc.Row(
            html.Br()
        )
    ])
])

],
    fluid=True,
)
