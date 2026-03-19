"""
Hook de pre-generación para validar inputs del cookiecutter.

Valida que el nombre del proyecto sea válido antes de generar archivos.
"""
import re
import sys

PROJECT_SLUG = "{{ cookiecutter.project_slug }}"
PROJECT_TITLE = "{{ cookiecutter.project_title }}"
ORGANIZATION = "{{ cookiecutter.organization }}"
PYTHON_VERSION = "{{ cookiecutter.python_version }}"

ERROR_COLOR = "\x1b[31m"
SUCCESS_COLOR = "\x1b[32m"
MESSAGE_COLOR = "\x1b[34m"
WARNING_COLOR = "\x1b[33m"
RESET_ALL = "\x1b[0m"

RESERVED_SLUGS = {
    'test', 'tests', 'src', 'lib', 'bin', 'venv', 'env',
    'data', 'docs', 'scripts', 'models', 'notebooks',
    'python', 'pip', 'conda', 'poetry', 'docker'
}

def validate_project_slug(slug):
    """Valida que el slug del proyecto sea válido."""
    errors = []

    if len(slug) < 3:
        errors.append("El nombre debe tener al menos 3 caracteres")

    if len(slug) > 50:
        errors.append("El nombre no debe exceder 50 caracteres")

    if not re.match(r'^[a-z][a-z0-9_]*$', slug):
        errors.append(
            "El nombre debe empezar con letra minúscula y solo contener "
            "letras minúsculas, números y guiones bajos"
        )

    if slug in RESERVED_SLUGS:
        errors.append(
            f"'{slug}' es un nombre reservado. "
            f"Usa un nombre más específico"
        )

    if slug.startswith('_') or slug.endswith('_'):
        errors.append("El nombre no debe empezar ni terminar con guión bajo")

    if '__' in slug:
        errors.append("El nombre no debe contener guiones bajos consecutivos")

    return errors

def main():
    """Ejecuta validaciones pre-generación."""
    print(f'{MESSAGE_COLOR}╔══════════════════════════════════════════════════╗{RESET_ALL}')
    print(f'{MESSAGE_COLOR}║  Generando Plantilla de Ciencia de Datos        ║{RESET_ALL}')
    print(f'{MESSAGE_COLOR}╚══════════════════════════════════════════════════╝{RESET_ALL}')
    print()
    print(f'{MESSAGE_COLOR}📦 Proyecto: {PROJECT_TITLE}{RESET_ALL}')
    print(f'{MESSAGE_COLOR}🏢 Organización: {ORGANIZATION}{RESET_ALL}')
    print(f'{MESSAGE_COLOR}🐍 Python: {PYTHON_VERSION}{RESET_ALL}')
    print(f'{MESSAGE_COLOR}📁 Slug: {PROJECT_SLUG}{RESET_ALL}')
    print()

    errors = validate_project_slug(PROJECT_SLUG)

    if errors:
        print(f'{ERROR_COLOR}❌ Errores de validación:{RESET_ALL}')
        for error in errors:
            print(f'{ERROR_COLOR}   • {error}{RESET_ALL}')
        print()
        print(f'''
            {WARNING_COLOR}💡 Sugerencia: Usa un nombre como "mi_proyecto_ds" 
            o "analisis_ventas"{RESET_ALL}
        ''')
        sys.exit(1)

    print(f'{SUCCESS_COLOR}✅ Validaciones pasadas. Generando proyecto...{RESET_ALL}')
    print()

if __name__ == '__main__':
    main()
