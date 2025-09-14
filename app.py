from flask import Flask, render_template, request
from datetime import datetime, timedelta
import locale
import calendar
import json

app = Flask(__name__)

locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")

@app.route("/", methods=["GET", "POST"])
def calendario():
    calendario_data = []
    fecha_inicio_str = ""
    dias_a_mostrar = ""
        
    # Cargar los días festivos desde el archivo JSON
    with open('data/festivo.json', encoding='utf-8') as f:
        d = json.load(f)   
        FESTIVOS = d["FESTIVOS"]


    if request.method == "POST":
        fecha_inicio_str = request.form.get("fecha_inicio")
        dias_a_mostrar = request.form.get("dias_a_mostrar")

        if fecha_inicio_str and dias_a_mostrar:
            dias_a_mostrar = int(dias_a_mostrar)
            fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d")
            dias_restantes = dias_a_mostrar
            fecha_actual = fecha_inicio

            while dias_restantes > 0:
                mes = fecha_actual.month
                anio = fecha_actual.year
                mes_nombre = fecha_actual.strftime("%B %Y").capitalize()

                primer_dia_mes = datetime(anio, mes, 1)
                ultimo_dia_mes = datetime(anio, mes, calendar.monthrange(anio, mes)[1])

                inicio_mes = max(fecha_actual, primer_dia_mes)
                dias_en_mes = min((ultimo_dia_mes - inicio_mes).days + 1, dias_restantes)

                semanas = [[]]

                for i in range(inicio_mes.weekday()):
                    dia_prev = inicio_mes - timedelta(days=inicio_mes.weekday() - i)
                    semanas[0].append({"dia": dia_prev.day, "clase": "fuera-rango"})

                fecha_iter = inicio_mes
                for _ in range(dias_en_mes):
                    if fecha_iter.strftime("%m-%d") in FESTIVOS:
                        clase = "festivo"
                    elif fecha_iter.weekday() >= 5:
                        clase = "fin-semana"
                    else:
                        clase = "laborable"                        
                    if fecha_iter < fecha_inicio:
                        clase = "fuera-rango"

                    semanas[-1].append({"dia": fecha_iter.day, "clase": clase})

                    if fecha_iter.weekday() == 6:
                        semanas.append([])

                    fecha_iter += timedelta(days=1)

                ultima_semana = semanas[-1]
                if ultima_semana and len(ultima_semana) < 7:
                    for i in range(7 - len(ultima_semana)):
                        dia_siguiente = fecha_iter + timedelta(days=i)
                        semanas[-1].append({"dia": dia_siguiente.day, "clase": "fuera-rango"})

                if semanas[-1] == []:
                    semanas.pop()

                calendario_data.append({"mes": mes_nombre, "semanas": semanas})

                fecha_actual = ultimo_dia_mes + timedelta(days=1)
                dias_restantes -= dias_en_mes

    return render_template("index.html",calendario=calendario_data,fecha_inicio=fecha_inicio_str,dias_a_mostrar=dias_a_mostrar)

if __name__ == "__main__":
    app.run(debug=True)
