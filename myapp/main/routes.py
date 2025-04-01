
from flask import Blueprint, render_template, request
from myapp.main.data_file import matches_list
import pandas as pd

main = Blueprint('main', __name__)


@main.route("/", methods=["GET", "POST"])
def home():
    match_data = matches_list
    if request.method == "POST":
        team_name = (request.form.get("team_name")).upper()
        venue_city_name = (request.form.get("venue_city_name")).title()
        data = pd.DataFrame(matches_list)

        if len(team_name) != 0 and len(venue_city_name) != 0:
            team_matches = data[(data["team 1"] == team_name) | (data["team 2"] == team_name)]
            selected_city_matches = team_matches[team_matches["venue city"] == venue_city_name]
            combined_match_df = pd.DataFrame(selected_city_matches)
            team_venue_match_list = combined_match_df.to_dict(orient="records")
            return render_template('index.html', full_data=team_venue_match_list)

        elif len(team_name) != 0:
            team_matches = data[(data["team 1"] == team_name) | (data["team 2"] == team_name)]
            match_df = pd.DataFrame(team_matches)
            team_match_list = match_df.to_dict(orient="records")
            return render_template('index.html', full_data=team_match_list)

        elif len(venue_city_name) != 0:
            city_matches = data[data["venue city"] == venue_city_name]
            city_df = pd.DataFrame(city_matches)
            city_matches_list = city_df.to_dict(orient="records")
            return render_template('index.html', full_data=city_matches_list)

    return render_template('index.html', full_data=match_data, title='home')


