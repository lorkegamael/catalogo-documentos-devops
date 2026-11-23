# Catálogo de documentos administrativos

Aplicación local de consulta para una unidad administrativa. Cada ficha muestra título, categoría, identificador y versión. Los tres registros son ficticios. La aplicación permite consultar el catálogo y filtrar por categoría. Los archivos originales de los documentos quedan fuera del alcance de esta demostración.

## Instalación y configuración

Instala Git y Docker Desktop con contenedores Linux y Compose v2 o posterior con soporte para `--wait`. Inicia Docker Desktop y espera a que el motor esté listo. En PowerShell, abre la carpeta que contiene compose.yaml. Si el proyecto ya fue publicado, también puedes obtenerlo con `git clone https://github.com/lorkegamael/catalogo-documentos-devops.git`.

```powershell
git --version
docker version
docker compose version
Copy-Item .env.example .env
docker compose config --quiet
docker compose up -d --build --wait --wait-timeout 120
docker compose ps
```

La primera construcción necesita Internet. El valor inicial de FRONTEND_PORT es 8080. Si está ocupado, libera el puerto o cambia esa variable en .env y usa el nuevo puerto en el navegador y las pruebas. Para la evaluación se recomienda 8080.

## Uso y verificación

1. Abre http://localhost:8080. Deben aparecer «Servicio disponible» y tres documentos.
2. Elige **Finanzas**. Debe quedar el formulario de rendición ADM-002, versión 1.3. Elige **Todas** para restaurar la vista.
3. Ejecuta los comandos siguientes desde la raíz. El primero recorre el proxy de Nginx. El tercero consulta la API por nombre desde el propio contenedor frontend.
```powershell
Invoke-RestMethod http://localhost:8080/health
(Invoke-RestMethod http://localhost:8080/api/documentos).documentos | Format-Table
docker compose exec -T frontend wget -qO- http://api:5000/api/documentos
docker compose logs --tail 30 frontend api
```

Con Python 3 disponible, ejecuta `python -m unittest discover -s tests -v` y `python tests/smoke.py http://localhost:8080`. Para la prueba de extremo a extremo, mantén ambos servicios activos. El pipeline de Actions ejecuta el mismo script.

## Cierre y diagnóstico

```powershell
docker compose down
docker compose ps -a
```

Si Nginx devuelve 502, revisa `docker compose logs api frontend` y confirma que el destino sea api:5000, el proceso escuche en 0.0.0.0 y la API esté healthy. Una ruta de catálogo equivocada hace fallar /health y bloquea el arranque dependiente. Corrige el montaje o CATALOGO_ARCHIVO y repite la ejecución. El montaje de solo lectura conserva catalogo.json en el equipo después de down.

## GitHub Actions y evidencias

El workflow se activa con push a main y con pull_request cuyo destino sea main. En la pestaña **Actions**, abre **Catálogo documental**, selecciona la ejecución para el SHA del commit y luego el job **verificar**. Revisa configuración, construcción, pruebas, logs, simulación y cierre. La simulación se habilita tras un push exitoso a main. En una solicitud de cambios queda omitida por diseño.

Guarda la URL de la ejecución y dos capturas auténticas: resumen con commit y resultado, y job expandido con el resultado de smoke.py y la simulación. Para la actividad local captura compose ps, la vista con el filtro Finanzas, los logs con las dos rutas y el estado tras down. Oculta datos privados ajenos al proyecto.

## Archivos y decisiones

- api/: Flask, catálogo JSON, lector validado, dependencias y Dockerfile. Gunicorn escucha en el puerto interno 5000.
- frontend/: página accesible desde el anfitrión y proxy Nginx. El navegador usa rutas relativas del mismo origen.
- compose.yaml: red bridge propia, montaje de solo lectura, healthchecks y reinicio unless-stopped.
- tests/: pruebas de datos y prueba HTTP a través del frontend.
- .github/workflows/ci-pipeline.yml: ejecución efímera en Ubuntu, limpieza incluso si una prueba falla.
- .env.example: parámetros ficticios. .gitignore excluye .env y admite el ejemplo. El repositorio solo contiene datos simulados y no requiere claves.
