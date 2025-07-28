import json
from datetime import datetime
from flask import Flask,render_template,request,redirect,flash,url_for
from utils.utils import find_competition_by_name, is_competition_in_past, load_clubs, load_competitions



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


@app.route('/purchase_place',methods=['POST'])
def purchase_place():
    competition_name = request.form['competition']
    competition = find_competition_by_name(name = competition_name)
    club_name = request.form["club"]
    competition_date= datetime.strptime(competition["date"], "%Y-%m-%d %H:%M:%S")
    if is_competition_in_past(competition_date):
        flash("ERROR: This competition is not available anymore... Sorry")
        return redirect(url_for('book', club=club_name, competition=competition_name))
    club = [c for c in clubs if c['name'] == request.form['club']]
    places_required = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-places_required
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))