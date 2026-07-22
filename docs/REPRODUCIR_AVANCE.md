# Reproducir el avance sin limpieza

Entorno probado: Python 3.12. Las versiones exactas de las dependencias están en requirements.txt.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m src.consolidar
```

El comando verifica los 23 CSV, consolida las 17 columnas, genera el diagnóstico previo y compara las métricas con el PDF del 22. No necesita red y no ejecuta ninguna transformación sobre el conjunto de origen.

Para una nueva extracción, use otra carpeta y conserve las versiones existentes:

```powershell
python -m src.obtener --destino data/nueva_extraccion
```

La descarga inicial es una operación en red; reejecutar el diagnóstico y la limpieza sobre la copia versionada es local. Los scripts no requieren tokens, contraseñas ni credenciales del MINEDUC.
