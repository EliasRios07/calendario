# calendario# Calendario (Flask)

Pequeña app en Flask que genera un calendario por meses, marcando días **laborables**, **fines de semana** y **festivos** leídos desde `Data/Festivo.json`.

---

## Requisitos

- **Python 3.10+** (o la versión estable más reciente)  
  Descarga: https://www.python.org/downloads/
- **pip** (viene con Python)
- (Opcional) **virtualenv** para aislar dependencias

---

## Instalación

### 1) Clona o descarga el proyecto
```bash
git clone <tu-repo> calendario
cd calendario


py -m pip install Flask

## EJECUCIÓN
py app.py

## Estructura del proyecto
.
├─ Data/
│  └─ Festivo.json
├─ static/
│  └─ index.css
├─ templates/
│  └─ index.html
├─ app.py
└─ README.md
