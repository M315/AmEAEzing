from flask import Flask, render_template, request
import os
from flask_bootstrap import Bootstrap
from flask_fontawesome import FontAwesome
from laberinto import *

import sys
sys.setrecursionlimit(30000)


app = Flask(__name__)
Bootstrap(app)
fa = FontAwesome(app)

@app.route('/candidatos')
def candidatos():
	global laberinto
	candidatos=buscaCandidatos(laberinto.current,laberinto)
	for candidato in candidatos:
		laberinto.laberinto[candidato.x][candidato.y]='C'
	return render_template('index.html', layout=laberinto.laberinto)

@app.route('/nuevo', methods=['POST'])
def nuevo():
	global laberinto

	x = 30
	y = 85
	numObstaculos = 0.35

	for item in request.form.to_dict():
		if item=="filas":
			x=int(request.form.to_dict()[item])
		if item=="columnas":
			y=int(request.form.to_dict()[item])
		if item=="obstaculos":
			numObstaculos=float(request.form.to_dict()[item])


	laberinto = Laberinto(x, y,numObstaculos)
	return render_template('index.html', layout=laberinto.laberinto)

@app.route('/solve')
def next():
	global laberinto
	resolverLaberinto(laberinto)

	return render_template('index.html', layout=laberinto.laberinto)



@app.route('/')
def index():
	return nuevo()

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000)) 
	app.run(debug=True, port=port)
