from flask import Flask, render_template, request
from datetime import datetime, timedelta
import locale

app = Flask(__name__)

locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")

FESTIVOS = ["01-01", "02-05", "03-18", "05-01", "09-16", "11-20", "12-25"]

@app.route("/", methods=["GET", "POST"])
def calendario():
    calendario_data = []
    fecha_inicio_str = ""
    dias_a_mostrar = ""

    if request.method == "POST":
        fecha_inicio_str = request.form.get("fecha_inicio")
        dias_a_mostrar = request.form.get("dias_a_mostrar")

        if fecha_inicio_str and dias_a_mostrar:
            dias_a_mostrar = int(dias_a_mostrar)
            fecha = datetime.strptime(fecha_inicio_str, "%Y-%m-%d")
            fecha_final = fecha + timedelta(days=dias_a_mostrar - 1)

            for _ in range(dias_a_mostrar):
                mes_nombre = fecha.strftime("%B %Y")
                if not calendario_data or calendario_data[-1]["mes"] != mes_nombre:
                    calendario_data.append({"mes": mes_nombre, "semanas": [[]]})

                dia_semana = fecha.weekday() 
                semana_actual = calendario_data[-1]["semanas"][-1]

                if not semana_actual and dia_semana > 0:
                    semana_actual.extend([{"dia": "", "clase": "fuera-mes"}] * dia_semana)

                dia_mes = fecha.strftime("%d")
                mes = fecha.strftime("%m")
                if fecha < datetime.strptime(fecha_inicio_str, "%Y-%m-%d") or fecha > fecha_final:
                    clase = "fuera-mes"
                elif f"{mes}-{dia_mes}" in FESTIVOS:
                    clase = "festivo"
                elif dia_semana >= 5:
                    clase = "fin-semana"
                else:
                    clase = "laborable"

                semana_actual.append({"dia": fecha.day, "clase": clase})

                if dia_semana == 6:
                    calendario_data[-1]["semanas"].append([])

                fecha += timedelta(days=1)

    return render_template(
        "index.html",
        calendario=calendario_data,
        fecha_inicio=fecha_inicio_str,
        dias_a_mostrar=dias_a_mostrar
    )

if __name__ == "__main__":
    app.run(debug=True)
