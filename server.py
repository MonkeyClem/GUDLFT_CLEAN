import json
from datetime import datetime
from flask import Flask,render_template,request,redirect,flash,url_for
from utils.utils import (
    exceed_club_points,
    find_club_by_email,
    find_club_by_name,
    loadClubs,
    loadCompetitions
)
from utils.utils import exceeds_max_places_per_booking, loadClubs, loadCompetitions



app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()


WELCOME_PAGE = "welcome.html"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/show_summary',methods=['POST'])
def show_summary():
    email = request.form["email"]
    matched_club = find_club_by_email(email= email, clubs=clubs)
    if matched_club is None: 
        flash("ERROR : Unknown e-mail")
        return redirect(url_for('index'))
    return render_template(WELCOME_PAGE, club=matched_club ,competitions=competitions)



@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template(WELCOME_PAGE, club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition_name = request.form['competition']
    competition = next((c for c in competitions if c['name'] == competition_name), None)
    if not competition:
        flash("ERROR: Competition not found.")
        return redirect(url_for('showSummary'))
    club_name = request.form["club"]
    club = find_club_by_name(club_name=club_name)
    club_available_points = int(club['points'])
    print("club_available_points => ", club_available_points)
    placesRequired = int(request.form['places'])
    if exceed_club_points(required_places=placesRequired, club_available_points=club_available_points):
        flash("ERROR: You do not have enough points to book these places.")
        return redirect(url_for('book', club=club_name, competition=request.form['competition']))
    else :
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
        club['points'] = club_available_points - placesRequired
        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/clubs/points', methods=['GET'])
def display_points():
    return render_template('club_points.html', clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
