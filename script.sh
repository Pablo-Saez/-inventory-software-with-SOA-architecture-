#!/bin/bash

# Ruta de la carpeta que contiene los archivos .py
carpeta="/home/pablosky/Escritorio/arqui-software/inventory-software-with-SOA-architecture-/services"

# Verifica que la carpeta exista
if [ ! -d "$carpeta" ]; then
  echo "La carpeta no existe: $carpeta"
  exit 1
fi

# Itera sobre todos los archivos .py en la carpeta y ejecútalos en segundo plano
for archivo_py in "$carpeta"/*.py; do
  if [ -f "$archivo_py" ]; then
    echo "Ejecutando $archivo_py en segundo plano"
    python3 "$archivo_py" &
  fi
done

# Espera a que todos los procesos en segundo plano finalicen
wait
