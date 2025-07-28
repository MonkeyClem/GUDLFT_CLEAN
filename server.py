import json
from flask import Flask,render_template,request,redirect,flash,url_for
from utils.utils import (
    find_club_by_email,
    loadClubs,
    loadCompetitions
)



app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

welcome_page = 'welcome.html'

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
    return render_template(welcome_page, club=matched_club ,competitions=competitions)



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
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
