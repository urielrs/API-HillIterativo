from flask import Flask, request, jsonify, render_template
import math
import random

app = Flask(__name__)

# Datos globales para guardar las ciudades
ciudades = {}

def distancia(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

def evalua_ruta(ruta):
    total = 0
    for i in range(len(ruta) - 1):
        total += distancia(ciudades[ruta[i]], ciudades[ruta[i + 1]])
    total += distancia(ciudades[ruta[-1]], ciudades[ruta[0]])
    return total

def i_hill_climbing():
    nombres = list(ciudades.keys())
    mejor_ruta = nombres[:]
    random.shuffle(mejor_ruta)
    mejor_dist = evalua_ruta(mejor_ruta)
    max_iteraciones = 10

    while max_iteraciones > 0:
        ruta = nombres[:]
        random.shuffle(ruta)
        mejora = True

        while mejora:
            mejora = False
            dist_actual = evalua_ruta(ruta)
            for i in range(len(ruta)):
                for j in range(i + 1, len(ruta)):
                    ruta_tmp = ruta[:]
                    ruta_tmp[i], ruta_tmp[j] = ruta_tmp[j], ruta_tmp[i]
                    dist_tmp = evalua_ruta(ruta_tmp)
                    if dist_tmp < dist_actual:
                        ruta = ruta_tmp
                        dist_actual = dist_tmp
                        mejora = True

        if dist_actual < mejor_dist:
            mejor_ruta = ruta
            mejor_dist = dist_actual

        max_iteraciones -= 1

    return mejor_ruta, mejor_dist

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_city', methods=['POST'])
def add_city():
    data = request.get_json()
    nombre = data['nombre']
    lat = float(data['lat'])
    lon = float(data['lon'])
    ciudades[nombre] = (lat, lon)
    return jsonify({'message': 'Ciudad agregada', 'ciudades': list(ciudades.keys())})

@app.route('/get_cities', methods=['GET'])
def get_cities():
    return jsonify({'ciudades': list(ciudades.keys())})

@app.route('/solve', methods=['GET'])
def solve():
    if len(ciudades) < 2:
        return jsonify({'error': 'Agrega al menos 2 ciudades'})
    mejor_ruta, mejor_dist = i_hill_climbing()
    return jsonify({'ruta': mejor_ruta, 'distancia': mejor_dist})

if __name__ == '__main__':
    app.run(debug=True)
