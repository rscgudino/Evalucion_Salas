from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', resultados=None)  # Asegúrate de pasar None a resultados

@app.route('/evaluar', methods=['POST'])
def evaluar():
    try:
        # Obtener datos del formulario y validar
        temp_exterior = float(request.form['temp_exterior'])
        temp_agua = float(request.form['temp_agua'])
        temp_sensor1 = float(request.form['temp_sensor1'])
        temp_sensor2 = float(request.form['temp_sensor2'])
        humedad_sensor1 = float(request.form['humedad_sensor1'])
        humedad_sensor2 = float(request.form['humedad_sensor2'])
        nombre_sala = request.form['nombre_sala']
        cantidad_utas = int(request.form['cantidad_utas'])

        # Obtener setpoints de UTAs y validarlos
        utas = []
        for i in range(1, cantidad_utas + 1):
            setpoint = request.form.get(f'setpoint_uta_{i}', '').strip()
            if setpoint:
                utas.append(float(setpoint))
            else:
                return f"Error: El setpoint de UTA {i} está vacío.", 400

        # Evaluar condiciones
        rango_temp_data_center = (10, 11)
        rango_temp_salas = (20, 25)
        rango_humedad = (42, 58)
        resultados = []

        # Verificación del chiller
        if temp_agua >= 12:
            resultados.append("El chiller Carrier debe encenderse para ayudar al Daikin.")
        else:
            resultados.append("El chiller Carrier está apagado.")

        # Evaluar temperaturas y humedades
        if not (rango_temp_data_center[0] <= temp_agua <= rango_temp_data_center[1]):
            resultados.append("La temperatura del data center está fuera de rango.")
        if not (rango_temp_salas[0] <= temp_sensor1 <= rango_temp_salas[1]):
            resultados.append("La temperatura en el sensor 1 está fuera de rango.")
        if not (rango_temp_salas[0] <= temp_sensor2 <= rango_temp_salas[1]):
            resultados.append("La temperatura en el sensor 2 está fuera de rango.")
        if not (rango_humedad[0] <= humedad_sensor1 <= rango_humedad[1]):
            resultados.append("La humedad en el sensor 1 está fuera de rango.")
        if not (rango_humedad[0] <= humedad_sensor2 <= rango_humedad[1]):
            resultados.append("La humedad en el sensor 2 está fuera de rango.")

        # Comparar temperaturas de las UTAs con los sensores
        for i, setpoint in enumerate(utas):
            if temp_sensor1 < setpoint:
                resultados.append(f"La temperatura en el sensor 1 está por debajo del setpoint de UTA {i + 1}.")
            elif temp_sensor1 > setpoint:
                resultados.append(f"La temperatura en el sensor 1 está por encima del setpoint de UTA {i + 1}.")
            if temp_sensor2 < setpoint:
                resultados.append(f"La temperatura en el sensor 2 está por debajo del setpoint de UTA {i + 1}.")
            elif temp_sensor2 > setpoint:
                resultados.append(f"La temperatura en el sensor 2 está por encima del setpoint de UTA {i + 1}.")

        # Sugerir movimiento de sensores
        if temp_sensor1 < rango_temp_salas[0] or temp_sensor1 > rango_temp_salas[1]:
            resultados.append("Se recomienda mover el sensor 1, ACERCAR AL PASILLO FRIO para ajustar la temperatura de la sala.")
            resultados.append("Esperar un Rango de 15 minutos después de cada modificación...")
            resultados.append("Aplicando los cambios.")

        if humedad_sensor1 < rango_humedad[0] or humedad_sensor1 > rango_humedad[1]:
            resultados.append("Se recomienda mover el sensor 1, ALEJAR DEL PASILLO FRIO para ajustar la humedad de la sala.")
            resultados.append("Esperar un Rango de 15 minutos después de cada modificación...")
            resultados.append("Aplicando los cambios.")

        if temp_sensor2 < rango_temp_salas[0] or temp_sensor2 > rango_temp_salas[1]:
            resultados.append("Se recomienda mover el sensor 2, ACERCAR AL PASILLO FRIO para ajustar la temperatura de la sala.")
            resultados.append("Esperar un Rango de 15 minutos después de cada modificación...")
            resultados.append("Aplicando los cambios.")

        if humedad_sensor2 < rango_humedad[0] or humedad_sensor2 > rango_humedad[1]:
            resultados.append("Se recomienda mover el sensor 2, ALEJAR DEL PASILLO FRIO para ajustar la humedad de la sala.")
            resultados.append("Esperar un Rango de 15 minutos después de cada modificación...")
            resultados.append("Aplicando los cambios.")

        return render_template('index.html', resultados=resultados)

    except ValueError:
        return "Error: Uno de los valores ingresados no es válido.", 400
    except Exception as e:
        return f"Ocurrió un error inesperado: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
