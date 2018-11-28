from flask import Flask, session, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://movie-db:movie-db@localhost:8889/movie-db'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Movie(db.Model):
    __tablename__ = 'Movie'
    id = db.Column(db.Integer, primary_key=True)
    release_year = db.Column(db.Integer)
    title = db.Column(db.String(500))
    origin = db.Column(db.String(500))
    director = db.Column(db.String(500))
    cast = db.Column(db.String(1000))     
    genre = db.Column(db.String(500))  
    wiki = db.Column(db.String(500))
    plot = db.Column(db.String(500))

    def __init__(self, release_year, title, origin, director, cast, genre, wiki, plot):
        self.release_year = release_year
        self.title = title
        self.origin = origin
        self.director = director
        self.cast = cast 
        self.genre = genre
        self.wiki = wiki
        self.plot = plot
    
    def __repr__(self):
        return '<Movie %r>' % self.title


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/movies")
def movie_listing():

    if len(request.args) == 0:
        movies = Movie.query.all()
        
        if len(movies) > 0:
            return render_template('movies.html', movies=movies)

        else: 
            return render_template('movies.html')
    
    elif request.args.get('id') != None:
        id = request.args.get('id', '')
        movie = Movie.query.get(id)
        title = movie.title
        release_year = movie.release_year
        origin = movie.origin
        director = movie.director
        cast = movie.cast 
        genre = movie.genre
        wiki = movie.wiki
        plot = movie.plot

        return render_template('movie-page.html', movie=movie, title=title, release_year=release_year, origin=origin, director=director, cast=cast, genre=genre, wiki=wiki, plot=plot)


@app.route('/add', methods=['GET','POST'])
def add_movie():
    
    if request.method == 'POST':
        release_year = request.form['release_year'] 
        title = request.form['title']
        origin = request.form['origin']
        director = request.form['director']
        cast = request.form['cast']
        genre = request.form['genre']
        wiki = request.form['wiki']
        plot = request.form['plot']

        new_movie = Movie(release_year, title, origin, director, cast, genre, wiki, plot)
        db.session.add(new_movie)
        db.session.commit()
        return redirect('/movies')

    return render_template('add-movie.html')


@app.route('/edit', methods=['GET','POST'])
def edit_movie():

    id = request.args.get('id', '')
    movie = Movie.query.get(id)

    if request.method == 'POST':
        release_year = request.form['release_year'] 
        title = request.form['title']
        origin = request.form['origin']
        director = request.form['director']
        cast = request.form['cast']
        genre = request.form['genre']
        wiki = request.form['wiki']
        plot = request.form['plot']

        movie.title = title
        movie.release_year = release_year 
        movie.origin = origin
        movie.director = director
        movie.cast = cast
        movie.genre = genre
        movie.wiki = wiki
        movie.plot = plot

        db.session.commit()
        return render_template('edited.html', movie=movie)
    
    return render_template('edit-movie.html', movie=movie)



#ADD PAGE - ARE YOU SURE?
@app.route('/delete')
def delete_movie():
    id = request.args.get('id', '')
    movie = Movie.query.get(id)
    db.session.delete(movie)
    db.session.commit() 
    return render_template('delete-movie.html', movie=movie)



@app.route('/search', methods=['GET','POST'])
def search():

    if request.method == 'POST':

        title = request.form['title']
        if len(title) > 0:
            movie = Movie.query.filter_by(title=title).first()
            #CATCH ERROR
            id = movie.id
            return redirect("/movies?id="+ str(id))

        release_year = request.form['release_year']
        if len(release_year) > 0:
            movie = Movie.query.filter_by(release_year=release_year).first()
            #CATCH ERROR
            id = movie.id
            return redirect("/movies?id="+ str(id))

        origin = request.form['origin']
        if len(origin) > 0:
            movie = Movie.query.filter_by(origin=origin).first()
            #CATCH ERROR
            id = movie.id
            return redirect("/movies?id="+ str(id))

        director = request.form['director']
        if len(director) > 0:
            movie = Movie.query.filter_by(director=director).first()
            #CATCH ERROR
            id = movie.id
            return redirect("/movies?id="+ str(id))

        genre = request.form['genre']
        if len(genre) > 0:
            movie = Movie.query.filter_by(genre=genre).first()
            #CATCH ERROR
            id = movie.id
            return redirect("/movies?id="+ str(id))

    return render_template('search.html')


if __name__ == "__main__":
    app.run()

