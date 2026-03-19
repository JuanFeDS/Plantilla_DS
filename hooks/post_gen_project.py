"""
Hook de post-generación para configurar el proyecto.

Configura git, entorno virtual, elimina módulos opcionales y prepara el proyecto.
"""
import shutil
import subprocess
from pathlib import Path

PROJECT_SLUG = "{{ cookiecutter.project_slug }}"
DEFAULT_BRANCH = "{{ cookiecutter.default_branch }}"
ENVIRONMENT_MANAGER = "{{ cookiecutter.environment_manager }}".lower()
PACKAGE_MANAGER = "{{ cookiecutter.package_manager }}".lower()
INCLUDE_FASTAPI = "{{ cookiecutter.include_fastapi }}" == "y"
INCLUDE_NOTEBOOKS = "{{ cookiecutter.include_notebooks }}" == "y"
INCLUDE_DOCS = "{{ cookiecutter.include_docs }}" == "y"
INCLUDE_SCRIPTS = "{{ cookiecutter.include_scripts }}" == "y"
INCLUDE_SLACK = "{{ cookiecutter.include_slack_notifications }}" == "y"
USE_DOCKER = "{{ cookiecutter.use_docker }}" == "y"

ERROR_COLOR = "\x1b[31m"
SUCCESS_COLOR = "\x1b[32m"
MESSAGE_COLOR = "\x1b[34m"
WARNING_COLOR = "\x1b[33m"
RESET_ALL = "\x1b[0m"


def run_command(cmd, error_msg=None, check=False):
    """Ejecuta comando con manejo de errores."""
    try:
        result = subprocess.run(
            cmd, 
            check=check, 
            capture_output=True, 
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        if error_msg:
            print(f'{ERROR_COLOR}❌ {error_msg}{RESET_ALL}')
            print(f'{ERROR_COLOR}   {e.stderr}{RESET_ALL}')
        return False
    except FileNotFoundError:
        if error_msg:
            print(f'{WARNING_COLOR}⚠️  {error_msg} (comando no encontrado){RESET_ALL}')
        return False


def remove_optional_modules():
    """Elimina módulos opcionales según configuración."""
    print(f'{MESSAGE_COLOR}🗑️  Limpiando módulos opcionales...{RESET_ALL}')

    if not INCLUDE_FASTAPI:
        api_path = Path('src/api')
        if api_path.exists():
            shutil.rmtree(api_path)
            print(f'{MESSAGE_COLOR}   • API removida{RESET_ALL}')

    if not INCLUDE_NOTEBOOKS:
        notebooks_path = Path('notebooks')
        if notebooks_path.exists():
            shutil.rmtree(notebooks_path)
            print(f'{MESSAGE_COLOR}   • Notebooks removidos{RESET_ALL}')

    if not INCLUDE_DOCS:
        docs_path = Path('docs')
        if docs_path.exists():
            shutil.rmtree(docs_path)
            print(f'{MESSAGE_COLOR}   • Documentación removida{RESET_ALL}')

    if not INCLUDE_SCRIPTS:
        scripts_path = Path('scripts')
        if scripts_path.exists():
            shutil.rmtree(scripts_path)
            print(f'{MESSAGE_COLOR}   • Scripts CLI removidos{RESET_ALL}')

    if not INCLUDE_SLACK:
        slack_path = Path('src/notifications/slack.py')
        if slack_path.exists():
            slack_path.unlink()
            print(f'{MESSAGE_COLOR}   • Notificaciones Slack removidas{RESET_ALL}')


def init_git():
    """Inicializa repositorio git."""
    if Path('.git').exists():
        print(f'{WARNING_COLOR}⚠️  Repositorio git ya existe, omitiendo inicialización{RESET_ALL}')
        return

    print(f'{MESSAGE_COLOR}📦 Inicializando repositorio git...{RESET_ALL}')

    if not run_command(['git', 'init'], 'Error al inicializar git'):
        return

    if DEFAULT_BRANCH != 'master':
        run_command(
            ['git', 'branch', '-M', DEFAULT_BRANCH],
            f'Error al renombrar rama a {DEFAULT_BRANCH}'
        )

    run_command(['git', 'add', '.'], 'Error al agregar archivos')

    run_command(
        ['git', 'commit', '-m', 'chore ⚒️: initial commit'],
        'Error al crear commit inicial'
    )

    print(f'{SUCCESS_COLOR}   ✅ Git inicializado en rama {DEFAULT_BRANCH}{RESET_ALL}')


def setup_environment():
    """Configura entorno virtual según el manager seleccionado."""
    print(f'{MESSAGE_COLOR}🐍 Configurando entorno virtual...{RESET_ALL}')

    if ENVIRONMENT_MANAGER == 'virtualenv':
        print(f'{MESSAGE_COLOR}   • Creando venv con virtualenv...{RESET_ALL}')
        if run_command(['python', '-m', 'venv', 'venv']):
            print(f'{SUCCESS_COLOR}   ✅ Entorno virtual creado{RESET_ALL}')
            print(f'{MESSAGE_COLOR}   💡 Activa con: venv\\Scripts\\activate (Windows) o source venv/bin/activate (Linux/Mac){RESET_ALL}')
        else:
            print(f'{ERROR_COLOR}   ❌ Error al crear venv{RESET_ALL}')

    elif ENVIRONMENT_MANAGER == 'conda':
        print(f'{MESSAGE_COLOR}   • Creando entorno conda...{RESET_ALL}')
        if run_command(['conda', 'create', '-n', PROJECT_SLUG, 'python={{ cookiecutter.python_version }}', '-y']):
            print(f'{SUCCESS_COLOR}   ✅ Entorno conda creado{RESET_ALL}')
            print(f'{MESSAGE_COLOR}   💡 Activa con: conda activate {PROJECT_SLUG}{RESET_ALL}')
        else:
            print(f'{WARNING_COLOR}   ⚠️  Conda no disponible, crea el entorno manualmente{RESET_ALL}')

    elif ENVIRONMENT_MANAGER == 'pipenv':
        print(f'{MESSAGE_COLOR}   • Configurando pipenv...{RESET_ALL}')
        if run_command(['pipenv', '--python', '{{ cookiecutter.python_version }}']):
            print(f'{SUCCESS_COLOR}   ✅ Pipenv configurado{RESET_ALL}')
            print(f'{MESSAGE_COLOR}   💡 Activa con: pipenv shell{RESET_ALL}')
        else:
            print(f'{WARNING_COLOR}   ⚠️  Pipenv no disponible{RESET_ALL}')

    elif ENVIRONMENT_MANAGER == 'poetry':
        print(f'{MESSAGE_COLOR}   • Configurando poetry...{RESET_ALL}')
        if run_command(['poetry', 'install']):
            print(f'{SUCCESS_COLOR}   ✅ Poetry configurado{RESET_ALL}')
            print(f'{MESSAGE_COLOR}   💡 Activa con: poetry shell{RESET_ALL}')
        else:
            print(f'{WARNING_COLOR}   ⚠️  Poetry no disponible{RESET_ALL}')

    else:
        print(f'{MESSAGE_COLOR}   • Sin entorno virtual configurado{RESET_ALL}')
        print(f'{MESSAGE_COLOR}   💡 Puedes crear uno manualmente cuando lo necesites{RESET_ALL}')


def show_next_steps():
    """Muestra próximos pasos al usuario."""
    print()
    print(f'{SUCCESS_COLOR}╔══════════════════════════════════════════════════╗{RESET_ALL}')
    print(f'{SUCCESS_COLOR}║  ✅ Proyecto generado exitosamente              ║{RESET_ALL}')
    print(f'{SUCCESS_COLOR}╚══════════════════════════════════════════════════╝{RESET_ALL}')
    print()
    print(f'{MESSAGE_COLOR}📋 Próximos pasos:{RESET_ALL}')
    print(f'{MESSAGE_COLOR}   1. cd {PROJECT_SLUG}{RESET_ALL}')

    if ENVIRONMENT_MANAGER != 'none':
        if ENVIRONMENT_MANAGER == 'virtualenv':
            print(f'{MESSAGE_COLOR}   2. Activa el entorno: venv\\Scripts\\activate{RESET_ALL}')
        elif ENVIRONMENT_MANAGER == 'conda':
            print(f'{MESSAGE_COLOR}   2. Activa el entorno: conda activate {PROJECT_SLUG}{RESET_ALL}')
        elif ENVIRONMENT_MANAGER == 'pipenv':
            print(f'{MESSAGE_COLOR}   2. Activa el entorno: pipenv shell{RESET_ALL}')
        elif ENVIRONMENT_MANAGER == 'poetry':
            print(f'{MESSAGE_COLOR}   2. Activa el entorno: poetry shell{RESET_ALL}')
        print(f'{MESSAGE_COLOR}   3. Instala dependencias: pip install -r requirements.txt{RESET_ALL}')
    else:
        print(f'{MESSAGE_COLOR}   2. Instala dependencias: pip install -r requirements.txt{RESET_ALL}')

    print(f'{MESSAGE_COLOR}   4. Lee la documentación en docs/README.md{RESET_ALL}')
    print(f'{MESSAGE_COLOR}   5. Revisa los workflows en .windsurf/workflows/{RESET_ALL}')
    print()
    print(f'{SUCCESS_COLOR}🚀 ¡Feliz coding!{RESET_ALL}')
    print()


def main():
    """Ejecuta configuración post-generación."""
    print()
    print(f'{MESSAGE_COLOR}⚙️  Configurando proyecto...{RESET_ALL}')
    print()

    remove_optional_modules()
    init_git()
    setup_environment()
    show_next_steps()


if __name__ == '__main__':
    main()
