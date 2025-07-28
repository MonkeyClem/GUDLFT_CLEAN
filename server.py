import json
from datetime import datetime
from flask import Flask,render_template,request,redirect,flash,url_for
from utils.utils import find_competition_by_name, is_competition_in_past, is_points_balance_valid, load_clubs, load_competitions



app = Flask(__name__)
app.secret_key = 'something_special'

competitions = load_competitions()
clubs = load_clubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    club = [club for club in clubs if club['email'] == request.form['email']][0]
    return render_template('welcome.html',club=club,competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition_name = request.form['competition']
    competition = find_competition_by_name(name = competition_name)
    club_name = request.form["club"]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    competition_date= datetime.strptime(competition["date"], "%Y-%m-%d %H:%M:%S")
    if is_competition_in_past(competition_date):
        flash("ERROR: This competition is not available anymore... Sorry")
        return redirect(url_for('book', club=club_name, competition=competition_name))
    places_required = int(request.form['places'])
    if not is_points_balance_valid(club, places_required):
        flash(f"ERROR: You do not have enough points. Your current balance: {club['points']}")
        return redirect(url_for('book', club=club_name, competition=competition_name))
    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/clubs/points', methods=['GET'])
def display_points():
    return render_template('club_points.html', clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


if __name__ == "__main__" : 
    app.run()