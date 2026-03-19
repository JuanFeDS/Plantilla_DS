# Plantilla Data Science

Plantilla para levantar proyectos de ciencia de datos con capas listas para datos, modelos, APIs y operaciones. En pocos minutos obtienes una base profesional, modular y ajustable mediante banderas de Cookiecutter.

---

## 📌 ¿Qué incluye?

- ✅ Estructura modular (`src/`, `scripts/`, `docs/`, `notebooks/`, `models/`).
- ✅ Hooks de pre/post generación con validaciones y automatizaciones (`git init`, entornos, limpieza de módulos opcionales).
- ✅ Conectores a BD, pipelines de datos, features, logging y notificaciones.
- ✅ API FastAPI opcional, Slack opcional, Docker opcional.
- ✅ Workflows base (tests, docs, despliegue) y documentación exhaustiva.

---

## ⚙️ Variables de cookiecutter

| Clave | ¿Para qué sirve? |
| --- | --- |
| `full_name`, `email`, `github_username` | Se usan en README, metadata y commits iniciales. |
| `project_title` | Nombre formal del proyecto (puede tener espacios). |
| `project_slug` | Slug en minúsculas (validado en `pre_gen_project.py`). |
| `project_description` | Resumen que alimenta README y doc inicial. |
| `organization`, `repository_url` | Referencias corporativas y enlaces oficiales. |
| `python_version` | Selecciona la versión base (3.11/3.10/3.9) para entornos. |
| `license` | Inserta el tipo de licencia en README/DOCS. |
| `package_manager` | Indica la estrategia preferida (`poetry`, `pip`, `uv`). |
| `environment_manager` | Crea entornos con `virtualenv`, `conda`, `pipenv`, `poetry` o `none`. |
| `include_fastapi` | Si es `n`, se elimina `src/api/` y dependencias HTTP. |
| `include_notebooks` | Controla la carpeta `notebooks/`. |
| `include_docs` | Activa o borra `docs/`. |
| `include_slack_notifications` | Mantiene o elimina `src/notifications/slack.py`. |
| `default_branch` | Rama inicial para `git init` (ej. `main`, `develop`). |
| `initial_model_name` | Nombre por defecto para artefactos en `models/`. |
| `use_docker` | Duplica archivos Docker únicamente cuando se requiere. |

> Todos los valores tienen defaults; puedes aceptar o personalizar según el proyecto.

---

## 🏗️ Estructura generada (modo completo)

| Carpeta / Archivo | Contenido | Se elimina si… |
| --- | --- | --- |
| `docs/` | Índice, estructura, guías de modelo/datos/ops. | `include_docs = 'n'` |
| `notebooks/` | Ejemplos exploratorios y workflows. | `include_notebooks = 'n'` |
| `scripts/` | CLI para data processing, training, evaluation. | — |
| `src/api/` | FastAPI + modelos Pydantic. | `include_fastapi = 'n'` |
| `src/bd/` | Conectores a bases de datos. | — |
| `src/data/`, `src/features/`, `src/pipelines/` | Pipelines y feature engineering base. | — |
| `src/notifications/` | Integraciones con Slack u otros canales. | `include_slack_notifications = 'n'` |
| `src/logger/` | Logger centralizado reutilizable. | — |
| `models/` | Experimentos, producción y metadata del modelo. | — |
| `.windsurf/workflows/` | Workflows para pruebas, revisión y commits. | — |
| `pyproject.toml` / `requirements.txt` | Dependencias según gestores elegidos. | — |
| `README.md` | Documentación inicial personalizada. | — |

El hook `post_gen_project.py` aplica estas reglas justo después de generar el proyecto, por lo que recibirás únicamente los módulos solicitados.

---

## 🚀 Guía de Uso

### 1. Instala cookiecutter

```bash
pip install cookiecutter
```

### 2. Genera un proyecto

```bash
cookiecutter https://github.com/JuanFeA98/Plantilla_DS
```

### 3. Después de generar

El hook `post_gen_project.py` se encarga de:

1. Inicializar git (`git init`, `git add .`, `git commit -m "chore ⚒️: initial commit"`).
2. Crear entornos según lo seleccionado (`venv`, `conda`, `pipenv`, `poetry`).
3. Eliminar módulos no deseados (API, notebooks, docs, Slack).
4. Mostrar los siguientes pasos (activar entorno, instalar deps, leer docs).

Si algún comando no existe en tu máquina, se mostrará un warning y podrás hacerlo manualmente.

---

## 📚 Documentación y Workflows

- **`docs/README.md`**: índice completo de documentación (modelo, datos, operaciones, configuraciones).
- **`docs/STRUCTURE.md`**: detalle de carpetas y responsabilidades.
- **`.windsurf/workflows/`**: guías para ejecutar tests, revisar el proyecto o generar commits.

---

## 🧪 Requisitos mínimos

- Python `>=3.9`.
- `cookiecutter` instalado globalmente.
- Opcional: `git`, `virtualenv`, `conda`, `poetry`, `pipenv`, `docker` (según selección).

---

## 🤝 Contribuciones

1. Haz fork del repositorio.
2. Crea una rama feature (`git checkout -b feat/nueva-capacidad`).
3. Ejecuta `cookiecutter --no-input` para probar cambios.
4. Envía PR con descripción y screenshots si aplica.

---

## 📞 Soporte

- Autor: [JuanFeA98](https://github.com/JuanFeA98)
- Reporta issues en GitHub o abre discusiones en el repositorio.

