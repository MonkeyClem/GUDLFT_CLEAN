import json
from flask import Flask,render_template,request,redirect,flash,url_for
<<<<<<< HEAD
from utils.utils import (
    find_club_by_email,
    loadClubs,
    loadCompetitions
)
=======
from utils.utils import exceeds_max_places_per_booking, loadClubs, loadCompetitions
>>>>>>> fix/max-places-12



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


@app.route('/purchase_places',methods=['POST'])
def purchase_places():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    places_required = int(request.form['places'])
    if exceeds_max_places_per_booking(places_required):
        flash("ERROR: You can not book more than 12 places")
        return redirect(url_for('book', club=club["name"], competition=competition["name"]))

    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-places_required
    flash('Great-booking complete!')
    return render_template(WELCOME_PAGE, club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))



if __name__ == "__main__":
    app.run(debug=True)
