from flask import Flask, render_template, request, redirect

from db import db

from movies.models import FilmWork
 
app = Flask(__name__)
 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
 
@app.before_first_request
def create_table():
    db.create_all()
 
@app.route('/data/create' , methods = ['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template('createpage.html')
 
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        creation_date = request.form['creation_date']
        rating = request.form['rating']
        type = request.form['type']
	genres = request.form['GenreFilmWork']
	persons = request.form['PersonFilmWork']
        db.session.add(filmwork)
        db.session.commit()
        return redirect('/data')
 
 
@app.route('/data')
def RetrieveList():
    FilmWorks = FilmWork.query.all()
    return render_template('datalist.html', filmworks = filmworks)
 
 
@app.route('/data/<int:id>/update',methods = ['GET','POST'])
def update(id):
    filmwork = FilmWork.query.filter_by(filmwork_id=id).first()
    if request.method == 'POST':
        if filmwork:
        	title = request.form['title']
        	description = request.form['description']
        	creation_date = request.form['creation_date']
        	rating = request.form['rating']
        	type = request.form['type']
		genres = request.form['GenreFilmWork']
		persons = request.form['PersonFilmWork']
        	db.session.add(filmwork)
        	db.session.commit()
            	return redirect(f'/data/{id}')
        return f"Filmwork with id = {id} Does nit exist"
 
    return render_template('update.html', filmwork = filmwork)
 
 
@app.route('/data/<int:id>/delete', methods=['GET','POST'])
def delete(id):
    filmwork = FilmWork.query.filter_by(filmwork_id=id).first()
    if request.method == 'POST':
        if filmwork:
            db.session.delete(filmwork)
            db.session.commit()
            return redirect('/data')
        abort(404)
 
    return render_template('delete.html')
