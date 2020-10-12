#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from sqlalchemy import *
from datetime import *

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO (X) : connect to a local postgresql database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:1111@localhost:5432/fyyur_project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
  __tablename__ = 'venues'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable = False)
  city = db.Column(db.String(120), nullable = False)
  state = db.Column(db.String(120), nullable = False)
  phone = db.Column(db.String(120), nullable = False)
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))
  web_site = db.Column(db.String(120))
  seeking_talent_atrist = db.Column(db.Boolean, default=False)
  seeking_talent_description = db.Column(db.String(500), default='')
  
  shows = db.relationship('Show', backref='venue')
  geners = db.relationship( 'Gener', secondary = 'venue_geners', backref = db.backref('venue', lazy=True))
  addresses = db.relationship('Address', backref='venue', lazy=True)
  image_link = db.relationship("ImageLink", secondary='venue_image_links', backref=db.backref("venue", lazy=True))  

    # TODO (X) : implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
  __tablename__ = 'artists'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable = False)
  city = db.Column(db.String(120), nullable = False)
  state = db.Column(db.String(120), nullable = False)
  phone = db.Column(db.String(120), nullable = False)
  facebook_link = db.Column(db.String(120))
  web_site = db.Column(db.String(120))
  seeking_venue = db.Column(db.Boolean, default=False)
  seeking_venue_description = db.Column(db.String(500), default='')
  
  shows = db.relationship('Show', backref='artist')
  geners = db.relationship("Gener", secondary='artist_geners', backref=db.backref("artist", lazy=True))  
  image_link = db.relationship("ImageLink", secondary='artist_image_links', backref=db.backref("artist", lazy=True))  

  # TODO (X) : implement any missing fields, as a database migration using Flask-Migrate

# XTODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Show(db.Model):
  __tablename__ = 'shows'
  
  id = db.Column(db.Integer, primary_key=True)
  data_and_time = db.Column(db.String, nullable=False)
  artist_id = db.Column(db.Integer, db.ForeignKey(Artist.id), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey(Venue.id), nullable=False)
      
class Gener(db.Model):
  __tablename__ = 'geners'
  
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)

class VenueGener(db.Model):
  __tablename__ = 'venue_geners'
  
  venue_id = db.Column('venue_id', db.Integer, db.ForeignKey(Venue.id), primary_key = True)
  gener_id = db.Column('gener_id', db.Integer, db.ForeignKey(Gener.id), primary_key = True)

class ArtistGener(db.Model):
  __tablename__ = 'artist_geners'
                           
  artist_id = db.Column('artist_id', db.Integer, db.ForeignKey(Artist.id), primary_key = True)
  gener_id = db.Column('gener_id', db.Integer, db.ForeignKey(Gener.id), primary_key = True)

class Address(db.Model):
  __tablename__ = 'addresses'

  id = db.Column(db.Integer, primary_key=True)
  address = db.Column(db.String(120), nullable=False, primary_key=True)
  venue_id = db.Column(db.Integer, db.ForeignKey(Venue.id), nullable=False)
  
class ImageLink(db.Model):
    __tablename__ = 'image_links'
    id = db.Column(db.Integer, primary_key=True)
    image_link = db.Column(db.String(500))
    
class VenueImageLink(db.Model):
  __tablename__ = 'venue_image_links'
  
  venue_id = db.Column('venue_id', db.Integer, db.ForeignKey(Venue.id), primary_key = True)
  image_link_id = db.Column('image_link_id', db.Integer, db.ForeignKey(ImageLink.id), primary_key = True)

class ArtistImageLink(db.Model):
  __tablename__ = 'artist_image_links'
                           
  artist_id = db.Column('artist_id', db.Integer, db.ForeignKey(Artist.id), primary_key = True)
  image_link_id = db.Column('image_link_id', db.Integer, db.ForeignKey(ImageLink.id), primary_key = True)

  
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO (X) : replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data = []
  venues = Venue.query.order_by(Venue.state.asc(), Venue.id.asc()).all()
  city = ''
  state = ''
  
  for venue in venues:
    num_shows = len(venue.shows)
    
    if venue.city != city or venue.state != state:
      city = venue.city
      state = venue.state
      
      data.append({
        "city": venue.city,
        "state": venue.state,
        "venues": [{
          "id": venue.id,
          "name": venue.name,
          "num_upcoming_shows": num_shows
        }]
      })
      
    else:
      data[-1]['venues'].append({
        "id": venue.id,
        "name": venue.name,
        "num_upcoming_shows": num_shows
      })
      
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO (X): implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"  
  
  # inspierd from: https://stackoverflow.com/questions/3325467/sqlalchemy-equivalent-to-sql-like-statement 
  search_term = request.form.get('search_term', '')
  search = "%{}%".format(search_term)
  venues = Venue.query.filter(Venue.name.ilike(search)).all()

  response={
    "count": len(venues),
    "data": venues
  }
  return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO (X): replace with real venue data from the venues table, using venue_id
  venue = Venue.query.get(venue_id)
  venue_shows = venue.shows
  venue_geners = venue.geners
  venue_addresses = venue.addresses
  venue_image_link = venue.image_link
  
  geners = []
  address = []
  image_link = []
  past_shows = []
  upcoming_shows = []
  
  current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  for gener in venue_geners:
    geners.append(gener.name)
  
  for addres in venue_addresses:
    address.append(addres.address)
    
  for image in venue_image_link:
    image_link.append(image.image_link) 
    
  for show in venue_shows:
    time = format_datetime(show.data_and_time, format='medium')
    artist = Artist.query.get(show.artist_id)
    atrints_images = artist.image_link
    artist_image_link = []
    
    for image in atrints_images:
      artist_image_link.append(image.image_link) 
    
    image = str(artist_image_link)[2:-2]
    
    if(time >= current_time):
      past_shows.append({
        "artist_id": artist.id,
        "artist_name": artist.name,
        "artist_image_link": image,
        "start_time": show.data_and_time
      })
      
    else:
      upcoming_shows.append({
        "artist_id": artist.id,
        "artist_name": artist.name,
        "artist_image_link": image,
        "start_time": show.data_and_time
      })

  data={
    "id": venue.id,
    "name": venue.name,
    "genres": geners,
    "address": str(address)[2:-2],
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.web_site,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent_atrist,
    "seeking_description": venue.seeking_talent_description,
    "image_link": str(image_link)[2:-2],
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
  }
  
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO (x): insert form data as a new Venue record in the db, instead
  # TODO (x): modify data to be the data object returned from db insertion
  error = False
  
  try:
    new_venue = Venue()
    new_address = Address()
    new_venue_gener = VenueGener()
    new_image_link = ImageLink()
    new_venue_image_link = VenueImageLink()
    
    address = request.form.get('address','')
    image_link = request.form.get('image_link','')
    geners = request.form.getlist('genres')
    
    
    for gener in geners:
      gener_id = Gener.query.filter(Gener.name.ilike(gener)).first()
      new_venue_gener.gener_id = gener_id
      new_venue_gener.venue_id = new_venue.id
    
    new_image_link.image_link = image_link
    new_venue_image_link.image_link_id = new_image_link.id
    new_venue_image_link.venue_id = new_venue.id
    
    new_address.address = address
    new_address.venue_id = new_venue.id
    

    new_venue.name = request.form.get('name','')
    new_venue.city = request.form.get('city','')
    new_venue.state = request.form.get('state','')
    new_venue.phone = request.form.get('phone','')
    new_venue.web_site = request.form.get ('website_link','')
    new_venue.facebook_link = request.form.get ('facebook_link','')

    if request.form.get('seek_talents','') == 'yes':
      new_venue.seeking_talent_atrist = True
      new_venue.seeking_talent_description = request.form.get('seek_description','')
    else:
      new_venue.seeking_talent_atrist = False 
    
    db.session.add(new_venue)
    db.session.commit()
    
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
  # TODO (x): on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  else:
  # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>/delete', methods=['GET'])
def delete_venue(venue_id):
  # TODO (x): Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  
  # the code below inspired by udacity lessons
  try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
  except:
    db.session.rollback()
    flash('There was an issue in deleting')
  finally:
    db.session.close()
    flash('Venue was successfully deleted!')
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO (x): replace with real data returned from querying the database
  data = []
  artists = Artist.query.order_by(Artist.name.asc()).all()

  for artist in artists:      
    data.append({
      "id": artist.id,
      "name": artist.name,
    })

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO (x): implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get('search_term', '')
  search = "%{}%".format(search_term)
  artists = Artist.query.filter(Artist.name.ilike(search)).all()

  response={
    "count": len(artists),
    "data": artists
  }

  return render_template('pages/search_artists.html', results=response, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO (x): replace with real venue data from the venues table, using venue_id
  
  artist = Artist.query.get(artist_id)
  artist_shows = artist.shows
  artist_geners = artist.geners
  artist_image_link = artist.image_link
  
  geners = []
  image_link = []
  past_shows = []
  upcoming_shows = []
  
  current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  for gener in artist_geners:
    geners.append(gener.name)
      
  for image in artist_image_link:
    image_link.append(image.image_link) 
    
  for show in artist_shows:
    time = format_datetime(show.data_and_time, format='medium')
    artist = Artist.query.get(show.artist_id)
    atrints_images = artist.image_link
    artist_image_link = []
    
    for image in atrints_images:
      artist_image_link.append(image.image_link) 
    
    image = str(artist_image_link)[2:-2]
    
    if(time >= current_time):
      past_shows.append({
        "artist_id": artist.id,
        "artist_name": artist.name,
        "artist_image_link": image,
        "start_time": show.data_and_time
      })
      
    else:
      upcoming_shows.append({
        "artist_id": artist.id,
        "artist_name": artist.name,
        "artist_image_link": image,
        "start_time": show.data_and_time
      })

  data={
    "id": artist.id,
    "name": artist.name,
    "genres": geners,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.web_site,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_venue_description,
    "image_link": str(image_link)[2:-2],
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
  }
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):

  artist = Artist.query.get(artist_id)
  artist_geners = artist.geners
  artist_image_link = artist.image_link
  
  geners = []
  image_link = []
  
  for gener in artist_geners:
    geners.append(gener.name)
      
  for image in artist_image_link:
    image_link.append(image.image_link) 


  form = ArtistForm(
    name = artist.name,
    city = artist.city,
    state = artist.state,
    phone = artist.phone,
    facebook_link = artist.facebook_link,
    website = artist.web_site,
    seeking_venue = artist.seeking_venue,
    seeking_description = artist.seeking_venue_description,
    image_link = str(image_link)[2:-2],
    genres = str(image_link)[2:-2]
  )  
  # TODO (x): populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO (x): take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  error = False
  
  try:
    current_artist = Artist.query.get(artist_id)
    
    # new_image_link = request.form.get('image_link','')
    # ImageLink.query.filter_by(image_link=current_artist.image_link).destroy()
    # new_image_link = ImageLink()
    # new_image_link.image_link = new_image_link
    
    # ArtistImageLink.query.filter_by(artist_id=artist_id).delete()
    # new_artist_image_link = ArtistImageLink()
    # new_artist_image_link.artist_id = artist_id
    # new_artist_image_link.image_link_id = new_image_link.id
    # new_geners = request.form.getlist('genres')
    # if new_geners != []:
    #   ArtistGener.query.filter(artist_id=artist_id).delete()
    #   current_artist_gener = ArtistGener()
    #   current_artist_gener.artist_id = artist_id
    # else:
    #   current_artist_gener = ArtistGener.query.filter_by(artist_id=artist_id).find()[0]
    
    # for gener in new_geners:
    #   gener_found = Gener.query.filter(Gener.name.ilike(gener)).all()[0]
    #   current_artist_gener.gener_id = gener_found.id
    
    current_artist.name = request.form.get('name','')
    current_artist.city = request.form.get('city','')
    current_artist.state = request.form.get('state','')
    current_artist.phone = request.form.get('phone','')
    current_artist.web_site = request.form.get ('website','')
    current_artist.facebook_link = request.form.get ('facebook_link','')

    if request.form.get('seek_venue','') == 'yes':
      current_artist.seeking_venue = True
      current_artist.seeking_venue_description = request.form.get('seek_description','')
    else:
      current_artist.seeking_venue = False 
    
    db.session.commit()
    
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
  # TODO (x): on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be edited.')
  else:
  # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully edited!')
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.get(venue_id)
  venue_geners = venue.geners
  venue_image_link = venue.image_link
  venue_address = venue.addresses
  
  geners = []
  image_link = []
  addresses = []
  
  for gener in venue_geners:
    geners.append(gener.name)
      
  for image in venue_image_link:
    image_link.append(image.image_link) 
    
  for address in venue_address:
    addresses.append(address.address) 


  form = VenueForm(
    name = venue.name,
    city = venue.city,
    state = venue.state,
    phone = venue.phone,
    facebook_link = venue.facebook_link,
    website = venue.web_site,
    seeking_venue = venue.seeking_talent_atrist,
    seeking_description = venue.seeking_talent_description,
    image_link = str(image_link)[2:-2],
    genres = str(image_link)[2:-2],
    address = str(addresses)[2:-2]
  )  
  # TODO (x): populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO (x): take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  
  error = False
  
  try:
    current_venue = Venue.query.get(venue_id)
    
    # new_image_link = request.form.get('image_link','')
    # ImageLink.query.filter_by(image_link=current_venue.image_link).destroy()
    # new_image_link = ImageLink()
    # new_image_link.image_link = new_image_link
    
    # VenueImageLink.query.filter_by(venue_id=venue_id).delete()
    # new_venue_image_link = VenueImageLink()
    # new_venue_image_link.venue_id = venue_id
    # new_venue_image_link.image_link_id = new_image_link.id
    # new_geners = request.form.getlist('genres')
    # if new_geners != []:
    #   VenueGener.query.filter(venue_id=venue_id).delete()
    #   current_venue_gener = VenueGener()
    #   current_venue_gener.venue_id = venue_id
    # else:
    #   current_venue_gener = VenueGener.query.filter_by(venue_id=venue_id).find()[0]
    
    # for gener in new_geners:
    #   gener_found = Gener.query.filter(Gener.name.ilike(gener)).all()[0]
    #   current_venue_gener.gener_id = gener_found.id
    
    current_venue.name = request.form.get('name','')
    current_venue.city = request.form.get('city','')
    current_venue.state = request.form.get('state','')
    current_venue.phone = request.form.get('phone','')
    current_venue.web_site = request.form.get ('website','')
    current_venue.facebook_link = request.form.get ('facebook_link','')

    if request.form.get('seek_talent','') == 'yes':
      current_venue.seeking_talent_atrist = True
      current_venue.seeking_talent_description = request.form.get('seek_description','')
    else:
      current_venue.seeking_venue = False 
    
    db.session.commit()
    
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
  # TODO (x): on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be edited.')
  else:
  # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully edited!')
    
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO (x): insert form data as a new Venue record in the db, instead
  # TODO (x): modify data to be the data object returned from db insertion
  error = False
  
  try:
    new_artist = Artist()
    new_artist_gener = ArtistGener()
    new_image_link = ImageLink()
    new_artist_image_link = ArtistImageLink()
    
    image_link = request.form.get('image_link','')
    geners = request.form.getlist('genres')
    
    
    for gener in geners:
      gener_id = Gener.query.filter(Gener.name.ilike(gener)).first()
      new_artist_gener.gener_id = gener_id
      new_artist_gener.artist_id = new_artist.id
    
    new_image_link.image_link = image_link
    new_artist_image_link.image_link_id = new_image_link.id
    new_artist_image_link.artist_id = new_artist.id

    new_artist.name = request.form.get('name','')
    new_artist.city = request.form.get('city','')
    new_artist.state = request.form.get('state','')
    new_artist.phone = request.form.get('phone','')
    new_artist.web_site = request.form.get ('website_link','')
    new_artist.facebook_link = request.form.get ('facebook_link','')

    if request.form.get('seek_talents','') == 'yes':
      new_artist.seeking_venue = True
      new_artist.seeking_venue_description = request.form.get('seek_description','')
    else:
      new_artist.seeking_venue = False 
    
    db.session.add(new_artist)
    db.session.commit()
    
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
  # TODO (x): on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
  else:
  # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO (x): replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  shows = Show.query.all()
  data = []
  for show in shows:
    venue = Venue.query.get(show.venue_id)
    artist = Artist.query.get(show.artist_id)
    atrints_images = artist.image_link
    artist_image_link = []
    
    for image in atrints_images:
      artist_image_link.append(image.image_link) 
    
    data.append({
        "venue_id": venue.id,
        "venue_name": venue.name,
        "artist_id": artist.id,
        "artist_name": artist.name,
        "artist_image_link": str(artist_image_link)[2:-2],
        "start_time": show.data_and_time
      })
  
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO (x): insert form data as a new Show record in the db, instead

  error = False
    
  try:
    new_show = Show()
        
    new_show.artist_id = request.form.get('artist_id','')
    new_show.venue_id = request.form.get('venue_id','')
    new_show.data_and_time = request.form.get('start_time','')
        
    db.session.add(new_show)
    db.session.commit()
    
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    flash('An error occurred. Show could not be listed.')
  else:
  # on successful db insert, flash success
    flash('Show was successfully listed!')
  # TODO (x): on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
