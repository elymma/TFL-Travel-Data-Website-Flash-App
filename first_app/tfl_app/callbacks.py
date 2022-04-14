import json
import dash
from dash import html, Output, Input
from dash import dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

from .layout import df


def register_callbacks(dash_app):
    @dash_app.callback([Output("box", "figure"),
                        Output("pie", "figure"),
                        Output("line", "figure"),
                        Output("stats-card", "children")],
                       Input("select-year", "value"))
    def update_tfl_chart(year_select):
        # Create a copy of dataset
        df.chosen_year = df.copy()
        # Select the data for chosen year
        if type(year_select) != int:
            # For when there is a list of year values
            df.chosen_year = df.chosen_year[
                df.chosen_year["Period ending"].dt.year.isin(year_select)]
        else:
            # For when there is only one year value
            df.chosen_year = df.chosen_year[df.chosen_year["Period ending"].dt.year == year_select]
        # Create figures
        fig_box_update = px.box(df.chosen_year, x="Travel Mode", y="Journeys (m)", color="Travel Mode",
                                title="Variation in Travel Modes<br><sup>Year(s) shown: {}</sup>".format(year_select))
        fig_pie_update = px.pie(df.chosen_year, values="Journeys (m)", names="Travel Mode",
                                title="Distribution of Travel Modes<br><sup>Year(s) shown: {}</sup>".format(
                                    year_select))
        fig_line_update = px.line(df.chosen_year, x="Period ending", y="Journeys (m)", color="Travel Mode",
                                  title="Travel Mode Usage Over Time<br><sup>Year(s) shown: {}</sup>".format(
                                      year_select))
        # Order data in descending/ascending order
        desc_order = df.chosen_year.sort_values("Journeys (m)", ascending=False)
        asc_order = df.chosen_year.sort_values("Journeys (m)", ascending=True)
        # Check if any years have been selected
        if type(year_select) != int and len(year_select) == 0:
            # Generate an empty stats card if no year is chosen
            stats_card = dbc.Card(className="bg-light text-dark", children=[
                dbc.CardBody([
                    html.H3("Statistics Panel".format(year_select), id="card-name", className="card-title"),
                    html.H6("No statistics to be shown"),
                    html.Br(),

                ])
            ], color="light")
        else:
            # If at least one year is chosen, store the data for the highest and lowest recording periods
            max_journeys = desc_order.iloc[0, 4]
            max_period_b = desc_order.iloc[0, 1]
            max_period_e = desc_order.iloc[0, 2]
            max_mode = desc_order.iloc[0, 3]
            min_journeys = asc_order.iloc[0, 4]
            min_period_b = asc_order.iloc[0, 1]
            min_period_e = asc_order.iloc[0, 2]
            min_mode = asc_order.iloc[0, 3]
            # Generate a filled out stats card with the data in readable formats
            stats_card = dbc.Card(className="bg-light text-dark", children=[
                dbc.CardBody([
                    html.H3("Statistics Panel".format(year_select), id="card-name", className="card-title"),
                    html.H6("Year(s) shown: {}".format(year_select)),
                    html.Br(),
                    html.H5("Busiest Period:", className="card-title"),
                    html.H6("The recording period with the most journeys was {} to {}.".format(
                        max_period_b.strftime("%d/%m/%Y"), max_period_e.strftime("%d/%m/%Y")),
                        className="card-text text-dark"),
                    html.Br(),
                    html.H6(
                        "There were {} million journeys using the {}.".format(format(max_journeys, ".1f"), max_mode),
                        className="card-text text-dark"),
                    html.Br(),
                    html.H5("Quietest Period:", className="card-title"),
                    html.H6("The recording period with the least journeys was {} to {}.".format(
                        min_period_b.strftime("%d/%m/%Y"), min_period_e.strftime("%d/%m/%Y")),
                        className="card-text text-dark"),
                    html.Br(),
                    html.H6(
                        "There were {} million journeys using the {}.".format(format(min_journeys, ".1f"), min_mode),
                        className="card-text text-dark"),
                    html.Br()
                ])
            ], color="light")
        return fig_box_update, fig_pie_update, fig_line_update, stats_card

# if __name__ == '__main__':
#    app.run_server(debug=True)
