import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for
from utils.utils import (
    exceed_club_points,
    find_club_by_email,
    find_club_by_name,
    is_competition_in_past,
    is_points_balance_valid,
    exceeds_max_places_per_booking,
    load_clubs,
    load_competitions,
)


app = Flask(__name__)
app.secret_key = "something_special"

competitions = load_competitions()
clubs = load_clubs()


WELCOME_PAGE = "welcome.html"
BOOKING_PAGE = "booking.html"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/show_summary", methods=["POST"])
def show_summary():
    email = request.form["email"]
    matched_club = find_club_by_email(email=email, clubs=clubs)
    if matched_club is None:
        flash("ERROR : Unknown e-mail")
        return redirect(url_for("index"))
    return render_template(WELCOME_PAGE, club=matched_club, competitions=competitions)


@app.route("/book/<competition>/<club>")
def book(competition, club):
    found_club = next((c for c in clubs if c["name"] == club), None)
    found_competition = [c for c in competitions if c["name"] == competition]
    found_competition = found_competition[0] if found_competition else None
    if found_club and found_competition:
        return render_template(
            BOOKING_PAGE, club=found_club, competition=found_competition
        )
    else:
        flash("Something went wrong-please try again")
        return render_template(WELCOME_PAGE, club=found_club, competitions=competitions)
    

@app.route("/purchase_places", methods=["POST"])
def purchase_places():
    competition_name = request.form["competition"]
    competition = next((c for c in competitions if c["name"] == competition_name), None)
    if not competition:
        flash("ERROR: Competition not found.")
        return redirect(url_for("index"))
    club_name = request.form["club"]
    club = find_club_by_name(club_name=club_name)
    club_available_points = int(club["points"])
    competition_date = datetime.strptime(competition["date"], "%Y-%m-%d %H:%M:%S")
    if is_competition_in_past(competition_date):
        flash("ERROR: This competition is not available anymore... Sorry")
        return render_template(BOOKING_PAGE, club=club, competition=competition)
    places_required = int(request.form['places'])
    error_msg = validate_places_request(places_required, int(competition['numberOfPlaces']))
    if error_msg:
        flash(error_msg)
        return redirect(url_for("book", competition=competition["name"], club=club))
    if exceeds_max_places_per_booking(places_required):
        flash("ERROR: You cannot book more than 12 places per competition.")
        return render_template(BOOKING_PAGE, club=club, competition=competition)
    if exceed_club_points(
        required_places=places_required, club_available_points=club_available_points
    ):
        flash("ERROR: You do not have enough points to book these places.")
        return render_template(BOOKING_PAGE, club=club, competition=competition)
    if places_required <= 0:
        flash("You must book at least 1 place")
        return render_template(BOOKING_PAGE, club=club, competition=competition)
    if places_required > int(competition["numberOfPlaces"]):
        flash("Not enough places available")
        return render_template(BOOKING_PAGE, club=club, competition=competition)
    else:
        competition["numberOfPlaces"] = (
            int(competition["numberOfPlaces"]) - places_required
        )
        club["points"] = club_available_points - places_required
        flash("Great-booking complete!")
        return render_template(WELCOME_PAGE, club=club, competitions=competitions)


@app.route("/clubs/points", methods=["GET"])
def display_points():
    return render_template("club_points.html", clubs=clubs)


@app.route("/logout")
def logout():
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
