"""Genera el extracto de widebody a partir del archivo original de OpenSky.

El original pesa 242 MB y supera el límite de GitHub (100 MB), por eso no se sube
al repositorio. Este script lo descarga si hace falta, comprueba su SHA-256 y crea:
  - opensky_widebody_2019_10.csv.gz: solo los vuelos widebody, sin cambiar ningún valor.
  - opensky_extracto_info.json: datos del archivo completo que el extracto ya no permite calcular.

Uso, desde la carpeta datos/: python crear_extracto_opensky.py
"""
import hashlib
import json
import urllib.request
from pathlib import Path

import pandas as pd

CARPETA = Path(__file__).resolve().parent
NOMBRE = "flightlist_20191001_20191031.csv.gz"
URL = f"https://zenodo.org/api/records/5815448/files/{NOMBRE}/content"
SHA256 = "F49E9C40910BF62B1746BE39D447B757A41ED992D1F4337D08F5C4B41CCB629B"
TYPECODES = {
    "A380": ["A388"],
    "747": ["B741", "B742", "B743", "B744", "B748", "B74S", "B74R"],
    "A350": ["A359", "A35K"],
    "777": ["B772", "B77L", "B773", "B77W", "B778", "B779"],
    "A330": ["A332", "A333", "A338", "A339"],
    "787": ["B788", "B789", "B78X"],
}

original = CARPETA / NOMBRE
if not original.exists():
    print("Descargando el original...")
    urllib.request.urlretrieve(URL, original)

sha = hashlib.sha256(original.read_bytes()).hexdigest().upper()
if sha != SHA256:
    raise SystemExit(f"El SHA-256 no coincide: {sha}")

df = pd.read_csv(original, dtype=str, keep_default_na=False)
codigos = [c for lista in TYPECODES.values() for c in lista]
extracto = df[df["typecode"].isin(codigos)]
extracto.to_csv(CARPETA / "opensky_widebody_2019_10.csv.gz", index=False, compression={"method": "gzip", "mtime": 0})

info = {
    "fuente": "The OpenSky Network, Crowdsourced air traffic data (Zenodo, v21.12, CC-BY 4.0)",
    "doi": "10.5281/zenodo.5815448",
    "archivo_original": NOMBRE,
    "url_original": URL,
    "sha256_original": SHA256,
    "vuelos_totales": len(df),
    "columnas": list(df.columns),
    "pct_vacio_total": {c: round((df[c] == "").mean() * 100, 1) for c in df.columns},
    "vuelos_extracto": len(extracto),
    "typecodes_por_familia": TYPECODES,
}
(CARPETA / "opensky_extracto_info.json").write_text(json.dumps(info, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps(info, indent=2, ensure_ascii=False))
